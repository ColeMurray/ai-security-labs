import os, json, logging
from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
from typing import Dict, Callable

# --------------------------------------------------------------------------- #
#  OpenAI client – real or monkey-patched by tests (see tests/conftest.py)
# --------------------------------------------------------------------------- #
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "DUMMY"))

# --------------------------------------------------------------------------- #
#  System datastore
# --------------------------------------------------------------------------- #
# In-memory storage of venues and events
VENUES = {
    "V001": {
        "id": "V001",
        "name": "Main Concert Hall",
        "total_seats": 500,
        "seat_price": 75.00,
        "location": "123 Music Ave, Austin, TX",
    }
}

EVENTS = {
    "E001": {
        "id": "E001",
        "name": "Rock Symphony",
        "venue_id": "V001",
        "date": "2023-09-15",
        "time": "20:00",
        "available_seats": 500,
        "description": "Classical meets rock in this unique orchestral experience"
    }
}

# Track bookings (not used in this simplified demo but kept for structure)
BOOKINGS = {}

# --------------------------------------------------------------------------- #
#  Tool implementations
# --------------------------------------------------------------------------- #
def book_seats(num_seats: int = 1, customer_name: str = None, customer_email: str = None) -> str:
    """
    Book seats for the Rock Symphony event with proper validation.
    
    ✅ SECURE: This function validates the num_seats parameter properly,
    preventing attackers from booking an excessive number of seats
    """
    # Comprehensive input validation
    if not customer_name or not customer_email:
        return "Customer name and email are required."
    
    # Proper parameter validation ✅
    # Validate num_seats is within reasonable limits
    MAX_SEATS_PER_BOOKING = 10
    if num_seats <= 0:
        return "Number of seats must be positive."
    if num_seats > MAX_SEATS_PER_BOOKING:
        return f"Cannot book more than {MAX_SEATS_PER_BOOKING} seats in a single transaction."
    
    # Check if enough seats are available
    if EVENTS["E001"]["available_seats"] < num_seats:
        return f"Not enough seats available. Only {EVENTS['E001']['available_seats']} seats left."
    
    # Get venue for this event
    venue_id = EVENTS["E001"]["venue_id"]
    venue = VENUES[venue_id]
    
    # Calculate cost
    total_cost = venue["seat_price"] * num_seats
    
    # Update available seats
    EVENTS["E001"]["available_seats"] -= num_seats
    
    logging.warning(f"🎟️ BOOKING: {num_seats} seats by {customer_name} - ${total_cost:.2f}")
    
    # Return confirmation
    result = {
        "status": "confirmed",
        "event": EVENTS["E001"]["name"],
        "num_seats": num_seats,
        "total_cost": total_cost,
        "customer_name": customer_name
    }
    
    return json.dumps(result, indent=2)

# --------------------------------------------------------------------------- #
#  Parameter validation
# --------------------------------------------------------------------------- #
def validate_parameters(parameters: Dict[str, any]) -> Dict[str, any]:
    """
    Validates and sanitizes parameters before they are passed to tools.
    
    ✅ SECURE: This prevents parameter pollution by validating inputs
    """
    # General validation and sanitization
    validated = {}
    
    # Copy necessary parameters
    if "num_seats" in parameters:
        try:
            # Convert to int and validate
            num_seats = int(parameters["num_seats"])
            MAX_SEATS_PER_BOOKING = 10
            
            if num_seats <= 0:
                raise HTTPException(status_code=400, detail="Number of seats must be positive")
            if num_seats > MAX_SEATS_PER_BOOKING:
                raise HTTPException(status_code=400, 
                                   detail=f"Cannot book more than {MAX_SEATS_PER_BOOKING} seats in a single transaction")
            
            validated["num_seats"] = num_seats
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid number of seats")
    
    # Copy customer information
    if "customer_name" in parameters:
        validated["customer_name"] = parameters["customer_name"]
    
    if "customer_email" in parameters:
        validated["customer_email"] = parameters["customer_email"]
        
    return validated

# --------------------------------------------------------------------------- #
#  Tool registry & Schema
# --------------------------------------------------------------------------- #
TOOLS: Dict[str, Callable[..., str]] = {
    "book_seats": book_seats,
}

FUNCTION_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "book_seats",
            "description": "Book seats for the Rock Symphony event",
            "parameters": {
                "type": "object",
                "properties": {
                    "num_seats": {
                        "type": "integer", 
                        "description": "Number of seats to book (maximum 10)"
                    },
                    "customer_name": {
                        "type": "string", 
                        "description": "Name of the customer making the booking"
                    },
                    "customer_email": {
                        "type": "string", 
                        "description": "Email of the customer making the booking"
                    }
                },
                "required": ["customer_name", "customer_email"]
            },
        },
    }
]

# --------------------------------------------------------------------------- #
app = FastAPI()

class Req(BaseModel):
    prompt: str

@app.post("/agent")
async def agent(req: Req = Body(...)):
    """
    Process user requests with proper parameter validation.
    
    ✅ SECURE: Parameters from LLM are validated before being used
    """
    messages = [
        {"role": "system", "content": "You are a helpful event booking assistant. Help users book tickets for the Rock Symphony."},
        {"role": "user", "content": req.prompt},
    ]

    # Process the user request
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=FUNCTION_SCHEMA,
        tool_choice="auto",
    )
    
    # Handle tool calls
    actions_log = []
    MAX_ITERATIONS = 10  # Maximum number of iterations to prevent infinite loop
    iteration_count = 0
    while resp.choices and resp.choices[0].message.tool_calls:
        if iteration_count >= MAX_ITERATIONS:
            logging.warning("Maximum iteration limit reached in tool call loop. Exiting loop to prevent non-termination.")
            break
        iteration_count += 1
        
        msg = resp.choices[0].message
        
        # Add the assistant message to conversation
        messages.append({
            "role": "assistant",
            "content": msg.content or "",
            "tool_calls": [
                {
                    "id": call.id,
                    "type": "function",
                    "function": {
                        "name": call.function.name,
                        "arguments": call.function.arguments
                    }
                }
                for call in msg.tool_calls
            ]
        })
        
        # Process each tool call
        tool_results = []
        for call in msg.tool_calls:
            args = json.loads(call.function.arguments or "{}")
            logging.info(f"Validating args for book_seats: {args}")
            
            # ✅ SECURE: Validate parameters from LLM before passing to function
            validated_args = validate_parameters(args)
            logging.info(f"Executing book_seats with validated args: {validated_args}")
            
            # Execute the tool with validated parameters
            result = book_seats(**validated_args)
            
            # Add tool result
            tool_results.append({
                "role": "tool",
                "tool_call_id": call.id,
                "name": "book_seats",
                "content": result
            })
            
            # Log for response
            actions_log.append({
                "tool": "book_seats",
                "args": validated_args,
                "result": result
            })
        
        # Add tool results to messages
        messages.extend(tool_results)
        
        # Get next response
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=FUNCTION_SCHEMA,
            tool_choice="auto",
        )
    
    # Final response
    final_content = resp.choices[0].message.content if resp.choices else "No response"
    return {
        "answer": final_content,
        "actions": actions_log
    } 
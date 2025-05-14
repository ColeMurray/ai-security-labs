import pytest, types, json
from unittest.mock import MagicMock

@pytest.fixture(autouse=True)
def stub_openai(monkeypatch):
    """
    Replace OpenAI client with a deterministic stub:

    * If user's prompt contains 'book' and a large number like '500', it calls book_seats with excessive seats
    * For legitimate prompts it performs appropriate booking with reasonable seat numbers
    """
    # Counter to track the number of calls
    call_counter = {"count": 0}

    def fake_chat_completion_create(model, messages, tools, tool_choice):
        call_counter["count"] += 1
        
        # Check if this is a follow-up call after a tool was used
        assistant_messages = [m for m in messages if m.get("role") == "assistant" and m.get("tool_calls")]
        tool_messages = [m for m in messages if m.get("role") == "tool"]
        
        # Determine if this is a follow-up call in a tool chain
        is_followup = len(assistant_messages) > 0 and len(tool_messages) > 0
        
        # Get the latest user prompt (if any)
        user_prompts = [m.get("content", "") for m in messages if m.get("role") == "user"]
        latest_prompt = user_prompts[-1].lower() if user_prompts else ""
        
        # Create empty response
        msg = types.SimpleNamespace(
            tool_calls=None, 
            content="I've processed your request."
        )

        # Only simulate tools we care about for the exploit test
        tools_map = {t["function"]["name"]: t for t in tools}
        tool_names = list(tools_map.keys())
        
        # First call in conversation with no prior tool usage
        if not is_followup:
            if "list events" in latest_prompt or "show events" in latest_prompt:
                # Call list_events
                if "list_events" in tool_names:
                    call = types.SimpleNamespace(
                        id="call_list_events",
                        function=types.SimpleNamespace(
                            name="list_events",
                            arguments="{}",
                        )
                    )
                    msg.tool_calls = [call]
            elif "event details" in latest_prompt and ("e001" in latest_prompt or "rock symphony" in latest_prompt):
                # Call get_event_details for Rock Symphony
                if "get_event_details" in tool_names:
                    call = types.SimpleNamespace(
                        id="call_event_details",
                        function=types.SimpleNamespace(
                            name="get_event_details",
                            arguments=json.dumps({"event_id": "E001"}),
                        )
                    )
                    msg.tool_calls = [call]
            elif "book" in latest_prompt and "seat" in latest_prompt:
                # Determine if this is an excessive booking attempt
                excessive = False
                seat_count = 2  # Default for reasonable booking
                
                # Look for excessive numbers in the prompt
                import re
                numbers = re.findall(r'\d+', latest_prompt)
                if numbers:
                    largest_num = max([int(n) for n in numbers])
                    if largest_num > 20:  # Consider anything over 20 as excessive
                        seat_count = largest_num
                        excessive = True
                    else:
                        seat_count = largest_num
                
                # Get event ID from prompt or default to E001
                event_id = "E001"  # Default to Rock Symphony
                if "e002" in latest_prompt:
                    event_id = "E002"
                elif "e003" in latest_prompt:
                    event_id = "E003"
                
                # Extract name from prompt or use default
                name = "John Smith"  # Default name
                email = "john@example.com"  # Default email
                
                if "book_seats" in tool_names:
                    call = types.SimpleNamespace(
                        id="call_book_seats",
                        function=types.SimpleNamespace(
                            name="book_seats",
                            arguments=json.dumps({
                                "event_id": event_id,
                                "num_seats": seat_count,
                                "customer_name": name,
                                "customer_email": email
                            }),
                        )
                    )
                    msg.tool_calls = [call]
            elif "booking" in latest_prompt and "detail" in latest_prompt:
                # Call get_booking_details - would need a valid booking ID
                if "get_booking_details" in tool_names:
                    call = types.SimpleNamespace(
                        id="call_booking_details",
                        function=types.SimpleNamespace(
                            name="get_booking_details",
                            arguments=json.dumps({"booking_id": "BDUMMY123"}),
                        )
                    )
                    msg.tool_calls = [call]
            elif "cancel" in latest_prompt and "booking" in latest_prompt:
                # Call cancel_booking - would need a valid booking ID
                if "cancel_booking" in tool_names:
                    call = types.SimpleNamespace(
                        id="call_cancel_booking",
                        function=types.SimpleNamespace(
                            name="cancel_booking",
                            arguments=json.dumps({"booking_id": "BDUMMY123"}),
                        )
                    )
                    msg.tool_calls = [call]

        choice = types.SimpleNamespace(message=msg)
        return types.SimpleNamespace(choices=[choice])

    dummy_client = types.SimpleNamespace(
        chat=types.SimpleNamespace(
            completions=types.SimpleNamespace(create=fake_chat_completion_create)
        )
    )

    # patch both starter and solution modules *when they import*
    monkeypatch.setattr("openai.OpenAI", lambda *_, **__: dummy_client)
    yield 
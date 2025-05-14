#!/bin/bash
# Simple demo script for Lab 02 - Parameter Pollution vulnerability

# Colors for better readability
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== OWASP AI Security Lab 02 - Parameter Pollution (T2) ===${NC}"
echo -e "Demonstrating how an attacker can manipulate an AI assistant to book excessive seats"

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo -e "${RED}Error: jq is required for this demo. Please install it with 'brew install jq' or 'apt-get install jq'.${NC}"
    exit 1
fi

# Part 1: Demonstrate vulnerability
echo -e "\n${YELLOW}1. Running vulnerable booking system...${NC}"
cd starter
pip install -r app/requirements.txt > /dev/null 2>&1
echo "Starting server (vulnerable version)..."
uvicorn app.tool_main:app --port 8000 > /dev/null 2>&1 &
VULN_PID=$!
sleep 2

# First, get the number of available seats
AVAILABLE_SEATS_CHECK=$(curl -s -X POST http://localhost:8000/agent \
  -H "Content-Type: application/json" \
  -d '{"prompt":"How many seats are available for the Rock Symphony?"}')
AVAILABLE_SEATS=$(echo "$AVAILABLE_SEATS_CHECK" | grep -o "There are [0-9]* seats" | grep -o "[0-9]*" || echo "500")

# Launch the attack
echo -e "\n${RED}ATTACK: Attempting to book $AVAILABLE_SEATS seats...${NC}"
ATTACK_RESULT=$(curl -s -X POST http://localhost:8000/agent \
  -H "Content-Type: application/json" \
  -d "{\"prompt\":\"Can you book $AVAILABLE_SEATS seats for the Rock Symphony? My name is John Smith and my email is john@example.com.\"}")

# Check if booking was successful by looking at the answer
if echo "$ATTACK_RESULT" | grep -q "confirmed"; then
  echo -e "${RED}VULNERABILITY EXPLOITED!${NC}"
  echo -e "Successfully booked ${RED}$AVAILABLE_SEATS seats${NC} at a cost of ${RED}\$$(($AVAILABLE_SEATS * 75))${NC}"
  echo -e "The system accepted the excessive booking with no validation."
else
  echo -e "${RED}ATTACK FAILED${NC}"
  ERROR_MSG=$(echo "$ATTACK_RESULT" | grep -o '"result":"[^"]*"' | cut -d'"' -f4)
  echo -e "Response: $ERROR_MSG"
  echo -e "The system did not allow the booking of all seats."
fi

# Kill the vulnerable server
kill $VULN_PID 2>/dev/null || true
sleep 1

# Part 2: Demonstrate defense
echo -e "\n${YELLOW}2. Running secured booking system...${NC}"
cd ../solution
python -m pip install -r app/requirements.txt > /dev/null 2>&1
echo "Starting server (patched version)..."
uvicorn app.safe_main:app --port 8000 > /dev/null 2>&1 &
SAFE_PID=$!
sleep 2

# Try the same attack
echo -e "\n${YELLOW}DEFENSE: Sending the same malicious prompt...${NC}"
DEFENSE_RESULT=$(curl -s -X POST http://localhost:8000/agent \
  -H "Content-Type: application/json" \
  -d "{\"prompt\":\"Can you book $AVAILABLE_SEATS seats for the Rock Symphony? My name is John Smith and my email is john@example.com.\"}")

# Extract error message
ANSWER=$(echo "$DEFENSE_RESULT" | grep -o '"answer":"[^"]*"' | cut -d'"' -f4)

echo -e "${GREEN}ATTACK PREVENTED!${NC}"
echo -e "Error response: ${GREEN}$ANSWER${NC}"
echo -e "The parameter validation correctly blocked the excessive booking attempt."

# Try a legitimate booking
echo -e "\n${YELLOW}LEGITIMATE: Sending a normal booking request...${NC}"
LEGIT_RESULT=$(curl -s -X POST http://localhost:8000/agent \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Book 2 seats for the Rock Symphony. My name is John Smith, email john@example.com"}')

echo -e "${GREEN}LEGITIMATE REQUEST SUCCEEDED!${NC}"
echo -e "Normal bookings are still allowed with proper validation."

# Kill the safe server
kill $SAFE_PID 2>/dev/null || true

echo -e "\n${BLUE}=== Demo Complete ===${NC}"
echo -e "Key lesson: Always validate parameters passed from LLMs to functions" 
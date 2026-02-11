import asyncio
import re
import time
import uuid

# Mock the AI Logic
class MockAI:
    def __init__(self):
        self.state = "START"
        self.data = {}

    def process(self, text):
        print(f"\n[AI Thinking] Analyzing: '{text}'...")
        time.sleep(1) # Simulate latency
        
        text = text.lower()
        
        # 1. Intent Extraction
        if "buy" in text: self.data['intent'] = "Buy"
        if "rent" in text: self.data['intent'] = "Rent"
        
        # 2. Name Extraction (Simple heuristic)
        if "name is" in text: 
            parts = text.split("name is")
            if len(parts) > 1: self.data['name'] = parts[1].split()[0].strip().capitalize()
        elif "i am" in text:
             parts = text.split("i am")
             if len(parts) > 1: self.data['name'] = parts[1].split()[0].strip().capitalize()

        # 3. Phone Extraction
        phone_match = re.search(r'\d{9,}', text)
        if phone_match: self.data['phone'] = phone_match.group(0)

        # Decision Logic
        if 'intent' not in self.data:
            return "Hello! Are you looking to Buy or Rent?"
        
        if 'name' not in self.data:
            return "Great. What is your name?"
        
        if 'phone' not in self.data:
            return f"Hi {self.data['name']}, can I have your phone number for our agent?"
        
        # All data present -> Call "Tool"
        return self.call_tool()

    def call_tool(self):
        print("\n[Tool Call] create_lead_task(...)")
        print(f"   Name: {self.data['name']}")
        print(f"   Phone: {self.data['phone']}")
        print(f"   Intent: {self.data['intent']}")
        time.sleep(1)
        
        # Mock ClickUp Response
        task_id = str(uuid.uuid4())[:8]
        print(f"✅ [System] Task created in ClickUp! (ID: {task_id})")
        
        return f"Perfect! I have connected you with an agent. Ticket #{task_id}."

async def main():
    print("========================================")
    print("   MOCK TERMINAL MODE (No Keys Needed)  ")
    print("========================================")
    print("Simulating Telegram Chat... Type 'exit' to quit.\n")
    
    ai = MockAI()
    
    while True:
        user_input = input("You (User): ")
        if user_input.lower() in ['exit', 'quit']:
            break
            
        response = ai.process(user_input)
        print(f"Bot (AI): {response}\n")

if __name__ == "__main__":
    asyncio.run(main())

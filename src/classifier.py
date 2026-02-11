import re

class LeadClassifier:
    def __init__(self):
        self.phone_pattern = re.compile(r'(\+?\d{9,15})')
        self.intent_patterns = {
            'buy': re.compile(r'\b(buy|purchase|interested in buying)\b', re.IGNORECASE),
            'rent': re.compile(r'\b(rent|lease|looking for rent)\b', re.IGNORECASE),
            'sell': re.compile(r'\b(sell|listing my property)\b', re.IGNORECASE)
        }

    def classify(self, text):
        """
        Parses the text to extract lead information.
        Expected input: "Hi, I am Ali (0501234567). Looking to buy a villa."
        """
        lead_data = {
            'original_text': text,
            'name': 'Unknown',
            'phone': None,
            'intent': 'General Inquiry',
            'priority': 'Normal'
        }

        # Extract Phone
        phone_match = self.phone_pattern.search(text)
        if phone_match:
            lead_data['phone'] = phone_match.group(1)

        # Determine Intent
        for intent, pattern in self.intent_patterns.items():
            if pattern.search(text):
                lead_data['intent'] = intent.capitalize()
                break

        # Simple Name Extraction (Heuristic: First 2 words if no obvious greeting)
        # This is very basic; NLP would be better, but regex is fast for MVP.
        # We'll just look for "I am {Name}" or "Name: {Name}"
        name_match = re.search(r'(?:I am|I\'m|Name:)\s+([A-Za-z]+)', text, re.IGNORECASE)
        if name_match:
            lead_data['name'] = name_match.group(1)

        return lead_data

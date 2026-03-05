import requests
import csv

class B2BContentEngine:
    def __init__(self):
        # Local Ollama URL (Default for Windows and Linux)
        self.api_url = "http://localhost:11434/api/generate"
        self.sales_data = self.load_sales_trends()

    def load_sales_trends(self):
        trends = {}
        try:
            with open('sales_trends.csv', mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    trends[row['category'].lower()] = row
        except FileNotFoundError:
            print("Warning: sales_trends.csv not found.")
        return trends

    def generate_with_trends(self, product_name, category, features):
        trend = self.sales_data.get(category.lower(), {})
        selling_point = trend.get('top_selling_point', 'efficiency')
        
        prompt = (f"Write a professional B2B product description focusing on {selling_point}. "
                  f"Product: {product_name}. Features: {features}. Description:")

        # Ollama payload
        payload = {
            "model": "llama3.2:1b",
            "prompt": prompt,
            "stream": False
        }

        try:
            response = requests.post(self.api_url, json=payload)
            if response.status_code == 200:
                return response.json().get('response', '').strip()
            else:
                return f"Ollama Error: {response.status_code}. Make sure Ollama is running."
        except Exception as e:
            return "Connection Error: Is the Ollama app open in your taskbar?"

    def audit_content(self, text, category):
        trend = self.sales_data.get(category.lower(), {})
        avoid = trend.get('avoid_words', '')
        issues = [f"B2B Audit: Remove '{w.strip()}'" for w in avoid.split(',') if w.strip() and w.strip().lower() in text.lower()]
        
        return {
            "status": "Approved" if not issues else "Needs Optimization",
            "feedback": issues
        }
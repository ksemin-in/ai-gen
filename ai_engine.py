import csv
import requests

class B2BContentEngine:
    def __init__(self, hf_token=None):
        # We no longer need api_url or headers for local Ollama
        # The hf_token=None allows the code to run even if no token is passed
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

        # Pointing to your LOCAL laptop instead of the cloud
        url = "http://172.19.192.1:11434/api/generate"
        payload = {
            "model": "llama3.2:1b",
            "prompt": prompt,
            "stream": False  # This gives us the full text at once
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                return response.json().get('response', '').strip()
            else:
                return f"Ollama Error: {response.status_code}"
        except Exception as e:
            return "Is Ollama running? Start the app and try again."

    def audit_content(self, text, category):
        trend = self.sales_data.get(category.lower(), {})
        avoid = trend.get('avoid_words', '')
        issues = [f"B2B Audit: Remove '{w.strip()}'" for w in avoid.split(',') if w.strip() and w.strip().lower() in text.lower()]
        
        return {
            "status": "Approved" if not issues else "Needs Optimization",
            "feedback": issues
        }
import csv
import requests

class B2BContentEngine:
    def __init__(self, hf_token):
        # Professional API endpoint - avoids laptop lag
        self.api_url = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-125M"
        self.headers = {"Authorization": f"Bearer {hf_token}"}
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
        
        # B2B specific prompt engineering
        prompt = (f"Write a professional B2B product description focusing on {selling_point}. "
                  f"Product: {product_name}. Features: {features}. Description:")

        # Send to Hugging Face Cloud
        response = requests.post(self.api_url, headers=self.headers, json={"inputs": prompt})
        
        if response.status_code == 200:
            result = response.json()
            return result[0]['generated_text'].replace(prompt, "").strip()
        elif response.status_code == 503:
            return "Model is loading in the cloud... please try again in 30 seconds."
        else:
            return f"Error: {response.status_code}. Check your API token."

    def audit_content(self, text, category):
        trend = self.sales_data.get(category.lower(), {})
        avoid = trend.get('avoid_words', '')
        issues = [f"B2B Audit: Remove '{w.strip()}'" for w in avoid.split(',') if w.strip() and w.strip().lower() in text.lower()]
        
        return {
            "status": "Approved" if not issues else "Needs Optimization",
            "feedback": issues
        }
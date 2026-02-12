import csv
from transformers import pipeline

class B2BContentEngine:
    def __init__(self):
        self.generator = pipeline("text-generation", model="EleutherAI/gpt-neo-125M")
        self.sales_data = self.load_sales_trends()

    def load_sales_trends(self):
        trends = {}
        try:
            with open('sales_trends.csv', mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    trends[row['category']] = row
        except FileNotFoundError:
            print("Warning: sales_trends.csv not found.")
        return trends

    def generate_with_trends(self, product_name, category, features):
        # Fetch data-driven insight
        trend = self.sales_data.get(category.lower(), {})
        selling_point = trend.get('top_selling_point', 'general quality')
        preference = trend.get('consumer_preference', 'reliability')

        # Context Injection (The "GenAI" Flex)
        prompt = (f"B2B Strategy: Focus on {selling_point} because consumers prefer {preference}.\n"
                  f"Product: {product_name}\n"
                  f"Features: {features}\n"
                  f"Write a professional product description:")

        raw_output = self.generator(prompt, max_length=150, do_sample=True)[0]['generated_text']
        return raw_output.replace(prompt, "").strip()

    def audit_content(self, text, category):
        trend = self.sales_data.get(category.lower(), {})
        avoid = trend.get('avoid_words', '')
        
        issues = []
        if avoid and avoid in text.lower():
            issues.append(f"Trend Alert: Avoid '{avoid}' - users currently find it unappealing.")
        
        status = "Approved" if not issues else "Needs Optimization"
        return {"status": status, "feedback": issues}
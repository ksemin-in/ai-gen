from ai_engine import B2BContentEngine

def run_genai_project():
    engine = B2BContentEngine(hf_token=None)
    
    product = "Industrial Solar Panel v4"
    category = "energy"
    features = "High durability, 25-year warranty, 22% efficiency"

    print(f"\n--- Generating B2B Content for {product} ---")
    description = engine.generate_with_trends(product, category, features)
    print(f"AI Output: {description}")

    print("\n--- Running B2B Sales Trend Audit ---")
    audit = engine.audit_content(description, category)
    print(f"Status: {audit['status']}")
    for feedback in audit['feedback']:
        print(f"- {feedback}")

if __name__ == "__main__":
    run_genai_project()
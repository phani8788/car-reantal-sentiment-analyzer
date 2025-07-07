import cohere
import pandas as pd
import time
from collections import Counter
from dotenv import load_dotenv
import os

load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

df = pd.read_csv("C:\\Users\\phani_mhqmewb\\Downloads\\test_data.csv")
df["Predicted Sentiment"] = ""
df["Extracted Issues"] = ""

def analyze_review(review_text):
    review_text = str(review_text)
    if review_text.strip() == "" or review_text.lower() == "nan":
        return {"sentiment": "Unknown", "issues": "None", "service_feedback": "None"}

    prompt = f"""
You are a customer service feedback analyst for a car rental company.

Analyze this review:
"{review_text}"

Return:
1. Sentiment: Positive, Neutral, or Negative — especially regarding service.
2. Other Issues: Any other complaints or highlights, such as car quality, delivery, or billing? Use 'None' if not mentioned.

Format:
Sentiment: <Positive | Neutral | Negative>
Other Issues: <comma-separated list or 'None'>
"""

    try:
        response = co.generate(
            model="command-r-plus",
            prompt=prompt,
            max_tokens=200, 
            temperature=0.3,
        )
        reply = response.generations[0].text.strip()

        
        sentiment = "Unknown"
        issues = "None"
        for line in reply.splitlines():
            if "Sentiment:" in line:
                sentiment = line.split(":", 1)[1].strip()
            elif "Other Issues:" in line:
                issues = line.split(":", 1)[1].strip()

        return {"sentiment": sentiment, "issues": issues}
 
    except Exception as e:
        print(f"Error analyzing review '{review_text}': {e}")
        return {"sentiment": "Error", "issues": "None"}


for idx, row in df.iterrows():
    result = analyze_review(row["Customer_Service"])
    df.at[idx, "Predicted Sentiment"] = result["sentiment"]
    df.at[idx, "Extracted Issues"] = result["issues"]
    print(f"✅ Processed row {idx + 1}/{len(df)}: Sentiment = {result['sentiment']}, Issues = {result['issues']}")
    time.sleep(1.6)  # ~40 requests per minute


output_file = "car_rental_sentiment_cohere_analysis.csv"
df.to_csv(output_file, index=False)

print(f"\n✅ All done! Results saved to: {output_file}")


print("\nSummary Report:")
print("=" * 50)

sentiment_counts = df["Predicted Sentiment"].value_counts()
print("\nSentiment Distribution:")
for sentiment, count in sentiment_counts.items():
    print(f" - {sentiment}: {count}")


issues_list = df["Extracted Issues"].dropna().tolist()
flat_issues = []
for item in issues_list:
    if item.lower() != "none":
        flat_issues.extend([issue.strip().lower() for issue in item.split(",")])

issue_counts = Counter(flat_issues)
print("\nMost Common Other Issues (Top 5):")
if issue_counts:
    for issue, count in issue_counts.most_common(5):
        print(f" - {issue}: {count}")
else:
    print(" - No specific 'Other Issues' identified.")

# Car Rental Sentiment & Issue Analyzer

This project analyzes customer service reviews using Cohere's LLM to extract:
- 💬 Sentiment (Positive, Neutral, Negative)
- ⚠ Common issues (car condition, billing, delay, etc.)

---

## Features

- Prompt-based text analysis using `command-r-plus` model
- CSV input/output
- Automated summary report generation
- API key protected using `.env`

---

## Input Format

The input must be a `.csv` file named (or renamed as) `test_data.csv` with at least **one column**:

### Required Column:
| Column Name        | Description                             |
|--------------------|-----------------------------------------|
| `Customer_Service` | Text reviews written by customers about their experience |

### Example:
```csv
Customer_Service
"The car was late and the support team was rude."
"Great experience, friendly staff!"
"Billing was confusing, and the car was not clean."

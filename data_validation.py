import pandas as pd

REQUIRED_COLUMNS = [
    "1. Age", "2. Gender", "3. LGA/LCDA",
    "4. How often do you bathe or shower per day?",
    "5. Do you use any of the following regularly? (Tick all that apply)",
    "6. How often do you consume the following foods? (Tick those eaten regularly)",
    "7. Do you sweat excessively even when not active?",
    "8. Are you aware of any medical condition that may cause body odor (e.g., diabetes, thyroid disorder)?",
    "9. Do you have close relatives with persistent body odor?",
    "10. Have you ever been told you have body odor?",
    "11. If yes, how did it affect you emotionally?",
    "12. Has body odor ever affected your social life or self-confidence?",
    "13. Do you think body odor can cause social discrimination or stigmatization?",
    "14. Have you tried any of the following to reduce body odor? (Tick all that apply)",
    "15. Rate the effectiveness of your chosen remedies.",
    "16. Do you believe some people naturally have stronger body odor due to their body chemistry or genetics?",
    "17. Do you think body odor should be treated as a medical issue in some cases"
]

def validate_columns(df: pd.DataFrame) -> bool:
    """
    Validates that all required columns exist.

    Returns:
        True if valid, False if missing columns.
    """
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]

    if missing:
        print("❌ Missing columns:", missing)
        return False

    print("✔ All required columns present.")
    return True

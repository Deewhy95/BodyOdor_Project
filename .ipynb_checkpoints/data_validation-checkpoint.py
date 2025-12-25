import pandas as pd

REQUIRED_COLUMNS = [
    "1. Age", "2. Gender", "3. LGA/LCDA",
    "4. How often do you bathe or shower per day?",
    "5. Do you use any of the following regularly? (Tick all that apply)",
    "6. How often do you consume the following foods? (Tick those eaten regularly)",
    "7. Do you sweat excessively even when not active?",
    "10. Have you ever been told you have body odor?",
    "14. Have you tried any of the following to reduce body odor? (Tick all that apply)",
    "15. Rate the effectiveness of your chosen remedies."
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

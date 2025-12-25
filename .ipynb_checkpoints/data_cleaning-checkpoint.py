import pandas as pd

valid_lgas = [
    "Agbado/Oke-Odo", "Epe", "Ikeja", "Odi Olowo/Ojuwoye", "Agboyi/Ketu", "Eredo", 
    "Ikorodu North", "Ojo", "Agege", "Eti Osa East", "Ikorodu West", "Ojodu", "Ajeromi",
    "Eti Osa West", "Ikosi", "Ejinrin", "Ojokoro", "Alimosho", "Iba", "Ikorodu", 
    "Olorunda", "Apapa", "Isolo", "Iru/Victoria Island", "Onigbongbo", "Apapa-Iganmu", 
    "Imota", "Itire Ikate", "Oriade", "Ayobo/Ipaja", "Ikoyi-Obalende", "Kosofe",
    "Orile Agege", "Badagry West", "Ibeju", "Lagos West", "Oshodi", "Badagry",
    "Ifako Ijaiye", "Lagos East", "Oto-Awori", "Bariga", "Ifelodun", "Lagos Mainland",
    "Shomolu", "Coker", "Aguda", "Igando/Ikotun", "Lekki", "Surulere", "Egbe Idimu",
    "Igbogbo/Bayeku", "Mosan/Okunola", "Yaba", "Ejigbo", "Ijede", "Mushin", 
    "Ajeromi-Ifelodun", "Amuwo-Odofin", "Lagos Island", "Oshodi-Isolo"
]

age_group_order =[
    "18-24 years",
    "25-34 years",
    "35-44 years",
    "45-54 years",
    "55-64 years",
    "65 & above"
]

def clean_age_group(series):
    """
    Cleans and locks Age into ordered categorical groups.
    Any unexpected value is set to 'Unknown'.
    """
    series = series.astype(str).str.strip()

    series = series.where(series.isin(age_group_order), "Unknown")

    return pd.Categorical(
        series,
        categories=age_group_order,
        ordered=True
    )

def clean_multi_select(series: pd.Series):
    """
    Splits comma-separated multi-select answers into lists.
    """
    return series.apply(lambda x: [i.strip() for i in x.split(",")] if isinstance(x, str) else [])

def clean_binary(series: pd.Series):
    """
    Converts Yes/No/Not sure to numeric values.
    """
    mapping = {"Yes": 1, "No": 0, "Not sure": None}
    return series.map(mapping)

def standardize_lga(value: str):
    """
    Cleans and standardizes LGA names by:
    - Removing leading/trailing spaces
    - Normalizing spacing
    - Converting known variants to official versions
    """

    if not isinstance(value, str):
        return "others"

    # Step 1: strip spaces + remove double spaces
    value = value.strip().replace("  ", " ")

    # Step 2: unify separators (for things like 'Oshodi Isolo")
    value = value.replace(" - ", "-").replace("- ", "-")
    value = value.replace("/", "/") # ensure consistent slash
    value = value.replace(" ", " ") # single space normalization

    # Step 3: map known variants → official values
    replacement_map = {
        "Oshodi Isolo": "Oshodi-Isolo",
        "Oshodi Isolo ": "Oshodi-Isolo",
        "Alimosho ": "Alimosho",
        "Surulere ": "Surulere",
        "Shomolu ": "Shomolu",
        "Kosofe ": "Kosofe",
        "Badagry ": "Badagry",
        "Ibeju Lekki": "Ibeju",
        "Ikosi Isheri": "Ikosi",
        "Ikorodu ": "Ikorodu",
        "Ajeromi ": "Ajeromi",
        "Lagos Island ": "Lagos Island",
        "Ketu": "Agboyi/Ketu",   # interpret Ketu correctly
        "Eti-Osa": "Eti Osa East",  # safe default
        "Ajah": "Eti Osa East",
        "Akoka": "Yaba",
        "Ebute Metta": "Yaba",
    }

    if value in replacement_map:
        return replacement_map[value]

    return value
    
""" def validate_lga(df, valid_lgas):
    
    Clean, standardize, and validate the LGA column. If any values are not in the valid list,
    raise an error and list the invalid entries.
    
    df["LGA/LCDA"] = df["3. LGA/LCDA"].apply(standardize_lga)

    df["LGA/LCDA"] = df["LGA/LCDA"].apply(lambda x: x if x in valid_lgas else "Others")

    invalid_count = (df["LGA/LCDA"] == "Others").sum()

    summary = {
        "total_rows": len(df),
        "invalid_lga_rows": invalid_count,
        "valid_rows": len(df) - invalid_count,
        "percent_invalid": round((invalid_count / len(df)) * 100, 2)
    }
    
    return df, summary
    """
def validate_lga(df, valid_lgas):
    """
    Standardizes and validates the LGA column. Invalid LGA entries are dropped from the dataframe.
    Returns a summary dictionary with total rows,  valid rows, and the percentage of invalid rows.
    """
    df["LGA/LCDA"] = df["3. LGA/LCDA"].apply(standardize_lga)
    df["LGA/LCDA"] = df["LGA/LCDA"].apply(lambda x: x if x in valid_lgas else "Others")
    invalid_count = (df["LGA/LCDA"] == "Others").sum()
    df = df[df["LGA/LCDA"] != "Others"]
    summary = {
        "total_rows": len(df),
        "valid_rows": len(df),
        "percent_invalid": round((invalid_count / len(df)) * 100, 2) if len(df) > 0 else 0
    }
    return df, summary
    
def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()
    """
    Full data cleaning pipeline, including LGA cleaning + validation.
    """
    #Age cleaning
    df["Age_Group"] = clean_age_group(df["1. Age"])
    
    # Clean + validate LGA
    df, lga_summary = validate_lga(df, valid_lgas)

    print("\n LGA Cleaning Summary:")
    print(lga_summary)

    
    # Split multi-select fields
    df.loc[:, "Foods"] = clean_multi_select(df["6. How often do you consume the following foods? (Tick those eaten regularly)"])
    df.loc[:, "Hygiene"] = clean_multi_select(df["5. Do you use any of the following regularly? (Tick all that apply)"])
    df.loc[:, "Remedies"] = clean_multi_select(df["14. Have you tried any of the following to reduce body odor? (Tick all that apply)"])

    # Convert Yes/No columns to numeric
    df.loc[:, "Excessive Sweating"] = clean_binary(df["7. Do you sweat excessively even when not active?"])
    df.loc[:, "Told_BO"] = clean_binary(df["10. Have you ever been told you have body odor?"])

    return df
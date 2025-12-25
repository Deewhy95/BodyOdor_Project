import pandas as pd

def load_data(file_path: str) -> pd.DataFrame:
    """
    Loads dataset from CSV, TXT, or TSV file formats.
    
    Args:
        file_path (str): Path to the dataset.

    Returns:
        pd.DataFrame: Loaded dataframe.
    """
    try:
        if file_path.endswith(".csv"):
            return pd.read_csv(file_path)

        elif file_path.endswith(".txt") or file_path.endswith(".tsv"):
            return pd.read_csv(file_path, sep="\t")

        else:
            raise ValueError("Unsupported file format")

    except Exception as e:
        print("ERROR loading data →", e)
        raise e

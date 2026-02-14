"""
File contains implementation of tools for the Agentic POC.
"""

import pandas as pd

from typing import List, Dict

DATA_FILE = "data/data.csv"

df = pd.read_csv(DATA_FILE)

def get_targets(cancer_name: str) -> List[str]:
    """
    Retrieves the list of gene targets associated with a specific cancer type.

    Args:
        cancer_name (str): The name of the cancer indication (e.g., 'lung').

    Returns:
        List[str]: A list of gene symbols associated with the cancer.
    """
    return df[df['cancer_indication'] == cancer_name]['gene'].tolist()

def get_expressions(genes: List[str]) -> Dict[str, float]:
    """
    Retrieves the median expression values for a given list of genes.

    Args:
        genes (List[str]): A list of gene symbols to retrieve values for.

    Returns:
        Dict[str, float]: A dictionary mapping gene symbols to their median expression values.
    """
    subset = df[df['gene'].isin(genes)]
    return dict(zip(subset['gene'], subset['median_value']))

def get_all_cancers() -> List[str]:
    """
    Retrieves a list of all unique cancer types present in the dataset.

    Returns:
        List[str]: A list of unique cancer indication strings.
    """
    return df['cancer_indication'].unique().tolist()

if __name__ == "__main__":
    cancer = "lung"
    targets = get_targets(cancer)
    expressions = get_expressions(targets)
    print(f"{cancer} targets:", targets)
    print(f"Expression values:", expressions)
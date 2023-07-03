import pandas as pd
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

def save_to_excel(df, output_path):
    try:
        df.to_excel(output_path, index=False)
    except Exception as e:
        logger.exception(f"Error saving DataFrame to Excel: {str(e)}")

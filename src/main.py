import os
import pandas as pd
from src.utils import pdf_utils, excel_utils
from src.utils.logger import setup_logger
from src.utils.exception import CustomException

# Set up logger
logger = setup_logger(__name__)

# Folder path containing PDF files
folder_path = ".src/data"

# Initialize an empty list to store ticket details from all PDF files
all_ticket_details = []

# Iterate over the PDF files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".pdf"):
        try:
            # Load the PDF file
            pdf_path = os.path.join(folder_path, filename)

            # Extract ticket details
            ticket_info = pdf_utils.extract_info(pdf_path)

            # Extract passenger details
            passenger_details = pdf_utils.extract_passenger_details(pdf_path)

            # Create DataFrame for ticket details
            ticket_df = pd.DataFrame([ticket_info])

            if passenger_details:
                # Create DataFrame for passenger details
                passenger_df = pd.DataFrame(passenger_details)

                # Duplicate ticket details to match the number of passengers
                ticket_df = pd.concat([ticket_df] * len(passenger_df), ignore_index=True)

                # Combine ticket and passenger details into a single DataFrame
                combined_df = pd.concat([ticket_df, passenger_df], axis=1)

                # Append ticket details to the list
                all_ticket_details.append(combined_df)
        except Exception as e:
            logger.exception(f"Error processing file '{filename}': {str(e)}")

# Combine ticket details from all PDF files into a single DataFrame
all_ticket_details_df = pd.concat(all_ticket_details, ignore_index=True)

# Save the combined DataFrame to an Excel file
output_folder = "./output"
os.makedirs(output_folder, exist_ok=True)
output_path = os.path.join(output_folder, "Ticket_Details.xlsx")
excel_utils.save_to_excel(all_ticket_details_df, output_path)

logger.info("Excel file saved successfully!")

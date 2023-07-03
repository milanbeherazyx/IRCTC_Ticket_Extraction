import re
from PyPDF2 import PdfReader
from src.utils.logger import setup_logger
from src.utils.exception import CustomException

logger = setup_logger(__name__)

def extract_info_from_text(pattern, text):
    return match[1] if (match := re.search(pattern, text)) else ""

def extract_info(pdf_path):
    try:
        pdf = PdfReader(pdf_path)

        # Extract the text data from the first page
        page = pdf.pages[0]
        extracted_text = page.extract_text()

        # Extract ticket details
        ticket_info = {
            "PNR": extract_info_from_text(r"PNR No\. : (\d+)", extracted_text),
            "Train Number": extract_info_from_text(
                r"Train No\. / Name : (\d+) / (.+)", extracted_text
            ),
            "Train Name": extract_info_from_text(
                r"Train No\. \/ Name : \d+ \/ (.+?) Quota", extracted_text
            ),
            "Quota": extract_info_from_text(r"Quota : (.+)", extracted_text),
            "Transaction ID": extract_info_from_text(
                r"Transaction ID : (\d+)", extracted_text
            ),
            "Date of Booking": extract_info_from_text(
                r'Date & T ime of Booking : (\d{2}-[A-Za-z]{3}-\d{4})',
                extracted_text,
            ),
            "Class": extract_info_from_text(r"Class : (.+)", extracted_text),
            "From": re.search(r"From : (.*?) \(.*?\)", extracted_text)[1],
            "Date of Journey": extract_info_from_text(
                r"Date of Journey : (\d+-[A-Za-z]+-\d+)", extracted_text
            ),
            "To": re.search(r"To : (.*?) \(.*?\)", extracted_text)[1],
            "Boarding At": extract_info_from_text(
                r"Boarding At : (.+)", extracted_text
            ).split(" ")[0],
            "Scheduled Departure": extract_info_from_text(
                r"Scheduled Departure\* : (\d+-[A-Za-z]+-\d+ \d+:\d+)",
                extracted_text,
            ),
            "Reservation Up to": extract_info_from_text(
                r"Reservation Up to : (.+)", extracted_text
            ).split(" Scheduled Arrival")[0],
            "Scheduled Arrival": extract_info_from_text(
                r"Scheduled Arrival : (\d+-[A-Za-z]+-\d+ \d+:\d+)",
                extracted_text,
            ),
            "Adult": extract_info_from_text(r"Adult:  (\d+)", extracted_text),
            "Child": extract_info_from_text(r"Child:  (\d+)", extracted_text),
            "Passenger Mobile No": extract_info_from_text(
                r"Passenger Mobile No : (.+)", extracted_text
            ).split(" Distance")[0],
            "Distance": extract_info_from_text(
                r"Distance : (\d+)KM", extracted_text
            ),
            "Insurance (No. of Psng)": extract_info_from_text(
                r"Insurance \(No\. of Psng\) : (\d+)", extracted_text
            ),
        }

        # Extract fare details
        fare_match = re.findall(r"\d+\.\d+", extracted_text)
        total_fare = max(fare_match, key=float) if fare_match else ""
        ticket_info["Total Fare"] = total_fare

        return ticket_info

    except Exception as e:
        logger.error(f"PDF extraction error: {e}")
        raise CustomException("Error occurred during PDF extraction") from e


def extract_passenger_details(pdf_path):
    try:
        pdf = PdfReader(pdf_path)

        # Extract the text data from the second page
        page = pdf.pages[1]
        extracted_text = page.extract_text()

        # Extract passenger details
        passenger_details = re.findall(r"\d+\..+?\d+", extracted_text)
        passenger_details = [re.split(r"\s{2,}", details) for details in passenger_details]
        passenger_details = [
            {
                "Passenger No": details[0],
                "Passenger Name": details[1],
                "Booking Status": details[2],
                "Current Status": details[3],
            }
            for details in passenger_details
        ]

        return passenger_details

    except Exception as e:
        logger.error(f"PDF extraction error: {e}")
        raise CustomException("Error occurred during PDF extraction") from e

import os
import requests
import pdfplumber
from pdf2image import convert_from_path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to download a PDF from a URL
def download_pdf(url, filename):
    try:
        response = requests.get(url)
        with open(filename, 'wb') as file:
            file.write(response.content)
        logging.info(f"Downloaded: {filename}")
    except Exception as e:
        logging.error(f"Failed to download {url}: {e}")

# Function to extract text using pdfplumber
def extract_text_with_pdfplumber(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            logging.info(f"Extracting text using pdfplumber from {pdf_path}, {len(pdf.pages)} pages found.")
            for page_num, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                else:
                    logging.warning(f"Page {page_num + 1} had no text.")
                logging.info(f"Extracted text from page {page_num + 1}")
        return text.strip()
    except Exception as e:
        logging.error(f"Error extracting text with pdfplumber: {e}")
        return ""

# Function to save pages with formulas or complex diagrams as images
def save_page_as_image(pdf_path):
    try:
        images = convert_from_path(pdf_path)
        for i, image in enumerate(images):
            image_path = f"{os.path.splitext(pdf_path)[0]}_page_{i + 1}.png"
            image.save(image_path, 'PNG')
            logging.info(f"Saved page {i + 1} as image: {image_path}")
    except Exception as e:
        logging.error(f"Error saving pages as images: {e}")

# Main function to handle both download and extraction
def convert_pdf_to_text(url, output_filename):
    pdf_filename = output_filename + ".pdf"

    # Download PDF from URL
    download_pdf(url, pdf_filename)

    # Extract text using pdfplumber
    logging.info(f"Extracting text from {pdf_filename} using pdfplumber...")
    extracted_text = extract_text_with_pdfplumber(pdf_filename)

    # If no text was extracted, save pages as images for manual review
    if not extracted_text:
        logging.error(f"No text could be extracted from {pdf_filename}. Saving pages as images.")
        save_page_as_image(pdf_filename)
    else:
        # Save the extracted text to a file
        output_txt_filename = output_filename + ".txt"
        with open(output_txt_filename, 'w', encoding='utf-8') as text_file:
            text_file.write(extracted_text)
        logging.info(f"Text extracted and saved to '{output_txt_filename}'")

if __name__ == "__main__":
    # List of URLs and their corresponding output filenames
    pdfs = {
        "https://www.issdc.gov.in/docs/as1/AstroSat_Payloads.pdf": "AstroSat Payloads",
        "https://www.issdc.gov.in/docs/as1/AstroSat-Handbook-v1.10.pdf": "AstroSat Handbook",
        "https://www.issdc.gov.in/docs/ch1/chandrayaan1_payload.pdf": "Chandrayaan 1 Payload",
        "https://www.issdc.gov.in/docs/ch2/chandrayaan2_payload.pdf": "Chandrayaan 2 Payload",
        "https://ftp.idu.ac.id/wp-content/uploads/ebook/tdg/DESIGN%20SISTEM%20DAYA%20GERAK/Rocket%20Propulsion%20Elements%20by%20George%20P.%20Sutton.pdf": "Rocket Propulsion Elements",
        "https://library.sciencemadness.org/library/books/ignition.pdf": "Ignition Book",
        "https://www.hlevkin.com/hlevkin/90MathPhysBioBooks/Mechanics/Curtis_OrbitamMechForEngineeringStudents.pdf": "Orbital Mechanics for Engineering Students",
        "https://ntrs.nasa.gov/api/citations/19710019929/downloads/19710019929.pdf": "Design_of_liquid_prop_engine"
    }

    # Iterate through all URLs and extract text
    for url, output_filename in pdfs.items():
        convert_pdf_to_text(url, output_filename)

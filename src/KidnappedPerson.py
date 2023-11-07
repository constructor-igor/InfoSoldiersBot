import os
import random
from PyPDF2 import PdfReader, PdfWriter


class KidnappedPerson():
    def __init__(self, full_source_pdf_file, data_folder_path):
        self.full_source_pdf_file = full_source_pdf_file
        self.data_folder_path = data_folder_path
        pdf_reader = PdfReader(self.full_source_pdf_file)
        self.total_count = len(pdf_reader.pages)
    def get_total_pages_number(self):
        return self.total_count
    def get_page(self, page_number, target_file_path):
        pdf_reader = PdfReader(self.full_source_pdf_file)

        # Check if the page number is within the valid range
        if 1 <= page_number <= len(pdf_reader.pages):
            pdf_writer = PdfWriter()
            page = pdf_reader.pages[page_number - 1]  # Pages are 0-indexed
            pdf_writer.add_page(page)
            with open(target_file_path, 'wb') as output_file:
                pdf_writer.write(output_file)
    def get_random(self):
        random_number = random.randint(1, self.total_count)
        target_file = os.path.join(self.data_folder_path + f"{random_number:03}.pdf")
        self.get_page(random_number, target_file)
        return target_file

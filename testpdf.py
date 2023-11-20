import PyPDF2
import tkinter as tk
from tkinter import filedialog

def extract_text_from_pdf(pdf_file_path):
    try:
        with open(pdf_file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            text = ''
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
            
            return text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def select_pdf_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.askopenfilename(
        title="Select PDF File",
        filetypes=[("PDF Files", "*.pdf")])

    if file_path:
        pdf_text = extract_text_from_pdf(file_path)
        if pdf_text:
            print(pdf_text)
        else:
            print("Failed to extract text from the PDF.")
    else:
        print("No file selected.")

if __name__ == "__main__":
    select_pdf_file()

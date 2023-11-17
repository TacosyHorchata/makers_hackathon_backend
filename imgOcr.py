from pdf2image import convert_from_path
from PIL import Image
import pytesseract

pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def convert_pdf_to_img(pdf_file):
    return convert_from_path(pdf_file)


def convert_image_to_text(file):   
    text = pytesseract.image_to_string(file)
    return text


def get_text_from_any_pdf(pdf_file):
    images = convert_pdf_to_img(pdf_file)
    final_text = ""
    for pg, img in enumerate(images):
        
        final_text += convert_image_to_text(img)
        #print("Page n°{}".format(pg))
        #print(convert_image_to_text(img))
    
    return final_text

path_to_pdf = './prueba.pdf'

print(get_text_from_any_pdf(path_to_pdf))
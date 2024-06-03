import fitz  # PyMuPDF
import os
import io
from PIL import Image
import pandas as pd
from trans import translate
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import date

def extract_text_and_elements(pdf_path, output_dir):
    # Open the PDF file
    doc = fitz.open(pdf_path)

    # Prepare directories for saving text, images, and tables
    text_dir = os.path.join(output_dir, "text")
    image_dir = os.path.join(output_dir, "images")
    table_dir = os.path.join(output_dir, "tables")

    os.makedirs(text_dir, exist_ok=True)
    os.makedirs(image_dir, exist_ok=True)
    os.makedirs(table_dir, exist_ok=True)

    text_paths = []

    # Loop through each page in the PDF
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text")
        blocks = page.get_text("dict")["blocks"]

        # Save text
        text_path = os.path.join(text_dir, f"page_{page_num+1}.txt")
        with open(text_path, "w", encoding="utf-8") as text_file:
            text_file.write(text)
        text_paths.append(text_path)

        # Extract images and tables from blocks
        for block in blocks:
            if block["type"] == 1:  # Image block
                for img in block["images"]:
                    xref = img["xref"]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    img_ext = base_image["ext"]
                    img = Image.open(io.BytesIO(image_bytes))
                    img.save(os.path.join(image_dir, f"page_{page_num+1}_img_{xref}.{img_ext}"))

            elif block["type"] == 0 and "lines" in block:  # Text block
                for line in block["lines"]:
                    spans = line["spans"]
                    for span in spans:
                        if span["flags"] == 4:  # This might indicate a table, but needs refining
                            table_text = span["text"]
                            table_df = pd.DataFrame([x.split() for x in table_text.split("\n")])
                            table_df.to_csv(os.path.join(table_dir, f"page_{page_num+1}_table_{span['bbox']}.csv"), index=False)

    return text_paths, image_dir, table_dir

def translate_and_reconstruct(pdf_path, output_dir, target_language='ko'):
    text_paths, image_dir, table_dir = extract_text_and_elements(pdf_path, output_dir)
    
    translated_texts = []
    for text_path in text_paths:
        with open(text_path, "r", encoding="utf-8") as file:
            text = file.read()
        translated_text = translate(text, to_language=target_language)
        translated_texts.append(translated_text)

    reconstructed_pdf_path = os.path.join(output_dir, "translated_document.pdf")
    c = canvas.Canvas(reconstructed_pdf_path, pagesize=letter)
    width, height = letter

    for page_num, translated_text in enumerate(translated_texts):
        c.drawString(30, height - 30, f"Page {page_num+1}")
        text_object = c.beginText(30, height - 50)
        text_object.setFont("Helvetica", 12)
        text_object.setTextOrigin(30, height - 50)
        text_object.textLines(translated_text)
        c.drawText(text_object)
        c.showPage()

    c.save()
    print(f"Translated and reconstructed PDF saved at {reconstructed_pdf_path}")

if __name__ == "__main__":
    # import argparse

    # parser = argparse.ArgumentParser(description="Extract, translate, and reconstruct PDF.")
    # parser.add_argument("--pdf_path", type=str, required=True, help="Path to the PDF file")
    # parser.add_argument("--output_dir", type=str, required=True, help="Directory to save the extracted contents")
    # parser.add_argument("--target_language", type=str, default="en", help="Target language for translation")
    # args = parser.parse_args()
    # print(args)

    # translate_and_reconstruct(args.pdf_path, args.output_dir, args.target_language)
    pdf_path=r"C:\Users\qkrwo\Documents\Digital\JPark\gpt_serviece_for_engineer\icon\KOWHS,October.23-24,Seoul.pdf"
    output_dir=r"C:\Users\qkrwo\Documents\Digital\JPark\gpt_serviece_for_engineer\icon"
    target_language="ko"
    translate_and_reconstruct(pdf_path,output_dir,target_language)

    #python pdf_extraction.py --pdf_path /path/to/your/pdf/file.pdf --output_dir /path/to/output/directory --target_language en
    #python C:\Users\qkrwo\Documents\Digital\JPark\gpt_serviece_for_engineer\gpt_servieces\pdf_extraction.py --pdf_path "C:\Users\qkrwo\Documents\Digital\JPark\gpt_serviece_for_engineer\icon\KOWHS,October.23-24,Seoul.pdf" --output_dir "C:\Users\qkrwo\Documents\Digital\JPark\gpt_serviece_for_engineer\icon" --target_language kr


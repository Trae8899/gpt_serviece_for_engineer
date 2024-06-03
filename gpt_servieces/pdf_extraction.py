import fitz  # PyMuPDF
import os
import io
from PIL import Image
import pandas as pd
from trans import translate
from reportlab.lib.pagesizes import A4, A3
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
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
    table_data = {}

    # Loop through each page in the PDF
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text")
        # blocks = page.get_text("dict")["blocks"]

        # Save text
        text_path = os.path.join(text_dir, f"page_{page_num+1}.txt")
        with open(text_path, "w", encoding="utf-8") as text_file:
            text_file.write(text)
        text_paths.append(text_path)

        # Extract images
        for img in page.get_images():
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            img_ext = base_image["ext"]
            img = Image.open(io.BytesIO(image_bytes))
            img.save(os.path.join(image_dir, f"page_{page_num+1}_img_{xref}.{img_ext}"))

        # Extract tables
        tables = page.find_tables()
        for table_num, table in enumerate(tables):
            table_data_path = os.path.join(table_dir, f"page_{page_num+1}_table_{table_num+1}.csv")
            table_data_df = table.to_pandas()
            table_data_df.to_csv(table_data_path, index=False)
            
            if page_num + 1 not in table_data:
                table_data[page_num + 1] = []
            table_data[page_num + 1].append(table_data_path)
    
    return text_paths, image_dir, table_data

def draw_wrapped_text(canvas_obj, text, x, y, max_width, font_name, font_size):
    lines = text.split('\n')
    text_object = canvas_obj.beginText(x, y)
    text_object.setFont(font_name, font_size)
    
    for line in lines:
        while line:
            if text_object.getX() + canvas_obj.stringWidth(line, font_name, font_size) < max_width:
                text_object.textLine(line)
                break
            else:
                for i in range(len(line)):
                    if text_object.getX() + canvas_obj.stringWidth(line[:i], font_name, font_size) >= max_width:
                        text_object.textLine(line[:i])
                        line = line[i:]
                        break
    
    canvas_obj.drawText(text_object)

def translate_and_reconstruct(pdf_path, output_dir, target_language='ko'):
    text_paths, image_dir, table_data = extract_text_and_elements(pdf_path, output_dir)
    
    translated_texts = []
    for text_path in text_paths:
        with open(text_path, "r", encoding="utf-8") as file:
            text = file.read()
        translated_text = translate(text, to_language=target_language)
        translated_texts.append(translated_text)

    reconstructed_pdf_path = os.path.join(output_dir, "translated_document.pdf")
    pagesize=A3

    c = canvas.Canvas(reconstructed_pdf_path, pagesize=pagesize)
    width, height = pagesize

    # Register a font that supports Korean characters
    font_path = r"C:\Users\qkrwo\Documents\Digital\JPark\gpt_serviece_for_engineer\icon\NotoSansKR-VariableFont_wght.ttf"
    pdfmetrics.registerFont(TTFont('NotoSansCJK', font_path))

    for page_num, translated_text in enumerate(translated_texts):
        c.setFont("NotoSansCJK", 12)
        c.drawString(30, height - 30, f"Page {page_num+1}")

        # Draw wrapped text
        draw_wrapped_text(c, translated_text, 30, height - 50, width - 60, "NotoSansCJK", 12)

        # Add images to the PDF
        image_files = sorted([f for f in os.listdir(image_dir) if f.startswith(f"page_{page_num+1}_img_")])
        y_position = height - 300  # Adjusted y_position
        for image_file in image_files:
            img_path = os.path.join(image_dir, image_file)
            img = Image.open(img_path)
            img_width, img_height = img.size
            aspect_ratio = img_width / img_height
            img_reader = ImageReader(img)
            if y_position - (img_height / aspect_ratio) < 50:
                c.showPage()
                y_position = height - 50
                c.drawString(30, height - 30, f"Page {page_num+1} (cont.)")
            c.drawImage(img_reader, 30, y_position - (img_height / aspect_ratio), width=img_width / aspect_ratio, height=img_height)
            y_position -= (img_height / aspect_ratio) + 10
        
        # Add tables to the PDF
        if page_num + 1 in table_data:
            for table_path in table_data[page_num + 1]:
                table_df = pd.read_csv(table_path)
                data = table_df.values.tolist()
                x = 30
                y = y_position - 20
                for row in data:
                    if y < 40:  # Prevents writing outside the page
                        c.showPage()
                        y = height - 30
                        c.drawString(x, y, f"Page {page_num+1} (cont.)")
                        y -= 20
                    c.drawString(x, y, " | ".join(map(str, row)))
                    y -= 15

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
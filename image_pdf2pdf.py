from PIL import Image
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
import tempfile

PAGE_WIDTH, PAGE_HEIGHT = A4
DPI = 300  # High print quality


def image_to_high_quality_pdf(image_path, output_pdf):
    img = Image.open(image_path).convert("RGB")

    img_width, img_height = img.size
    img_ratio = img_width / img_height
    page_ratio = PAGE_WIDTH / PAGE_HEIGHT

    if img_ratio > page_ratio:
        new_width = PAGE_WIDTH
        new_height = PAGE_WIDTH / img_ratio
    else:
        new_height = PAGE_HEIGHT
        new_width = PAGE_HEIGHT * img_ratio

    x = (PAGE_WIDTH - new_width) / 2
    y = (PAGE_HEIGHT - new_height) / 2

    c = canvas.Canvas(output_pdf, pagesize=A4, pageCompression=0)  # ❌ no compression
    c.setPageSize(A4)
    c.drawImage(
        image_path,
        x, y,
        new_width, new_height,
        preserveAspectRatio=True,
        mask='auto'
    )
    c.showPage()
    c.save()


def images_and_pdfs_to_pdf(input_folder, output_pdf):
    writer = PdfWriter()
    writer.compress_content_streams = False  # ❌ disable PDF compression
    temp_pdfs = []

    for file in sorted(os.listdir(input_folder)):
        path = os.path.join(input_folder, file)

        # PDFs → keep original pages (no scaling)
        if file.lower().endswith(".pdf"):
            reader = PdfReader(path)
            for page in reader.pages:
                writer.add_page(page)

        # Images → convert at high quality
        elif file.lower().endswith((".jpg", ".jpeg", ".png")):
            temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            image_to_high_quality_pdf(path, temp_pdf.name)
            temp_pdfs.append(temp_pdf.name)

            reader = PdfReader(temp_pdf.name)
            writer.add_page(reader.pages[0])

    with open(output_pdf, "wb") as f:
        writer.write(f)

    for tmp in temp_pdfs:
        os.remove(tmp)

    print("✅ High-quality PDF created (minimal loss)")


images_and_pdfs_to_pdf("docs_images", "output_pdf.pdf")

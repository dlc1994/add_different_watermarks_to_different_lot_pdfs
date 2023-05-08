from pathlib import Path
from typing import Union, Literal, List

from pypdf import PdfWriter, PdfReader, Transformation
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
import csv
import sys

def makeWatermark(text, output_file_name, font="Helvetica", font_size=50, alpha_degree=0.25, rotate=45, delta_x=200, delta_y=100):
    pdf = canvas.Canvas(output_file_name, pagesize=A4)
    pdf.translate(inch, inch)
    pdf.setFillColor(colors.grey, alpha=alpha_degree)
    pdf.setFont(font, font_size)
    pdf.rotate(rotate)
    # A4 is 210 * 297
    for i in range(0, 2100, delta_x):
        for j in range(0, 2970, delta_y):
            pdf.drawCentredString(i, j, text)
    pdf.save()

def dowatermark(
    content_pdf: Path,
    stamp_pdf: Path,
    pdf_result: Path,
    page_indices: Union[Literal["ALL"], List[int]] = "ALL",):
    reader = PdfReader(content_pdf)
    if page_indices == "ALL":
        page_indices = range(len(reader.pages))

    writer = PdfWriter()
    watermark_page = PdfReader(stamp_pdf).pages[0]
    for index in page_indices:
        content_page = reader.pages[index]
        content_page.merge_transformed_page(
            watermark_page,
            Transformation(),
        )
        writer.add_page(content_page)

    with open(pdf_result, "wb") as fp:
        writer.write(fp)

def read_csv(file_path):
    watermarks = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            watermarks.append(str(row['title']))
    return watermarks

if __name__ == "__main__":
    print("hello, someone")
    print(sys.argv[1:])
    input_name = sys.argv[1:][0]
    font_name = sys.argv[1:][1]
    font_size = float(sys.argv[1:][2])
    alpha_degree = float(sys.argv[1:][3])
    rotate = float(sys.argv[1:][4])
    delta_x =  int(sys.argv[1:][5])
    delta_y =  int(sys.argv[1:][6])
    watermarks = read_csv("./test.csv")
    print("Support fonts: ", canvas.Canvas(None).getAvailableFonts())
    for watermark in watermarks:
        tmp = "./" + watermark + ".pdf"
        print("processing... ", tmp)
        makeWatermark(watermark, "./tmp.pdf", font_name, font_size, alpha_degree, rotate, delta_x, delta_y)
        dowatermark("./" + input_name + ".pdf", "./tmp.pdf", tmp)

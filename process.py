import io
import re
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfWriter, PdfReader

if __name__ == "__main__":
    # VARIABLES
    input_pdf = "template_.pdf"
    input_csv = "data.csv"
    output_pdf = "result.pdf"

    # READ DATA
    data_df = pd.read_csv(input_csv, sep=";", dtype = {"Pin filtered": str, "N Tarjeta 2": str})

    # read your existing PDF
    existing_pdf = PdfReader(open(input_pdf, "rb"))

    output = PdfWriter()

    for idx, page in enumerate(existing_pdf.pages):
        if idx % 10 == 0:
            print(f"Doing page {idx}/{len(existing_pdf.pages)}")
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.drawString(230, 252, re.sub(r"VUELTA\-",
                                        "",
                                        re.sub(r"\'",
                                               "",
                                               data_df["MATRICULA"][idx])))
        can.drawString(150, 232, data_df["N Tarjeta 2"][idx])
        can.drawString(70, 212, data_df["Pin filtered"][idx])
        can.save()
        
        #move to the beginning of the StringIO buffer
        packet.seek(0)
    
        # create a new PDF with Reportlab
        new_pdf = PdfReader(packet)
        page.merge_page(new_pdf.pages[0])
    
        output.add_page(page)

    output_stream = open(output_pdf, "wb")
    output.write(output_stream)
    output_stream.close()

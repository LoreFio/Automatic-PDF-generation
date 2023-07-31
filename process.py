import io
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfFileWriter, PdfFileReader

# VARIABLES
input_pdf = "template_.pdf"
input_csv = "data.csv"
output_pdf = "result.pdf"

# READ DATA
data_df = pd.read_csv(input_csv)

# READ DATA
packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)
can.drawString(10, 100, "Hello world")
can.save()

#move to the beginning of the StringIO buffer
packet.seek(0)

# create a new PDF with Reportlab
new_pdf = PdfFileReader(packet)
# read your existing PDF
existing_pdf = PdfFileReader(open("original.pdf", "rb"))
output = PdfFileWriter()
# add the "watermark" (which is the new pdf) on the existing page
page = existing_pdf.pages[0]
page.merge_page(new_pdf.pages[0])
output.add_page(page)
# finally, write "output" to a real file
output_stream = open("destination.pdf", "wb")
output.write(output_stream)
output_stream.close()

"""
for idx, page in enumerate(existing_pdf.pages):
	packet = io.BytesIO()
	can = canvas.Canvas(packet, pagesize=letter)
	can.drawString(10, 100, "Hello world")
	can.save()
	
	#move to the beginning of the StringIO buffer
	packet.seek(0)

	# create a new PDF with Reportlab
	new_pdf = PdfFileReader(packet)
	page.merge_page(new_pdf.pages[0])

	output.add_page(page)
"""

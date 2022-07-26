from fpdf import FPDF
import csv


class PDFCreator:
    def __init__(self, title: str, paragraph: str, font="Helvetica", font_size=14, csv_path=None):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_margins(5, 5)
        pdf.set_font(font, 'B', font_size * 3)
        cell_width = 200
        pdf.cell(cell_width, font_size, txt=title,
                 ln=1, align='C')
        pdf.ln()
        pdf.set_font(font, '', font_size)
        pdf.cell(cell_width, font_size, txt=paragraph,
                 ln=1, align='C')
        pdf.ln()
        with open(csv_path, newline='') as csv_file:
            reader = csv.reader(csv_file)
            for (index, row) in enumerate(reader):
                for cell in row:
                    if index == 0:
                        pdf.set_font(font, 'B', font_size)
                    else:
                        pdf.set_font(font, '', font_size)
                    pdf.cell(cell_width/len(row), font_size - 2, str(cell), border=1, align='C')
                pdf.ln()

        pdf.output('test.pdf', 'F')

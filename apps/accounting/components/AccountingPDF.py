from io import BytesIO
import time
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.platypus import Paragraph, Table, TableStyle

from apps.accounting.models import *


def Receipt_pdf(request, pk):
    recpt = Receipt.objects.get(id_rec = pk)
    response = HttpResponse(content_type='application/pdf')
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    #Header
    p.setFillColor('#2471A3')
    p.roundRect(0, 750, 694, 120, 20, fill=1)
    p.drawImage('static/img/logoFCI.png', 250, 760, width=150, height=70)

    p.setFont('Helvetica', 28)
    p.setFillColor('#34495E')
    p.drawCentredString(70, 700, "Receipt")


    p.setFont('Helvetica-Bold', 12)
    p.drawString(50, 680, 'No. '+str(recpt.serial))

    p.setFont('Helvetica',12)
    p.setFillColorRGB(0,0,0)
    p.drawString(460, 700, 'Date: '+str(recpt.start_date))
    p.line(450, 697, 562, 697)

    #Footer
    p.setFont('Helvetica', 9)
    p.setFillColorRGB(0, 0, 0)
    p.line(0, 50, 800, 50)
    p.drawString(30, 20, 'Date of printing '+time.strftime("%m/%d/%y %H:%M:%S")+' by %s' % request.user.first_name)

    #Boby
    styles = getSampleStyleSheet()
    stylesBH = styles["Heading3"]
    stylesBH.alignment = TA_CENTER
    stylesBH.fontSize = 10
    stylesBH.fill = '#34495E'
    description = Paragraph('''Description''',stylesBH)
    waytopay = Paragraph('''Payment Method''',stylesBH)
    value = Paragraph('''Total''',stylesBH)
    data = []
    data.append([description, waytopay, value])

    stylesBD = styles["BodyText"]
    stylesBD.alignment = TA_CENTER
    stylesBD.fontSize = 7
    high = 550
    this_receipt = [recpt.description, recpt.waytopay, recpt.total]
    data.append(this_receipt)
    high = high - 18

    width, height = A4
    table = Table(data, colWidths=[11 * cm, 4 * cm, 2 * cm])
    table.setStyle(TableStyle([
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    ]))
    table.wrapOn(p, width, height)
    table.drawOn(p, 40, high)

    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
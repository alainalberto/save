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
    p.drawCentredString(70, 700, "RECEIPT")


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

def Invoices_pdf(request, pk):
    invoice = Invoice.objects.get(id_inv = pk)
    customer = Customer.objects.get(id_cut=invoice.customers_id)
    descrip = InvoicesHasItem.objects.filter(invoices=invoice)
    business = Busines.objects.get(id_bus=invoice.business_id)
    response = HttpResponse(content_type='application/pdf')
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    #Header
    p.setFillColor('#2471A3')
    p.roundRect(0, 750, 694, 120, 20, fill=1)
    p.drawImage('static/img/logoFCI.png', 250, 760, width=150, height=70)

    p.setFont('Helvetica', 28)
    p.setFillColor('#E5E7E9')
    p.drawCentredString(70, 785, "INVOICE")

    p.setFillColor('#34495E')
    p.setFont('Helvetica-Bold', 12)
    p.drawString(50, 730, 'No. '+invoice.prefix+"-"+str(invoice.serial))

    p.setFont('Helvetica', 10)
    p.drawImage('static/img/icon/address-o.png', 50, 700, width=10, height=10)
    p.drawString(65, 700, business.address)
    p.drawImage('static/img/icon/phone-o.png', 50, 680, width=10, height=10)
    p.drawString(65, 680, business.phone)
    if business.fax:
      p.drawImage('static/img/icon/fax-o.png', 50, 660, width=10, height=10)
      p.drawString(65, 660, business.fax)


    p.setFont('Helvetica',12)
    p.setFillColorRGB(0,0,0)
    p.drawString(460, 700, 'Date: '+str(invoice.start_date))
    p.line(450, 697, 562, 697)

    #Customer
    if customer.company_name:
        p.setFillColor('#34495E')
        p.setFont('Helvetica-Bold', 14)
        p.drawString(75, 620, customer.company_name)
        p.drawString(50, 620, 'To:')
    if customer.fullname:
        p.setFont('Helvetica-Bold', 12)
        p.drawString(75, 600, customer.fullname)
    if customer.address:
        p.setFont('Helvetica', 12)
        p.drawString(75, 580, customer.address)
    if customer.phone:
        p.setFont('Helvetica', 12)
        p.drawString(75, 560, customer.phone)


    #Footer
    p.setFillColor('#2471A3')
    p.roundRect(0, 0, 694, 50, 0, fill=1)
    p.setFont('Helvetica', 9)
    p.setFillColorRGB(0, 0, 0)
    p.line(0, 50, 800, 50)
    user_print = ""
    if request.user.first_name:
        user_print = request.user.first_name+" "+request.user.last_name
    else:
        user_print= request.user.username
    p.drawString(30, 20, 'Date of printing '+time.strftime("%m/%d/%y %H:%M:%S")+' by %s' % user_print)
    p.setFillColor('#34495E')
    p.setFont('Helvetica', 10)
    p.drawString(200, 60, 'THANK YOU FOR YOUR BUSSINESS!')


    #Boby
    p.setFillColor('#020000')
    p.setFont('Helvetica-Bold', 14)
    p.drawString(450, 590, "Total: $"+ str(invoice.total))
    p.setFont('Helvetica', 12)
    p.drawString(450, 570, "Discount: $" + str(invoice.discount))
    p.setFont('Helvetica', 12)
    p.drawString(450, 550, "Subtotal: $" + str(invoice.subtotal))

    styles = getSampleStyleSheet()
    stylesBH = styles["Heading3"]
    stylesBH.alignment = TA_CENTER
    stylesBH.fontSize = 10
    stylesBH.fill = '#34495E'
    quantity = Paragraph('''Quantity''', stylesBH)
    description = Paragraph('''Description''', stylesBH)
    value = Paragraph('''Unit Price''',stylesBH)
    tax = Paragraph('''Tax %''', stylesBH)
    subtotal = Paragraph('''Subtotal''', stylesBH)
    data = []
    data.append([quantity, description, value, tax, subtotal])

    stylesBD = styles["BodyText"]
    stylesBD.alignment = TA_CENTER
    stylesBD.fontSize = 7
    high = 510
    for item in descrip:
        this_descrip = [item.quantity, item.description, item.value, item.tax, item.subtotal]
        data.append(this_descrip)
        high = high - 18

    width, height = A4
    table = Table(data, colWidths=[2 * cm, 8 * cm, 4 * cm, 2 * cm])
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
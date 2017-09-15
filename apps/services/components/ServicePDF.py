from io import BytesIO
import time
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.platypus import Paragraph, Table, TableStyle
from apps.services.models import *

def PendingListPDF(request):
    permit = Permit.objects.all()
    insurance = Insurance.objects.filter(state='Pending')
    equipment = Equipment.objects.filter(state='Pending')
    ifta = Ifta.objects.filter(state='Pending')
    contract = Contract.objects.filter(state='Pending')
    audit = Audit.objects.filter(state='Pending')
    driver = Driver.objects.filter(state='Pending')
    response = HttpResponse(content_type='application/pdf')
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    #Header
    p.setFillColor('#2471A3')
    p.roundRect(0, 790, 694, 60, 10, fill=1)
    p.drawImage('static/img/logoFCI.png', 520, 795, width=70, height=45)

    p.setFont('Helvetica', 14)
    p.setFillColor('#BDBDBD')
    p.drawCentredString(200, 810, "List of pending services")

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
    customer = Paragraph('''Customer''', stylesBH)
    service = Paragraph('''Service''', stylesBH)
    description = Paragraph('''Description''', stylesBH)
    update = Paragraph(''' Last Up Date''', stylesBH)
    user = Paragraph('''Up Date User''',stylesBH)
    data = []
    data.append([customer, service,description, update, user])

    stylesBD = styles["BodyText"]
    stylesBD.alignment = TA_CENTER
    stylesBD.fontSize = 7
    high = 730
    for pr in permit:
     this_permit = [pr.customers, 'Permit', pr.name, pr.update, pr.users]
     data.append(this_permit)
     high = high - 18
    for i in insurance:
     description;
     if i.policy_liability or i.cargo_policy or i.physical_damg_policy:
        description = 'Liability: '+i.policy_liability, 'Cargo: '+i.cargo_policy, 'Physical Damage: '+i.physical_damg_policy
     this_insurance = [i.customers, 'Insurance', description, i.update, i.users.first_name]
     data.append(this_insurance)
     high = high - 18
    for e in equipment:
     this_equipment = [e.customers, 'Equipment', 'Serial Number: '+e.serial, e.update, e.users.first_name]
     data.append(this_equipment)
     high = high - 18
    for it in ifta:
     this_ifta = [it.customers, 'IFTA', 'Type: '+it.type, it.update, it.users.first_name]
     data.append(this_ifta)
     high = high - 18
    for c in contract:
     this_contrac = [c.customers, 'Contract', 'Serial: '+c.serial, c.update, c.users.first_name]
     data.append(this_contrac)
     high = high - 18
    for a in audit:
     this_audit = [a.customers, 'Audit', 'Type: '+a.type, a.update, a.users.first_name]
     data.append(this_audit)
     high = high - 18
    for d in driver:
     this_driver = [d.customers, 'Driver', 'Name: '+d.name, d.update, d.users.first_name]
     data.append(this_driver)
     high = high - 18
    width, height = A4
    table = Table(data, colWidths=[4 * cm, 2 * cm, 7 * cm, 2.5 * cm, 3.5 * cm])
    #table.setStyle(TableStyle([
    #    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
    #    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    #]))
    table.wrapOn(p, width, height)
    table.drawOn(p, 20, high)

    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
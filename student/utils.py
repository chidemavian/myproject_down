

import os
from xlwt import Workbook, easyxf
from xhtml2pdf import pisa
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.utils.html import escape
try:
    import cStringIO as StringIO
except:
    import StringIO

class UnsupportedMediaPathException(Exception): pass

def fetch_resources(uri):
    """
    Callback to allow xhtml2pdf/reportlab to retrieve Images,Stylesheets, etc.
    `uri` is the href attribute from the html link element.
    `rel` gives a relative path, but it's not used here.

    """
    if uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT,
            uri.replace(settings.MEDIA_URL, ""))
    elif uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.STATIC_ROOT,
            uri.replace(settings.STATIC_URL, ""))
    else:
        # if relative path is used tries to prefix path with static root
        # if this does not yield a file, tries prefixing with media root
        # if this fails too raise exception
        path = os.path.join(settings.STATIC_ROOT,
            uri.replace(settings.STATIC_URL, ""))

        if not os.path.isfile(path):
            path = os.path.join(settings.MEDIA_ROOT,
                uri.replace(settings.MEDIA_URL, ""))

            if not os.path.isfile(path):
                raise UnsupportedMediaPathException(
                    'media urls must start with %s or %s' % (
                        settings.MEDIA_ROOT, settings.STATIC_ROOT))
    return path


def render_to_pdf(template_src, context_dict):
    """Function to render html template into a pdf file"""
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")),
        dest=result,
        encoding='UTF-8',
        link_callback=fetch_resources)
    if not pdf.err:
        response = HttpResponse(result.getvalue(),
            mimetype='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=report.pdf'

        return response

    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

def render_to_xls(context_dict):
    """Function to output data in a queryset to MS Excel"""

    students_list, title, school = context_dict.get('students_list'), context_dict.get('report_title'), context_dict.get('school')

    style0 = easyxf('font: name Times New Roman, colour blue, bold on')
    style1 = easyxf('',num_format_str='D-MMM-YY')

    wb = Workbook()
    ws = wb.add_sheet()
    ws.write(0, 0, school.name, style0)
    ws.write(1, 0, school.address, style0)
    ws.write(1, 0, school.website, style0)
    ws.write(3, 0, title, style0)
    ws.write(3, 4, datetime.now(), style1)

    if 'withdraw' in title.lower():
        field_names = ['S/N', 'Name', 'Admission No', 'Reason', 'Date']
    else:
        field_names = ['S/N', 'Name', 'Sex', 'Admission No', 'Class', 'Arm', 'House']

    for i in len(field_names):
        ws.write(5, i, field_names[i], style0)

    row, counter = 6, 1
    for student in students_list:
        if 'withdraw' in title.lower():
            ws.write(row, 0, counter)
            ws.write(row, 1, student.fullname)
            ws.write(row, 2, student.admissionno)
            ws.write(row, 3, student.withdrawal__reason)
            ws.write(row, 4, student.withdrawal__date_withdrawn, style1)
        else:
            ws.write(row, 0, counter)
            ws.write(row, 1, student.fullname)
            ws.write(row, 2, student.sex)
            ws.write(row, 3, student.admissionno)
            ws.write(row, 4, student.admitted_class)
            ws.write(row, 5, student.admitted_arm)
            ws.write(row, 6, student.house)

        row += 1; counter += 1

    xls = StringIO.StringIO()
    wb.save(xls)
    response = HttpResponse(xls.getvalue(), mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=report.xls'

    return response

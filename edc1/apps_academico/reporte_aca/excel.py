import xlwt
from PIL import Image
from io import BytesIO
from django.http import HttpResponse
from django.contrib.auth.models import User

def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users_prueba.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')
    img= Image.open('media/image_event/espol.png')
    image_parts = img.split()
    r = image_parts[0]
    g = image_parts[1]
    b = image_parts[2]
    img = Image.merge("RGB", (r, g, b))
    fo = BytesIO()
    img.save(fo,format='bmp')
    ws.insert_bitmap_data(fo.getvalue(),0,0)
    #xlwt.Worksheet.insert_bitmap('media/imagen_event/espol.png', 0, 1, x)

    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    mystyle = xlwt.easyxf('pattern: pattern solid, fore_colour blue;'
                              'font: colour white, bold True')
    columns = ['Username', 'First name', 'Last name', 'Email address', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], mystyle)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = User.objects.all().values_list('username', 'first_name', 'last_name', 'email')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response
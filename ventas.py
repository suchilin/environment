import mercadopago
import os
import requests
import json
import xlwt
import math
from datetime import date

client_id = os.environ['MP_CLIENT_ID']
client_secret = os.environ['MP_CLIENT_SECRET']
hoy = str(date.today())
mp = mercadopago.MP(client_id, client_secret)
access_token = mp.get_access_token()
print(mp.get_access_token())
user_id = "177416286"
book = xlwt.Workbook()
sheet = book.add_sheet('Producto_vendidos')
i = 0
url = 'https://api.mercadolibre.com/orders/search?seller=%s&access_token=%s' % (
    user_id, access_token)
url = url+'&order.date_created.from=2019-08-15T00:00:00.000-00:00'
url = url+'&order.date_created.to='+hoy+'T00:00:00.000-00:00'

ventasResponse = requests.get(url)
ventas = json.loads(ventasResponse.text)
total_pages = math.ceil(ventas['paging']['total']/50)
for page in range(total_pages):
    ventas = []
    urlfinal = ''
    urlfinal = url+'&offset='+str(page*50)
    print(urlfinal)
    ventasResponse = requests.get(urlfinal)
    ventas = json.loads(ventasResponse.text)
    for venta in ventas['results']:
        shipping_id = venta['shipping']['id']
        shipping_details_url = 'https://api.mercadolibre.com/shipments/' + \
            str(shipping_id)+'?access_token='+access_token
        shipping_details = requests.get(shipping_details_url)
        shipping_details = json.loads(shipping_details.text)
        shipping_status = 'Sin status'
        delivered_date = ''
        if 'status' in shipping_details:
            shipping_status = shipping_details['status']
        if 'status_history' in shipping_details:
            if 'date_delivered' in shipping_details['status_history']:
                delivered_date = shipping_details['status_history']['date_delivered']
        logistic_type = 'No especificado'
        if 'logistic_type' in shipping_details:
            logistic_type = shipping_details['logistic_type']
        for item in venta['order_items']:
            row = sheet.row(i)
            row.write(0, venta['buyer']['nickname'])
            row.write(1, item['item']['id'])
            row.write(2, item['item']['title'])
            row.write(3, item['full_unit_price'])
            row.write(4, venta['shipping']['shipping_mode'])
            row.write(5, venta['shipping']['status'])
            row.write(6, logistic_type)
            row.write(7, item['quantity'])
            row.write(8, shipping_status)
            row.write(9, delivered_date)
            print("ITEM: ", i)
            i = i+1
filename = 'ventas_'+hoy+'.xlsx'
book.save(filename)
#  print(venta['buyer']['nickname'],item['item']['id'],item['item']['title'],item['full_unit_price'],venta['shipping']['shipping_mode'])

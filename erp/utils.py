from django.conf import settings
from suds.client import Client
from suds.xsd.doctor import Import, ImportDoctor

def test():
    URL_DEV = 'http://181.224.255.235/WCFBUSPORTALPB_DES/RestServicePeruBus.svc?wsdl'

    imp = Import('http://www.w3.org/2001/XMLSchema',location='http://www.w3.org/2001/XMLSchema.xsd')
    imp.filter.add('http://tempuri.org/')
    client = Client(URL_DEV, doctor=ImportDoctor(imp))
    print('call getOrigen...')
    result = client.service
    print(result)

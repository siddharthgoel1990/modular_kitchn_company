from django.http import HttpResponse
import jijacrypto as j
from django.shortcuts import render
import json
from decimal import *
from django.views.generic import TemplateView
# Create your views here.


from rest_framework import status
from rest_framework.decorators import api_view, parser_classes, permission_classes, authentication_classes
from rest_framework.parsers import JSONParser, FileUploadParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from django.http import HttpResponse



class WebsiteIndexPage(TemplateView):
    template_name = "index.html"

@api_view(['GET'])
@csrf_exempt
def crypto(request):
    # print "HHH"
    data = j.get_all_price2()
    # data = [{'transaction': 'cryptopia_buy-bittrex_sell', 'name': 'ZENBTC', 'profit': Decimal('-0.0001006799999999996933497392604'), 'sell_rate': 0.00442019, 'profit_raio': Decimal('-0.02227004979130116524481306351'), 'buy_rate': 0.00452087}, {'transaction': 'bittrex_buy-cryptopia_sell', 'name': 'ZENBTC', 'profit': Decimal('-0.00003731000000000046779025097976'), 'sell_rate': 0.00447544, 'profit_raio': Decimal('-0.008267686000775683468835494868'), 'buy_rate': 0.00451275}]
    # data = [{'abc': 'nj'},{'abc': 'nk'}]
    print data
    # print json.load(data)
    return Response({'data': data})

@api_view(['POST'])
@csrf_exempt
def sendmail(request):
    import jijacrypto as j
    crequest = request.data
    # print crequest
    # datatobesent = crequest['message']
    # print datatobesent
    j.sendemail(crequest)
    return Response({'status': "ok"})



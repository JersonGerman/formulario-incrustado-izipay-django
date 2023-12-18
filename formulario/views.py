from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import requests as http
from requests.auth import HTTPBasicAuth
import random
import hmac
import hashlib
import json

import environ
env = environ.Env()
environ.Env.read_env()

USERNAME = env('IZI_USERNAME')
PASSWORD = env('IZI_PASSWORD')
PUBLIC_KEY = env('IZI_PUBLIC_KEY')
SHA256_HMAC_KEY =  env('IZI_SHA256_HMAC')
ENDPOINT = env('IZI_API_IZIPAY')

def INCRUSTADO(request):    
    body = {
        'amount': 100, 
        'currency': 'PEN', 
        'customer': {
            'email':'example@gmail.com'
        }, 
        'orderId': random.randint(1,1000)
    }

    auth =HTTPBasicAuth(USERNAME, PASSWORD)
    response = http.post(ENDPOINT+'/api-payment/V4/Charge/CreatePayment', auth=auth, json=body)

    if response.status_code == 200:
        formToken = response.json().get('answer').get('formToken')
        return render(request, 'incrustado.html', {'formToken': formToken, "publickKey": PUBLIC_KEY} )
    else:
        # return JsonResponse({'error': 'No se pudo completar la solicitud'}, status=400)
        return render(request, 'incrustado.html')

def PAID(request):
    if(request.method == 'GET'): 
        return HttpResponseNotFound()

    # Obtener datos del request
    data = {
        'kr-hash-key': request.POST.get('kr-hash-key'),
        'kr-hash-algorithm': request.POST.get('kr-hash-algorithm'),
        'kr-answer': request.POST.get('kr-answer'),
        'kr-answer-type': request.POST.get('kr-answer-type'),
        'kr-hash': request.POST.get('kr-hash')
    }

    # Verificar el hash si es válido
    if not checkHash(data, SHA256_HMAC_KEY) :
        return render(request, 'paid.html', {"error":"error de firma"})
    
    # Recuperar el estado de la transaccion y orderId
    answer = json.loads(data['kr-answer'])
    orderStatus = answer['orderStatus']
    return render(request, 'paid.html', {"answer": answer, "orderStatus": orderStatus } )

@csrf_exempt
def IPN(request):
    if(request.method == 'GET'): 
        return HttpResponseNotFound()
    
    # Obtener datos del request
    data = {
        'kr-hash-key': request.POST.get('kr-hash-key'),
        'kr-hash-algorithm': request.POST.get('kr-hash-algorithm'),
        'kr-answer': request.POST.get('kr-answer'),
        'kr-answer-type': request.POST.get('kr-answer-type'),
        'kr-hash': request.POST.get('kr-hash')
    }

    # Verificar el hash si es válido
    if not checkHash(data, PASSWORD) :
        return HttpResponse("Signature invalid", status_code=400)
    
    # Recuperar el estado de la transaccion y orderId
    answer = json.loads(data['kr-answer'])
    orderStatus = answer['orderStatus'] ## PAID or UNPAID
    return HttpResponse("Order Status is !"+ orderStatus, status=200)

# Función verificadora   
def checkHash(data_post, key_sha256):
    key_sha256_bytes = key_sha256.encode()  # Convierte la llave secreta a bytes
    answer_bytes = data_post['kr-answer'].encode()  # Convierte la cadena a bytes

    hash = hmac.new(key_sha256_bytes, answer_bytes, hashlib.sha256)

    return hash.hexdigest() == data_post['kr-hash']     # Devuelve "True" si los Hash son identicos


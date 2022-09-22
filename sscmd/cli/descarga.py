# -*- coding: utf-8 -*-
"""
Created on Tue May  4 00:24:49 2021

@author: Daga
"""

import requests
import json
import zipfile
import io
import time
import os


from base64 import b64encode

## Parametro generales
#server = "https://app1.microdatos.cl" # Para definir servidor
#userAndPass = b64encode(b"camiapi:CMDdatos2021*").decode("ascii") # Para logear 

## Parametro funcion
#formato = "Tabular" # Para definir base a descargar [Tabular, STATA, SPSS, Binary, DDI, Paradata]
#path_download = "C:\\Users\\Daga\\Documents\\ss" # Para definir directorio donde se guardara la base
#cuestionario = "8aea1ec5-e5a9-4bba-ad6b-1f343c96c0b2" # Id cuestionario principal, debe ir con guiones buscar en https://app1.microdatos.cl/SurveySetup
#v = "3"  # version, debe ir en string

def descarga(server, userAndPass,formato,cuestionario,v,path_download,subfolder=''):
    #userAndPass = b64encode(b"admin:Micro.2020*").decode("ascii") 
    headers = { 'Authorization' : 'Basic %s' %  userAndPass } 
    #server = "https://app2.microdatos.cl/primary/"
    #v = "2"
    #cuestionario = "4daaa215-bf0d-480b-92cc-c3f6fa313fdf"
    #path_download = "home/cmd/datos/ELSOC_M1/data"
    #formato = "STATA"
    
    ##################################################
    # 0) Comienza descargando base
    ##################################################
    print("#############################")
    print("Comenzando proceso de descarga para cuestionario " + str(cuestionario) + 'en formato ' + str(formato) + " en version " + str(v))
    cuestionario = cuestionario+ "$" + str(v) # Id cuestionario principal
    
    ##################################################
    # 1) Comienza descargando base
    ##################################################
  
    #url de la api
    url=server+"api/v2/export"
       
    #json para fijar parametros
    
    data={
      "ExportType": formato,
      "QuestionnaireId":cuestionario,
      "InterviewStatus": "All",
      "From": None,
      "To": None,
      "AccessToken": None,
      "RefreshToken": None,
      "StorageType": None,
      "TranslationId": None,
      "IncludeMeta": True
    }
    #data = json.dumps(data) 

   
    # realiza requerimiento
    r=requests.post(url = url, headers=headers, json=data)
    
    #- r.raise_for_status()  Sirven para inspeccionar resultado request
   
    response_data = r.json() 
    JobId=r.json()["JobId"] 
       
    
    
    ##################################################
    #2 Espera hasta que exportacion se encuentre completa
    ##################################################
    
    Status = None
    Progress= 0
    while Status!="Completed":
        if Progress==0:
            print("Generando exportacion de " + str(formato) + "...")
    
        time.sleep(10)
        url = server + "/api/v2/export/" + str(JobId)
        r = requests.get(url = url, headers = headers)
        Progress=r.json()["Progress"]
        Status = r.json()["ExportStatus"]
    
        if Status=="Running":
            print(str(Progress)+"%", end = ' ')
        if Status=="Completed":
            print( str(100)+"%"+" Exportacion completada de manera exitosa")
            
    
    ##################################################
    #3 Descarga, descomprime, y guarda
    ##################################################
    
    #Genera descarga
    print("Descargando " + str(formato) + "...")
    url = server + "/api/v2/export/"  +str(JobId) + "/file" 
    r = requests.get(url = url, headers = headers)
    r.raise_for_status()
    if r.status_code == 200:
        print("Descarga completada de manera exitosa")
    else:
        print("Fallo descarga")
    
    
    #Genera ruta para guardar si no existe
    if formato=="Paradata":
        path = os.path.join(path_download,"paradata_v"+v,subfolder)
    
    if formato=="STATA":
        path = os.path.join(path_download,"SurveySolutions_v"+v,subfolder)
        
    if not os.path.exists(path):
        os.makedirs(path)
    
    #Descomprime y guarda en ruta    
    print("Descompriendo y guardando en.. " + path)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(path)
    
    print("Proceso finalizado")
    print("#############################")
    

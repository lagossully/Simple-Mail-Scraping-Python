import imaplib
import re
import string
import time
from time import sleep
import os
import email
from email.parser import HeaderParser

host = 'imap.gmail.com'
imap = imaplib.IMAP4_SSL(host)

f = open("InfoSensible.txt", "r")#txt que contiene mi contraseña
Contraseña = f.read()

g = open("msgidcorreo1wom.txt","w")
h = open("msgidcorreo2falabella.txt","w")
i = open("msgidcorreo3reddit.txt","w")
j = open("msgidcorreo4needle.txt","w")
k = open("msgidcorreo5beersquare.txt","w")
l = open("fromcorreo1wom.txt","w")
m = open("fromcorreo2falabella.txt","w") 
n = open("fromcorreo3reddit.txt","w")
o = open("fromcorreo4needle.txt","w")
p = open("fromcorreo5beersquare.txt","w")
q = open("datecorreo1wom.txt","w")
r = open("datecorreo2falabella.txt","w")
s = open("datecorreo3reddit.txt","w")
t = open("datecorreo4needle.txt","w")
u = open("datecorreo5beersquare.txt","w")
v = open("primerocorreo1wom.txt","w")
w = open("primerocorreo2falabella.txt","w")
x = open("primerocorreo3reddit.txt","w")
y = open("primerocorreo4needle.txt","w")
z = open("primerocorreo5beersquare.txt","w")
aa = open("penultimocorreo1wom.txt","w")
bb = open("penultimocorreo2falabella.txt","w")
cc = open("penultimocorreo3reddit.txt","w")
dd = open("penultimocorreo4needle.txt","w")
ee = open("penultimocorreo5beersquare.txt","w")

escribir = [g,h,i,j,k]
escribir2 = [l,m,n,o,p]
escribir3 = [q,r,s,t,u]
escribir4 = [v,w,x,y,z]
escribir5 = [aa,bb,cc,dd,ee]

correos = ['info@news.wom.cl','novedades@cl.falabella.com','noreply@redditmail.com','needle@needle.cl','contacto@beersquare.com']

imap.login('lagosdiego97@gmail.com', Contraseña)
imap.select('Inbox')

def obtenermsgid(texto,emisor):
    typ, data = imap.search(None,'FROM', emisor)
    for num in data[0].split():
        typ, data = imap.fetch(num, '(BODY[HEADER.FIELDS (MESSAGE-ID)])')
        datito= data[0][1].decode()
        datito=datito.replace("Message-ID:", "")
        datito=datito.replace(">", "")
        datito=datito.replace("<", "")
        datito=datito.replace("Message-Id:", "")
        datito=datito.strip()
        print(datito)
        texto.write(datito+'\n')

def obtenerfrom(texto,emisor):
    typ, data = imap.search(None,'FROM', emisor)
    for num in data[0].split():
        typ, data = imap.fetch(num, '(BODY[HEADER.FIELDS (From)])')
        datito= data[0][1].decode()
        datito=datito.replace("FROM:", "")
        datito=datito.replace(">", "")
        datito=datito.replace("<", "")
        datito=datito.replace("From:", "")
        datito=datito.strip()
        print(datito)
        texto.write(datito+'\n')

def obtenerdate(texto,emisor):
    typ, data = imap.search(None,'FROM', emisor)
    for num in data[0].split():
        typ, data = imap.fetch(num, '(BODY[HEADER.FIELDS (DATE)])')
        datito= data[0][1].decode()
        datito=datito.replace("DATE:", "")
        datito=datito.replace(">", "")
        datito=datito.replace("<", "")
        datito=datito.replace("Date:", "")
        datito=datito.strip()
        print(datito)
        texto.write(datito+'\n')

def todoslosreceived(texto1,texto2,emisor):
    typ, data = imap.search(None,'FROM', emisor)
    for num in data[0].split():
        typ, data = imap.fetch(num, '(BODY[HEADER.FIELDS (Received)])')
        datito= data[0][1].decode()
        prueba = cortarreceived(datito,texto1,texto2)

def cortarreceived(receivedcomprimido,textoprimero,textopenultimo):
    receivedcomprimido = receivedcomprimido.strip()
    receivedcomprimido = re.split("\s", receivedcomprimido)
    separados = []
    rstring = []
    penultimo = []
    idx = 0
    contador = 0

    for i in range (0, len(receivedcomprimido)):
        if receivedcomprimido[i] == 'Received:' and contador == 0:
            idx = i
            contador = contador+1
        elif receivedcomprimido[i] == 'Received:' and contador > 0:
            separados.append(receivedcomprimido[idx:i])
            idx = i
        if i == len(receivedcomprimido)-1:
            separados.append(receivedcomprimido[idx:i])

    for i in range(0, len(separados)):
        rstring.append([]) ##crea un lista de listas, matriz(?)
        for j in range(0,len(separados[i])):
            if separados[i][j] != '':
                if len(rstring[i]) == 0:
                    rstring[i] = str(separados[i][j]) + " "
                else:
                    rstring[i] = str(rstring[i]) + str(separados[i][j]) + " "   
    primero = rstring[len(rstring)-1] #ya que el imap lee los recieved al revés, el primero es el último
    print(primero)
    textoprimero.write(primero+'\n')
    if len(rstring) == 2:
        penultimo = rstring[0] #el ayudante dijo que en el caso de tener solo dos received, se debe tomar el último (el primero en la lista) como "penultimo" 
    if len(rstring) >= 3:
        penultimo = rstring[(1)] #el penúltimo es el segundo
    print(rstring)
    textopenultimo.write(penultimo)
    textopenultimo.write('\n')

for i in range (len(correos)):
    msgid= obtenermsgid(escribir[i],correos[i])
    From = obtenerfrom(escribir2[i],correos[i])
    Date = obtenerdate(escribir3[i],correos[i])
    primerreceived = todoslosreceived(escribir4[i],escribir5[i],correos[i])

imap.close()
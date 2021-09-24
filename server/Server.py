from genericpath import isdir
import os
import zmq
import random
import string
import hashlib

context = zmq.Context()

links = {}

s = context.socket(zmq.REP)

s.bind('tcp://*:8010')

tamaño = 1024*1024*50
        


def upload(dates):
    if(not os.path.isdir(os.getcwd() + '/' + dates['nombre'])):
        os.mkdir(dates['nombre'])

    s.recv_string()

    if(dates['archivo'] in os.listdir(os.getcwd() + '/' + dates['nombre'])):
        s.send_string('esta')
    else:
        s.send_string('no esta')
        arc = open('./'+ dates['nombre'] + '/' + dates['archivo'],'wb')
        strng = s.recv()
        while strng:
            arc.write(strng)
            s.send('llega'.encode('utf-8'))
            strng = s.recv()
        s.send('llega'.encode('utf-8'))
        arc.close()


def download(dates):
    arc = open('./'+ dates['nombre'] + '/' + dates['archivo'], 'rb')
    strng = arc.read(tamaño)
    while strng:
        s.recv_string()
        s.send(strng)
        strng = arc.read(tamaño)
    s.recv_string()
    s.send(b'')
    arc.close()


def listDates(dates):
    contenido = os.listdir('./'+ dates['nombre'])
    s.recv_string()
    s.send_json(contenido)



def shareLink(dates):
    while True:
        linklocal = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20))
        if not linklocal in links.keys():
            break
    links[linklocal] = []
    links[linklocal].append(dates['nombre'])
    links[linklocal].append(dates['archivo'])
    s.recv_string()
    s.send_string(linklocal)

def downloadLink(dates):
    s.recv_string()
    if dates['archivo'] in links.keys():
        s.send_string('paso')
        s.recv_string()
        s.send_string(links[dates['archivo']][1])
        s.recv_string()
        print(links[dates['archivo']])
        print(links[dates['archivo']][0])
        print(links[dates['archivo']][1])
        arc = open('./' + links[dates['archivo']][0] + '/' + links[dates['archivo']][1], 'rb')
        strng = arc.read()
        s.send(strng)
        arc.close()
    else:
        s.send_string('no paso')


while True:
    print('Esperando accion...')
    jsonrecv = s.recv_json()
    s.send_string('')
    if jsonrecv['accion'] == 'upload':
        upload(jsonrecv)
    elif jsonrecv['accion'] == 'download':
        download(jsonrecv)
    elif jsonrecv['accion'] == 'list':
        listDates(jsonrecv)
    elif jsonrecv['accion'] == 'sharelink':
        shareLink(jsonrecv)
    elif jsonrecv['accion'] == 'downloadlink':
        downloadLink(jsonrecv)



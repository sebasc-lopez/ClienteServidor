import zmq
from zmq.sugar.constants import NULL
import json
import sys
import os
import hashlib

context = zmq.Context()

s = context.socket(zmq.REQ)
s.connect('tcp://localhost:8010')
jsonSend = NULL

tamaño = 1024*1024*50

sha1 = hashlib.sha1()


if sys.argv[2] == "list":
    jsonSend = {'nombre':sys.argv[1], 'accion':sys.argv[2]}
else:
    root, extension = os.path.splitext(os.getcwd() + '/' + sys.argv[3])
    '''with open(sys.argv[3], 'rb') as f:
        while True:
            data = f.read(tamaño)
            if not data:
                break
            sha1.update(data)'''
    jsonSend = {'nombre':sys.argv[1], 'accion':sys.argv[2], 'archivo':sys.argv[3], 'ext':extension, 'hash':sha1.hexdigest()}



s.send_json(jsonSend)

hola = s.recv_string()



while True:
    if jsonSend['accion'] == 'upload':
        s.send_string('')
        if s.recv_string() == 'esta':
            print('El archivo ya esxiste porfavor cambia el nombre')
        else:
            arc = open(sys.argv[3], 'rb')
            strng = arc.read(tamaño)
            while strng:
                s.send(strng)
                s.recv()
                strng = arc.read(tamaño)
            arc.close()
            s.send(b'')
            s.recv()
    elif jsonSend['accion'] == 'download':
        s.send_string('listo')
        dataracv = s.recv()
        arc = open(jsonSend['archivo'], 'wb')
        while dataracv:
            arc.write(dataracv)
            s.send_string('listo')
            dataracv = s.recv()
        arc.close()
    elif jsonSend['accion'] == 'list':
        s.send_string('listo')
        contenido = s.recv_json()
        print('Lista de archivos:\n')
        for i in contenido:
            print('\t', i)
    elif jsonSend['accion'] == 'sharelink':
        s.send_string('listo')
        link = s.recv_string()
        print(link)
    elif jsonSend['accion'] == 'downloadlink':
        s.send_string('listo')
        if s.recv_string() == 'paso':
            s.send_string('')
            nombrearch = s.recv_string()
            s.send_string('')
            arc = open(nombrearch, 'wb')
            datas = s.recv()
            arc.write(datas)
            arc.close()
        else:
            print('Codigo expiro')

    break



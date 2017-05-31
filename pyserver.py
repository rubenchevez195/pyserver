#Server Libraries
import socketserver
from http.server import BaseHTTPRequestHandler

#Google Maps Libraries
import googlemaps
from datetime import datetime

#Server Configuration
from flask import Flask, abort, request, jsonify 
import json

import base64
from PIL import Image
import operator
import io

##Google Maps Configuration
gmaps = googlemaps.Client(key='AIzaSyAUOMk8n8nhxUiSTEXq06jNth_kiV_s55E')
app = Flask(__name__)
@app.route('/ejercicio1', methods=['POST'])
def ejercicio1():
	data = request.get_json(force=True)
	try:
		origen = data['origen']
		destino = data['destino']

		directions_result = gmaps.directions(origen, destino, mode="driving", departure_time=datetime.now())
		json = jsonify(directions_result)
		resp = 'Http 200{"ruta":['
		if(len(directions_result) != 0):
			listDir = directions_result[0]['legs'][0]['steps']
			cont = 0
			for obj in listDir:
				if(cont != 0):
					resp+=','
				resp+= '{'+str(obj['start_location'])+','+str(obj['end_location'])+'}'
				cont+=1
		else:
			return('Http 400{ "error":"No hay Resultados, Revise que la direccion este escrita correctamente y el formato JSON sea el correcto"}')
		resp += ']'
		return resp
	except (KeyError, TypeError, ValueError, Exception):
		return('Http 400{ "error":"No hay Resultados, Revise que la direccion este escrita correctamente y el formato JSON sea el correcto"}')
@app.route('/ejercicio2', methods=['POST'])
def ejercicio2():
	data = request.get_json(force=True)
	try:
		origen = data['origen']
		restaurants = gmaps.places('restaurant', origen, 2000, 'en-AU', min_price=1, max_price=100000, open_now=False, type='food')
		resp = 'Http 200{"restaurantes":['
		if(len(restaurants) != 0):
			listDir = restaurants["results"]
			cont = 0
			for obj in listDir:
				if(cont != 0):
					resp+=','
				resp+= '{'+str(obj["geometry"]["location"]["lat"])+','+str(obj["geometry"]["location"]["lng"])+'}'
				cont+=1
		else:
			return('Http 400{ "error":"No hay Resultados, Revise que la direccion este escrita correctamente"}')
		resp += ']'
		return resp
		return jsonify(restaurants)
	except (KeyError, TypeError, ValueError, Exception):
		return('Http 400{ "error":"No hay Resultados, Revise que la direccion este escrita correctamente y el formato JSON sea el correcto"}')
@app.route('/ejercicio3', methods=['POST'])
def ejercicio3():
	data = request.get_json(force=True)
	try:
		rawImg = data['data']
		imgdata = base64.b64decode(rawImg)
		filename = data['nombre']  # I assume you have a way of picking unique filenames
		with open(filename, 'wb') as f:
			f.write(imgdata)
		pix = Image.open(filename)
		img = pix.load()
		print ('width: %d - height: %d' % pix.size)
		for x in range(0,pix.size[0] - 1):
			for y in range(0 ,pix.size[1] - 1):
				r, g, b = img[x, y]
				value = int((r + g + b)/3)
				img[x, y] = (value, value, value)
		

		strArr = filename.split('.')
		newFilename = strArr[0]+"(Blanco Y Negro)."+strArr[1]
		pix.save(newFilename)
		buf = io.BytesIO()
		pix.save(buf, format="BMP")
		buf.seek(0)
		img_bytes = buf.read()
		base64_encoded_result_bytes = base64.b64encode(img_bytes)
		base64_encoded_result_str = base64_encoded_result_bytes.decode('ascii')
		res = 'Http 200{"nombre" : "'+newFilename+'","data": "'+base64_encoded_result_str+'"}'
		return res 

	except (KeyError, TypeError, ValueError, Exception):
		return('Http 400{ "error":"No hay Resultados, Revise que la imagen no sea compresa y sea formato RGB 24-bits y el formato JSON sea el correcto"}')
@app.route('/ejercicio4', methods=['POST'])
def ejercicio4():
	# print(request.get_json())
	data = request.get_json(force=True)
	try:
		rawImg = data['data']
		imgdata = base64.b64decode(rawImg)
		filename = data['nombre']  # I assume you have a way of picking unique filenames
		with open(filename, 'wb') as f:
			f.write(imgdata)
		pix = Image.open(filename)
		img = pix.load()
		print ('width: %d - height: %d' % pix.size)
		
		newW = int(pix.size[0]/2)
		newH = int(pix.size[1]/2)
		finalFile = ''
		contx = 0
		conty = 0
		while newW > data['tamaño']['ancho']:
			newPix = Image.new( pix.mode , (newW, newH), (255, 255, 255))
			newImage = newPix.load()
			for y in range(0, newH- 1):
				for x in range(0 ,newW - 1):
					xTuple = tuple(map(operator.add, img[contx, conty], img[contx+1, conty]))
					yTuple = tuple(map(operator.add, img[contx, conty+1], img[contx+1, conty+1]))
					finalTuple = tuple(map(operator.add, xTuple, yTuple))
					newImage[x, y] = (int(finalTuple[0]/4), int(finalTuple[1]/4), int(finalTuple[2]/4))
					contx += 2
					# print(xTuple, yTuple)
				conty += 2
				contx = 0
			pix = newPix
			newW = int(newW/2)
			newH = int(newH/2)
		strArr = filename.split('.')
		newFilename = strArr[0]+"(Reducida)."+strArr[1]
		pix.save(newFilename)
		buf = io.BytesIO()
		pix.save(buf, format="BMP")
		buf.seek(0)
		img_bytes = buf.read()
		base64_encoded_result_bytes = base64.b64encode(img_bytes)
		base64_encoded_result_str = base64_encoded_result_bytes.decode('ascii')
		res = 'Http 200{"nombre" : "'+newFilename+'","data": "'+base64_encoded_result_str+'"}'
		return res 
	except (KeyError, TypeError, ValueError, Exception):
		return('Http 400{ "error":"No hay Resultados, Revise que la imagen no sea compresa y sea formato RGB 24-bits y el formato JSON sea el correcto"}')
if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8080, debug='true')



# class MyHandler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         if self.path == '/ejercicio1':
#             # Insert your code here
#         elif self.path == '/ejercicio2':

#         elif self.path == '/ejercicio3':

#         elif self.path == '/ejercicio4':

#         self.send_response(200)

# httpd = SocketServer.TCPServer(("", 8080), MyHandler)
# httpd.serve_forever()

#!/usr/bin/python
# -*- coding: utf-8 -*- 

from flask import Flask, url_for, session, render_template, Response, request, flash, redirect, abort, jsonify
from flaskext.mysql import MySQL
import json
import time


mysql = MySQL()

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('IROOM_SETTINGS', silent=True)
mysql.init_app(app)
last_value = [0,0,0,0,0]

def event_sensor():
	while True:		   
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute ("""SELECT valor FROM sensors WHERE nombre='temperature' order by time desc""")
		temperatura = int(cursor.fetchone()[0])
		if temperatura != last_value[0]:
			sensor = {"tipo":"temperatura", "valor":temperatura}
			data_json = json.dumps(sensor)
			print (sensor)
			yield 'data: %s\n\n' % str(data_json)
			last_value[0] = temperatura
			#flash('Actualizado sensor de temperatura')
		cursor.execute ("""SELECT valor FROM sensors WHERE nombre='humidity' order by time desc""")
		humedad = int(cursor.fetchone()[0])
		if humedad != last_value[1]:
			sensor = {"tipo":"humedad", "valor":humedad}
			data_json = json.dumps(sensor)
			print (sensor)
			yield 'data: %s\n\n' % str(data_json)
			last_value[1] = humedad
			#flash('Actualizado sensor de humedad')
		cursor.execute ("""SELECT valor FROM sensors WHERE nombre='light' order by time desc""")
		luz = int(cursor.fetchone()[0])
		if luz != last_value[2]:
			sensor = {"tipo":"luz", "valor":luz}
			data_json = json.dumps(sensor)
			print (sensor)
			yield 'data: %s\n\n' % str(data_json)
			last_value[2] = luz
			#flash('Actualizado sensor de luz')
		cursor.execute ("""SELECT valor FROM sensors WHERE nombre='sound' order by time desc""")
		sonido = int(cursor.fetchone()[0])
		if sonido != last_value[3]:
			sensor = {"tipo":"sonido", "valor":sonido}
			data_json = json.dumps(sensor)
			print (sensor)
			yield 'data: %s\n\n' % str(data_json)
			last_value[3] = sonido
			#flash('Actualizado sensor de sonido')
		cursor.execute ("""SELECT valor FROM sensors WHERE nombre='motion' order by time desc""")
		movimiento = int(cursor.fetchone()[0])
		if movimiento != last_value[4]:
			sensor = {"tipo":"movimiento", "valor":movimiento}
			data_json = json.dumps(sensor)
			print (sensor)
			yield 'data: %s\n\n' % str(data_json)
			last_value[4] = movimiento
			#flash('Actualizado sensor de temperatura')
		
		"""PARTE 2: ARRIBA TIENE UN EJEMPLO DE ATUALIZACIÓN DEL SENSOR DE TEMPERATURA POR SSE CUANDO
		SE HA ACTUALIZADO EL VALOR EN LA BASE DE DATOS
		ESCRIBA LE CODIGO PARA EL RESTO DE SENSORES """

	   
@app.route('/update_sensor')
def sse_request():	  
	return Response(event_sensor(), mimetype='text/event-stream')
	  
@app.route('/')
def main(): 
	return render_template('index.html')
		
@app.route('/sensors')
def sensors():
	return render_template('sensors.html')

"""
	PARTE 2: INSERTE AQUÍ EL CÓDIGO DE LA FUNCION SENSORS PARA REDIRIGIR A LA VISTA sensors.html 
	CUANDO SE RECIBE UN GET A /sensors
""" 


@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('Has entrado en la sesion')
			return redirect(url_for('sensors'))
	return render_template('login.html', error=error)


@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('Has salido de la sesion')
	return redirect(url_for('main'))


@app.route('/iluminacion')
def iluminacion():
	return render_template('iluminacion.html')
	

@app.route('/setcolor', methods=['GET'])
def setcolor():
	color = request.args.get('color')
	red = int('0x'+color[1:3], 16)
	blue = int('0x'+color[3:5], 16)
	green = int('0x'+color[5:7], 16)
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("INSERT INTO sensors (nombre, valor)" "VALUES(%s, %s)",('red',red))
	cursor.execute("INSERT INTO sensors (nombre, valor)" "VALUES(%s, %s)",('blue',blue))
	cursor.execute("INSERT INTO sensors (nombre, valor)" "VALUES(%s, %s)",('green',green))
	conn.commit()
	"""
		PARTE 3: INSERTE AQUI EL CÓDIGO PARA GUARDAR EL COLOR DE LA BASE DE DATOS 
		CUANDO SE RECIBE DESDE EL CLIENTE POR AJAX
	""" 

if __name__=='__main__':
	with app.test_request_context():
		app.debug = True
		app.run(host ='0.0.0.0')
		

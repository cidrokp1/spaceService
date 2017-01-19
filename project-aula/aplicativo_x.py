"""`main` is the top level module for your Bottle application."""

from bottle import Bottle, template, debug, request, redirect
from google.appengine.ext import ndb
from main
import urllib2
import json
debug(True)
# Create the Bottle WSGI application.
bottle = Bottle()



# PAGINAS DE REGISTO
@bottle.route('/web/register/<username>', method='POST')
def registerUser(username):


    if User.query(User.userName==username).count()==0 and my_containsAny(username, ' '):
    	m = User(userName = username)
    	key = m.put()
    	return name=m.userName , userID=str(key.id()) #COLOCAR EM JSON
    else:
    	return None



# PAGINAS DE LOGIN
@bottle.route('/web/login/<numID>', method='POST')
def loginUser(numID):
	if (int(numID))==0:  #Caso seja o Admin
		redirect("/web/admin/free")
	else: 		     #Caso seja o User
		msgs = User.get_by_id(int(numID))
		if msgs== None:
			return None
		else:
			url="/web/user/"+numID
			redirect(url)


# PAGINAS - ADMINISTRADOR
@bottle.route('/web/adminspace/<r_id>' , method='GET')
def adminspace(r_id):
	response = urllib2.urlopen("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/"+r_id)
	texto=response.read()
	spaces = json.loads(texto)
	return spaces  #lista dos espacos em json


@bottle.route('/web/adminspace/' , method='GET')
def adminspace():
	response = urllib2.urlopen("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/")
	texto=response.read()
	print texto
	spaces = json.loads(texto)

	return texto  #lista dos espacos em json


@bottle.route('/web/admin/free' , method='GET')
def adminFree():
	salas = Sala.query()
	jsonString='''{ "salas" : [ '''
	for m in salas:
		logins = Check.query(Check.roomId==m.roomId).count()
		jsonString+= '''{ "id" : "''' +str(m.roomId)+ ''' " , "name" : " ''' + m.roomName+''' " , "ocupation" : " ''' +str(logins)+''' " } ,'''
	jsonString=jsonString[:-1] + """ ] } """
	spaces = json.loads(jsonString)
	return  spaces  #retornar salas livres da base de dados, em json


@bottle.route('/web/adminspace/addRoom/<s>/<r_id:int>', method='GET')
def addRoom(s,r_id):
	m = Sala(roomName = s, roomId=r_id)
	key = m.put()
	return None



# PAGINAS - ALUNO
@bottle.route('/web/user/<userID>', method = 'GET')
def mainUserPage(userID):
	salas = Sala.query()
	jsonString='''{ "salas" : [ '''
	for m in salas:
		jsonString+= '''{ "id" : "''' +str(m.roomId)+ ''' " , "name" : " ''' + m.roomName+''' " } ,'''
	jsonString=jsonString[:-1] + """ ] } """
	spaces = json.loads(jsonString)
	return  spaces  #retornar salas disponiveis, em json


#WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW


@bottle.route('/enterRoom/<s>/<room_id:int>/<user_id:int>', method='GET')
def enterRoom(s,room_id, user_id):
	profiles=Check.query(Check.userId==user_id)
        for g in profiles:
		g.key.delete()

	r = Check(roomId = room_id, userId=user_id)
	key = r.put()
	return None


@bottle.route('/detailRoom/<room_id:int>', method='GET')
def detailRoom(room_id):
	alunos=Check.query(Check.roomId==room_id)
	jsonString='''{ "alunos" : [ '''
        for al in alunos:
		jsonString+= '''{ "id" : "''' +str(al.userId)+ ''' " } ,'''
	jsonString=jsonString[:-1] + """ ] } """
	students = json.loads(jsonString)
	return  students   #retornar alunos da sala em json



# Define an handler for 404 errors.
@bottle.error(404)
def error_404(error):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.'

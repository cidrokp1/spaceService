"""`main` is the top level module for your Bottle application."""

from bottle import Bottle, template, debug, request, redirect
from google.appengine.ext import ndb
import urllib2
import json
debug(True)
# Create the Bottle WSGI application.
bottle = Bottle()

# Note: don't need to call run() since application is embedded within the App Engine WSGI application server.

#CLASSES 
class MessageM(ndb.Model):
    """Models an individual Guestbook entry with content and date."""
    content = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

class Sala(ndb.Model):
    roomName = ndb.StringProperty()
    roomId= ndb.IntegerProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

class Check(ndb.Model):
    roomId= ndb.IntegerProperty()
    userId= ndb.IntegerProperty()

class User(ndb.Model):
    userName= ndb.StringProperty()

def my_containsAny(str, set):
    for c in set:
        if c not in str: return 1;
    return 0;



# PAGINA INICIAL
@bottle.route('/web')
def mainPage():
	return """
	</body>
	</html>

    <h1>Main Page</h1><br>
    <h4>Selecione uma das opcoes abaixo:</h4>
    <button type="button" onclick="inscrever()">inscrever</button>
    <button type="button" onclick="entrar()">entrar</button>
    <script>
    function inscrever(){
    window.open("http://localhost:8080/web/register/","_self")
    }
    function entrar(){
    window.open("http://localhost:8080/web/login/","_self")
    }
    </script>
    """
    
# PAGINAS DE REGISTO
@bottle.route('/web/register/')
def registerPage():
    return """
    <h1>Register Page</h1>
    <body>
    <form action="/web/register/" method="post">
      Insira um unico nome de utilizador:<br>
      <input name="username" type="text" /> <br>
      <input type="submit" value="Submit">
      <input type="button" value="Voltar" onClick="history.go(-1)"> 
    </form>
    </body>
    """

@bottle.route('/web/register/', method='POST')
def registerUser():
    username = request.forms.get('username')

    if User.query(User.userName==username).count()==0 and my_containsAny(username, ' '):
    	m = User(userName = username)
    	key = m.put()
    	return template("""<h1>Login Page</h1>
    		<body><br>
   		Utilizador {{name}} foi inscrito com o id: {{userID}}
   		<button onclick="location.href='/web'" type="button">Voltar ao Menu Principal</button>
   		</body>""",name=m.userName , userID=str(key.id()))
    else:    
    	return """
    	<h1>Register Page</h1>
    	<body>
    	<form action="/web/register/">
    	O nome de utilizador que inseriu nao e valido!<br>
    	Nota: Tente criar um nome unico/diferente. Este nome de utilizador nao pode conter espacos em branco.
    	<input type="submit" value="retroceder">
    	</form>
    	</body>
    	"""
    	
# PAGINAS DE LOGIN
@bottle.route('/web/login/')
def loginPage():
    return """
    <h1>Login Page</h1>
    <body>
    <form action="/web/login/" method="post">
      ID:<br>
      <input name="numID" type="text" /> <br> <br>
      <input type="submit" value="Submit">
      <input type="button" value="Voltar" onClick="history.go(-1)"> 
    </form>
    </body>
    """

@bottle.route('/web/login/' , method='POST')
def loginUser():
	numID = request.forms.get('numID')
	if (int(numID))==0:
		response = urllib2.urlopen("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/")
		texto=response.read()
		spaces = json.loads(texto)
		return """
      		<h1>Welcome Administrator</h1> <br>
		<h3>Libertar Salas:
		<button onclick="location.href='/web/admin/list'" type="button">libertar</button></h3>  
		<h3>Ver Salas Disponiveis:
      		<button onclick="location.href='/web/admin/free'" type="button">ver</button></h3><br>
      		<input type="button" value="Voltar" onClick="history.go(-1)"> 
    		""" 
	else:
		msgs = User.get_by_id(int(numID))
		if msgs== None:
			return """
    		
    		Esse identificador nao existe<br>

		<input type="button" value="Voltar" onClick="history.go(-1)"> 
    		"""
		else:
			url="/web/user/"+numID
			redirect(url)
			
		
			
# PAGINAS - ADMINISTRADOR
@bottle.route('/web/admin/free' , method='GET')
def adminFree():

	salas = Sala.query()
	data ={}
	for m in salas:
		logins = Check.query(Check.roomId==m.roomId).count()
		data[m.roomId] = [m.roomName, logins]
	
	return template("""
		<html>
		<head>
		<style>
		table {
    		    font-family: arial, sans-serif;
		    border-collapse: collapse;
		    width: 100%;
		}

		td, th {
		    border: 1px solid #dddddd;
		    text-align: left;
		    padding: 8px;
		}

		tr:nth-child(even) {
		    background-color: #dddddd;
		}
		</style>
		</head>
		
		
		<body>
		<h1>Salas disponiveis</h1> </h1> <br>
		<table>
		  <tr>
		    <th>Sala(ID)</th>
		    <th>Sala(nome)</th>
		    <th>Numero de alunos</th>
		  </tr>
		%for item in rooms:
		<tr>
		    	<td> {{item}}</td>
			%for var in rooms[item]:
			  <td>{{var}}</td>  
			%end
			</tr>
		%end
		</table>
		<input type="button" value="Voltar" onClick="history.go(-1)"> 
		</body>
		</html>
		""", rooms=data)	
	


@bottle.route('/web/admin/list' , method='GET')
def adminList():
	response = urllib2.urlopen("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/")
	texto=response.read()
	spaces = json.loads(texto)

	return template("""
		<html>
		<head>
		<style>
		table {
    		    font-family: arial, sans-serif;
		    border-collapse: collapse;
		    width: 100%;
		}

		td, th {
		    border: 1px solid #dddddd;
		    text-align: left;
		    padding: 8px;
		}

		tr:nth-child(even) {
		    background-color: #dddddd;
		}
		</style>
		</head>
		
		<body>
		<h1>Bem Vindo Administrador</h1> </h1> <br>
		<p id="demo">Select an option:</p>
		
		<table>
		%for item in spaces:
		<tr>
		    	<td>ID:{{item["id"]}} </td><td><a href="/web/adminspace/{{item["id"]}}?numID=0"> 
		Name:{{item["name"]}}</a></td><tr>
		%end
		</table>
		<input type="button" value="Voltar" onClick="history.go(-1)"> 
		</body>
		</html>
		""", spaces=spaces)

@bottle.route('/web/adminspace/<r_id>' , method='GET')
def adminspace(r_id):
	numID = request.query['numID']
	response = urllib2.urlopen("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/"+r_id)
	texto=response.read()
	spaces = json.loads(texto)
	return template("""
		<html>
		<head>
		<style>
		table {
    		    font-family: arial, sans-serif;
		    border-collapse: collapse;
		    width: 100%;
		}

		td, th {
		    border: 1px solid #dddddd;
		    text-align: left;
		    padding: 8px;
		}

		tr:nth-child(even) {
		    background-color: #dddddd;
		}
		</style>
		</head>
	

		<body>
		<h1>Welcome Administrator</h1> </h1> <br>
		<p id="demo">Select an option:</p>

		<table>
		%for item in spaces:
			<tr>
			%if item["type"]!="ROOM":
				<td>ID:{{item["id"]}} </td><td> <a href="/web/adminspace/{{item["id"]}}?numID=0"> 
				Name:{{item["name"]}}</a></td><td>{{item["type"]}}<td>
			%else:
				<td>ID:{{item["id"]}}  </td><td> Name:{{item["name"]}} </td><td>
				<button type="button" onclick="freeRoom('{{item["name"]}}', {{item["id"]}})">Libertar Sala</button></td>
			%end
		</tr>
  		%end
  		</table>
  		<input type="button" value="Voltar" onClick="history.go(-1)"> 

		
		<script>
		function freeRoom(name,id){
			var xhttp = new XMLHttpRequest();
			xhttp.onreadystatechange = function() {
  			if (this.readyState == 4 && this.status == 200) {
  				document.getElementById("demo").innerHTML = this.responseText;
   			}
  			};
			
 			xhttp.open("GET", "/addRoom/"+name+"/"+id, true);
  			xhttp.send();
		}
		</script>
		</body>
		</html>
		""", spaces=spaces['containedSpaces'])



# PAGINAS - ALUNO		
@bottle.route('/web/user/<userID>', method = 'GET')
def mainUserPage(userID):
	salas = Sala.query()
	data ={}
	for m in salas:
		data[m.roomId] = m.roomName
	
	return template("""
		<html>
		<head>
		<style>
		table {
    		    font-family: arial, sans-serif;
		    border-collapse: collapse;
		    width: 100%;
		}

		td, th {
		    border: 1px solid #dddddd;
		    text-align: left;
		    padding: 8px;
		}

		tr:nth-child(even) {
		    background-color: #dddddd;
		}
		</style>
		</head>
	
	
		<body>
		<h1>Available Rooms</h1> </h1> <br>
		<p id="demo">Choose a room:</p>
		<input type="button" value="Voltar" onClick="history.go(-1)"> 
		
		<input type="button" value="Check Out"style="float: right" onClick="out('{{userID}}');">
		<table>
		%for item in rooms:
			<tr>
			<td>{{rooms[item]}}  </td><td>{{item}}</td><td>
			<input type="button"  value="Details" onClick="visual({{item}});" /></td><td>
			<input type="button" id={{item}} value="Enter" onClick="action('{{rooms[item]}}',id, '{{userID}}');" /></td></tr>
		%end
		
		
		<script>
		var hidden= false;
  		function action(name,id, userID) 
  		{
  		if (hidden)
  			{
        		document.getElementById(hidden).style.visibility = 'visible';
        		}
           	document.getElementById(id).style.visibility = 'hidden';
        	hidden = id;

    		var xhttp = new XMLHttpRequest();
		xhttp.onreadystatechange = function() {
  		if (this.readyState == 4 && this.status == 200) {
  			document.getElementById("demo").innerHTML = this.responseText;
   			}
  			};
    		xhttp.open("GET", "/enterRoom/"+name+"/"+id+"/"+userID, true);
  		xhttp.send();
  		}
  		
  		function visual(id)
  		{
  		window.open ("http://localhost:8080/detailRoom/"+ id,"mywindow",'_blank',"width=500,height=100");
  		}
  		
  		function out(userID)
  		{
  		document.getElementById(hidden).style.visibility = 'visible';
  		hidden= false;
  		
    		
    		var xhttp = new XMLHttpRequest();
		xhttp.onreadystatechange = function() {
  		if (this.readyState == 4 && this.status == 200) {
  			document.getElementById("demo").innerHTML = this.responseText;
   			}
  			};
 		xhttp.open("GET", "/outRoom/"+userID, true);
  		xhttp.send();

  		}
		</script>
		</body>
		</html>
		""", rooms=data, userID=userID)

	
	
#WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW	
	
	
@bottle.route('/addRoom/<s>/<r_id:int>', method='GET')
def addRoom(s,r_id):
	m = Sala(roomName = s, roomId=r_id)
	key = m.put()
	return 'A sala %s ficou agora livre' %(s)
	
	
	
@bottle.route('/enterRoom/<s>/<room_id:int>/<user_id:int>', method='GET')
def enterRoom(s,room_id, user_id):
	profiles=Check.query(Check.userId==user_id)
        for g in profiles:
		g.key.delete()
		
	r = Check(roomId = room_id, userId=user_id)
	key = r.put()
	
	return 'Entrou na sala: %s (%s) ' %(s,str(room_id))
	
	
	
@bottle.route('/detailRoom/<room_id:int>', method='GET')
def detailRoom(room_id):
	ret = "Actual students in the room:<br>"
	alunos=Check.query(Check.roomId==room_id)
        for al in alunos: 
		ret += str(al.userId) +"<br>"
	return ret

@bottle.route('/outRoom/<user_id:int>', method='GET')
def outRoom(user_id):
	profiles=Check.query(Check.userId==user_id)
        for g in profiles:
		g.key.delete()
	
	return 'Check out bem sucedido '



# Define an handler for 404 errors.
@bottle.error(404)
def error_404(error):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.'

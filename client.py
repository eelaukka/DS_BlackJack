import socket
import struct
import threading
import json
import os

def server():
	UDP_IP = "127.0.0.1"
	UDP_PORT = 5006
	global sock
	global response
	global ingame
	global yourTurn
	sock.settimeout(45)
	while True:
		data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
		response = json.loads(data.decode())
		if os.name == 'nt':
			os.system('CLS')
		if os.name == 'posix':
			os.system('clear')
		#join game response, 1=success
		print(response.get("message"))
		print("==============================\n\n")
		print("Commands:\n 0 = Joingame\n 1 = Hit\n 2 = Stand\n 3 = Quit\n")
		if (response.get("id")==0):
			if (response.get("status")=="success"):
				ingame=True
				if (response.get("playerAmount")==1):
					print("Server waiting for game to start...")
				else:
					print("2 Players ingame, starting game...")
				response={"id" : 0, "status" : "success"}
				s = json.dumps(response).encode()
				sock.sendto(s, ( addr[0], addr[1] ))
				print ("Liityit peliin")
			else:
				print ("Full game or no work")
				joinGame()
		elif (response.get("id")==1): #hit response from server
			#
			print("hitted")
		elif (response.get("id")==2): #stand response from server
			#
			print(response.get("message")) # quit response
		elif (response.get("id")==3):
			#
			print("quit")
		elif (response.get("id")==4): #error response, server waiting for someone else
			print(response.get("message"))
		elif (response.get("id")==6): #state response, gives info for state
			if (response.get("state")=="dealing"):
				print("Game started, dealer dealing")
			elif (response.get("state")=="yourturn"):
				yourTurn=True
			elif (response.get("state")=="endOfTurn"):
				yourTurn=False
				print("Your turn ended.")
			response={"id" : 6, "status" : "success"}
			s = json.dumps(response).encode()
			sock.sendto(s, ( addr[0], addr[1] ))

		
UDP_IP = "127.0.0.1"
UDP_PORT_SERVER = 5005
UDP_PORT = 5006
#UDP_PORT=int(input("ana portti"))
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
for i in range(0, 3):
	try:
		sock.bind((UDP_IP, UDP_PORT+i))
	except OSError:
		continue

t = threading.Thread(target=server)
t.start()
print ("UDP target IP:", UDP_IP)
print ("UDP target port:", UDP_PORT_SERVER)

def joinGame(server_ip=UDP_IP):
	#server_ip=input("Anna palvelimen IP osoite: ")
	print ("Joining game...")
	print ("--------------------------\n\n")
	try:
		request={"id" : 0}
		data=json.dumps(request)
		sock.sendto(data.encode(), (server_ip, UDP_PORT_SERVER))
		#print(sock)
	except:
		joinGame()
		
def sendHitRequest(server_ip):
	try:
		request={"id" : 1}
		data=json.dumps(request)
		sock.sendto(data.encode(), (server_ip, UDP_PORT_SERVER))
	except:
		sendHitRequest(server_ip)
		
def sendStandRequest(server_ip):
	try:
		request={"id" : 2}
		data=json.dumps(request)
		sock.sendto(data.encode(), (server_ip, UDP_PORT_SERVER))
	except:
		sendHitRequest(server_ip)
		
def sendExitMessage(server_ip):
	try:
		request={"id" : 3}
		data=json.dumps(request)
		sock.sendto(data.encode(), (server_ip, UDP_PORT_SERVER))
	except:
		sendHitRequest(server_ip)

server_ip='127.0.0.1'
response=""
ingame=False
yourTurn=False
commands = {0 : joinGame,
           1 : sendHitRequest,
           2 : sendStandRequest,
           3 : sendExitMessage,
}
while True:
	if (yourTurn or not ingame):
		try:
			command=int(input("give command: "))
			
			try:
				commands[command](server_ip)
			except KeyError:
				print("Give a proper command")
			print("\n\n")
		except ValueError:
			continue
		command=None
#message = ""
#message += struct.pack("i",4)
#message += struct.pack("i",3)
#sock.sendto(message, (UDP_IP, UDP_PORT_SERVER))
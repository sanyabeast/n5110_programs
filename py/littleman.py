import logging

from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout

import time
import xml
import sys
import os
import json
import requests
from subprocess import check_output

__dirname__ = os.path.dirname(os.path.abspath(__file__))
__rootdir__ = os.path.normpath(__dirname__ + "/..") + "/"

with open(__rootdir__ + "config.json") as config_json:  
    config = json.load(config_json)

authorized = config["littleman"]["authorized"]

class EchoBot(ClientXMPP):

    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.onmessage)
        self.add_event_handler("diconnected", self.ondisconnect)
        self.add_event_handler("connected", self.onconnect)

    def ondisconnect(self, event):
        print("diskonnected")

    def onconnect(sefl, event):
        xmpp.say_good_morning()


    def session_start(self, event):
        self.send_presence()
        self.get_roster()


    def onmessage(self, msg):
        if (msg["type"] in ("chat", "normal")):
            addresserJID = str(msg["from"]).split("/")[0]
            
        if addresserJID in authorized:
            try:
                self.processMessage(msg)
            except Exception, e:
                print(str(e))

    def processMessage(self, msg):
        command = msg["body"]

        if command.lower() == "reboot":
            msg.reply("Good night!").send()
            check_output(["reboot"])
            return True
            
        if command.lower() == "ip":
            msg.reply(check_output(["hostname", "-I"])).send()
            return True 
            
        if command.lower() == "extip":
            ip = "failed"
            
            try:
                ip = requests.get("https://api.myip.com").json()["ip"]
            except Exception, e:
                print(str(e))
                
            msg.reply(ip).send()
            return True
            
        if command.lower() == "exit":
            msg.reply("Bye").send()
            sys.exit()
            return True 
            
        if command.lower() == "shutup":
            msg.reply("Bye").send()
            check_output(["shutdown", "-h", "now"]) 
            return True

        if command.strip().lower().startswith("run"):
            command = command.strip()
            command = command[4:len(command)]
            output = "no output"

            try:
                print(command.split(" "))
                output = check_output(command.split(" "))
            except Exception, e:
                output = str(e)

            msg.reply(output).send()
            return True


        msg.reply("Unknown command: \n%(body)s"  % msg).send()
        return False	


    def say_good_morning(self):
        print("Salute!")

        for jid in authorized:
            print(jid)
            self.send_message(mto=jid, mbody="Salute!", mtype="chat")

if __name__ == "__main__":
    
    timeout = 1.0
    while ( check_output(["hostname", "-I"])=="\n" ):
        timeout = timeout * 2.0
        if (timeout > 60.0):
            timeout = 60.0
            
        print(timeout)
        time.sleep(5.0)

    xmpp = EchoBot(config["littleman"]["creds"][0], config["littleman"]["creds"][1])    
    xmpp.connect()   
    xmpp.process(block=True)


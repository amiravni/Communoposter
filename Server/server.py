import SimpleHTTPServer, SocketServer
import urlparse
import sys
from db_api import db_handler
import json
import traceback
import random

PORT = int(sys.argv[1])



class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    
    my_db_handler = db_handler()
    
    def setup(self):
        "Sets a timeout on the socket"
        self.request.settimeout(10)
        SimpleHTTPServer.SimpleHTTPRequestHandler.setup(self)
    
    def do_GET(self):
    
       # Parse query data & params to find out what was passed
        parsedParams = urlparse.urlparse(self.path)
        queryParsed = urlparse.parse_qs(parsedParams.query)
       

        if parsedParams.path ==  "/map":
           self.showMap(queryParsed)
        elif parsedParams.path == "/getCompostersJson":
            self.getCompostersJson()
        elif parsedParams.path == "/updateComposterReadings":
            self.upadteComposterReadings(queryParsed)
        elif parsedParams.path == "/shouldOpenDoor":
            self.shouldOpenDoor(queryParsed)
        elif parsedParams.path == "/openUpDoor":
            self.openUpDoor(queryParsed)
        elif parsedParams.path == "/closeUpDoor":
            self.closeUpDoor(queryParsed)
        elif parsedParams.path == "/openDownDoor":
            self.openDownDoor(queryParsed)
        elif parsedParams.path == "/closeDownDoor":
            self.closeDownDoor(queryParsed)
        elif parsedParams.path == "/getCompostReadings":
            self.getCompostReadings(queryParsed)
        elif parsedParams.path == "/plotCompostData":
            self.plotCompostData(queryParsed)

        else:
           self.showWelcom(queryParsed)

   
    def showMap(self,query):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
       
        map_html = open('./site/map.html','r').read()
        self.wfile.write(map_html)
        self.wfile.close()
        
        
    def getCompostersJson(self):
        composters = self.my_db_handler.get_composters()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        self.wfile.write(json.dumps(composters))
        self.wfile.close()
        
        
    def shouldOpenDoor(self,query):
        try:
            composter_id = int(query['id'][0])
            mycomposter = self.my_db_handler.get_composters_by_id(composter_id)  
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            
            self.wfile.write(str(mycomposter['up_door_status']) + ' ' + str(mycomposter['down_door_status']))
            self.wfile.close()
        except:
            traceback.print_exc(file=sys.stdout)
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            
            self.wfile.write("Error!")
            self.wfile.close()

    def openUpDoor(self,query):
        try:
            composter_id = int(query['composter_id'][0])
            user_id = int(query['user_id'][0])
            self.my_db_handler.composter_open_up_door(user_id,composter_id)
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            
            self.wfile.write("Thanks")
            self.wfile.close()
        except:
            traceback.print_exc(file=sys.stdout)
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            
            self.wfile.write("Error!")
            self.wfile.close()

    def closeUpDoor(self,query):
        try:
            composter_id = int(query['composter_id'][0])
            user_id = int(query['user_id'][0])
            self.my_db_handler.composter_close_up_door(user_id,composter_id)
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            
            self.wfile.write("Thanks")
            self.wfile.close()
        except:
            traceback.print_exc(file=sys.stdout)
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            
            self.wfile.write("Error!")
            self.wfile.close()

    def openDownDoor(self,query):
        try:
            composter_id = int(query['composter_id'][0])
            user_id = int(query['user_id'][0])
            self.my_db_handler.composter_open_down_door(user_id,composter_id)
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            
            self.wfile.write("Thanks")
            self.wfile.close()
        except:
            traceback.print_exc(file=sys.stdout)
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            
            self.wfile.write("Error!")
            self.wfile.close()

    def closeDownDoor(self,query):
        try:
            composter_id = int(query['composter_id'][0])
            user_id = int(query['user_id'][0])
            self.my_db_handler.composter_close_down_door(user_id,composter_id)
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            
            self.wfile.write("Thanks")
            self.wfile.close()
        except:
            traceback.print_exc(file=sys.stdout)
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            
            self.wfile.write("Error!")
            self.wfile.close()

    def upadteComposterReadings(self,query):
        print query
        try:
            composter_id = int(query['id'][0])
            temp = float(query['temp'][0])
            temp1 = temp
            temp2 = temp + random.random()*2
            temp3 = temp + random.random()*2
            temp4 = temp + random.random()*2
            
            humidity = float(query['humidity'][0])
            humidity1 = humidity + random.random()*2
            humidity2 = humidity + random.random()*2
            humidity3 = humidity + random.random()*2
            humidity4 = humidity + random.random()*2
            
            dist1 =  float(query['dist1'][0])
            dist2 =  float(query['dist2'][0])
            dist3 =  float(query['dist3'][0])
            dist4 =  float(query['dist4'][0])
            
            up_door_status = int(query['up_door_status'][0])
            down_door_status =  int(query['down_door_status'][0])
            
            weight = float(query['weight'][0])
            self.my_db_handler.composter_reading_update(composter_id,
                                                        temp1,temp2,temp3,temp4,
                                                        humidity1,humidity2,humidity3,humidity4,
                                                        dist1,dist2,dist3,dist4,
                                                        0.0,
                                                        up_door_status,down_door_status)
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write("Thanks")
            self.wfile.close()
        except:
            traceback.print_exc(file=sys.stdout)
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write("Error!")
            self.wfile.close()

    def showWelcom(self,query):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
       
        map_html = open('./site/index.html','r').read()
        self.wfile.write(map_html)
        self.wfile.close()


    def getCompostReadings(self,query):
        try:
            composter_id = int(query['id'][0])
            composter_readings = self.my_db_handler.composter_get_last_readings(composter_id)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            self.wfile.write(json.dumps(composter_readings))
            self.wfile.close()
        except:
            traceback.print_exc(file=sys.stdout)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps([]))
            self.wfile.close()

    def plotCompostData(self,query):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
       
        plot_html = open('./site/plot_graphs.html','r').read()
        self.wfile.write(plot_html)
        self.wfile.close()

Handler = MyHandler

httpd = SocketServer.TCPServer(("", PORT), Handler, bind_and_activate=True)
httpd.allow_reuse_address = True

print "serving at port", PORT
httpd.serve_forever()

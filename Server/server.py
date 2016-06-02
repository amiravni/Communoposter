import SimpleHTTPServer, SocketServer
import urlparse
import sys
from db_api import db_handler
import json
import traceback

PORT = int(sys.argv[1])

class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    
    my_db_handler = db_handler()
    
    
    def do_GET(self):
    
       # Parse query data & params to find out what was passed
        parsedParams = urlparse.urlparse(self.path)
        queryParsed = urlparse.parse_qs(parsedParams.query)
       

        if parsedParams.path ==  "/map":
           self.showMap(queryParsed)
        elif parsedParams.path == "/getCompostersJson":
            self.getCompostersJson()
        elif parsedParams.path == "/upadteComposterReadings":
            self.upadteComposterReadings(queryParsed)
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
        
    def upadteComposterReadings(self,query):
        print query
        try:
            composter_id = int(query['id'][0])
            temp = float(query['temp'][0])
            humidity = float(query['humidity'][0])
            door_status = int(query['door_status'][0])
            weight = float(query['weight'][0])
            self.my_db_handler.composter_reading_update(composter_id,temp,humidity,door_status,weight)
            
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
       
        self.wfile.write('<html><head></head><body>Welcome</body></html>')
        self.wfile.close()


Handler = MyHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()
import SimpleHTTPServer, SocketServer
import urlparse
import sys
from db_api import db_handler
import json

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
        
    def getComposterData(self,composter_id)


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
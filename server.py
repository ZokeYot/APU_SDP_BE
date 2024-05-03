import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from dbConnection import *
from Controller.UserController import UserController

class ApiServer(BaseHTTPRequestHandler):
    MYSQL = MySQL_DB()
    MONGO = Mongo_DB()


    UserController = UserController(MYSQL, MONGO)


    # GET Request Endpoint
    def do_GET(self):
        data = [400, json.dumps({"Invalid API Endpoint !!"})]
        if self.path == "/user/all":
            data = self.UserController.get_all_user()

        elif self.path.startswith("/user/find"):
            # Get the path variable
            paths = self.path.split("/")
            id = paths[-1] if len(paths) == 4 and paths[-1].isdigit() else -1
            data = self.UserController.find_user_by_id(id)

        self.sent_response(data)

    # POST Request Endpoint
    def do_POST(self):
        data = [400, json.dumps({"Invalid API Endpoint !!"})]

        if self.path == "/user/create":
            # Get the data from the request body
            content_length = int(self.headers['Content-Length'])
            request_body = self.rfile.read(content_length).decode('utf-8')
            data = self.UserController.create_user(request_body)

        self.sent_response(data)

    # PUT Request Endpoint
    def do_PUT(self):
        data = [400, json.dumps({"Invalid API Endpoint !!"})]

        if self.path.startswith("/user/update/"):
            # Get the data from the reqeust body
            content_length = int(self.headers['Content-Length'])
            request_body = self.rfile.read(content_length).decode('utf-8')

            # Get the path variable
            paths = self.path.split("/")
            id = paths[-1] if len(paths) == 4 and paths[-1].isdigit() else -1
            data = self.UserController.update_user(request_body, id)



        self.sent_response(data)

    # DELETE Request Endpoint
    def do_DELETE(self):
        data = [400, json.dumps({"Invalid API Endpoint !!"})]

        if self.path.startswith("/user/delete/"):
            # Get the path variable
            paths = self.path.split("/")
            id = paths[-1] if len(paths) == 4 and paths[-1].isdigit() else -1
            self.UserController.delete_user(id)


        self.sent_response(data)

    # Set up the header and send response to the client
    def sent_response(self, response):
        self.send_response(response[0])
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', 'http://localhost:4200')
        self.wfile.write(response[1].encode('utf-8'))
        self.end_headers()

# Start a web server 
def main():
    server_address = ('localhost', 8000)
    httpd = HTTPServer(server_address, ApiServer)
    print('Server running on http://{}:{}/'.format(*server_address))
    httpd.serve_forever()

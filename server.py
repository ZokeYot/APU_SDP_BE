import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from Controller import UserController
from Controller import QuizController
from Controller import MessageGroupController
from Controller import MessageController
from Controller import MaterialController
from Controller import GameItemController
from Controller import SubmissionController

class ApiServer(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', 'http://localhost:4200')  # Allow requests from the Angular app
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')  # Allow these HTTP methods
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')  # Allow the Content-Type header
        self.end_headers()


    def do_GET(self):
        response = [500, json.dumps({"failure": "Invalid Url"})]
        if self.path == "/quiz/all":
            response = QuizController.get_quizzes()
        elif self.path == "/material/all":
            response = MaterialController.get_materials()
        elif self.path == "/student/all":
            response = UserController.get_all_student()
        elif self.path == "/user/all":
            response = UserController.get_all_user()

        self.sent_response(response)


    def do_POST(self):
        response = [500, json.dumps({"failure": "Invalid Url"})]

        if self.path == "/user/login":
            response = UserController.login(self.get_request_body())
        elif self.path == "/user/register":
            response = UserController.register(self.get_request_body())
        elif self.path == "/user/profile":
            response = UserController.get_profile(self.get_request_body())
        elif self.path == "/user/update":
            response = UserController.update_profile(self.get_request_body())
        elif self.path == "/quiz/find":
            response = QuizController.get_quiz(self.get_request_body())
        elif self.path == "/quiz/lecturer-quiz":
            response = QuizController.get_lecturer_quizzes(self.get_request_body())
        elif self.path == "/quiz/create":
            response = QuizController.create_quiz(self.get_request_body())
        elif self.path == "/quiz/add-participant":
            response = QuizController.add_participant(self.get_request_body())
        elif self.path == "/quiz/update":
            response = QuizController.update_quiz(self.get_request_body())
        elif self.path == "/quiz/delete":
            response = QuizController.delete_quiz(self.get_request_body())
        elif self.path == "/quiz/join":
            response = QuizController.join_quiz(self.get_request_body())
        elif self.path == "/quiz/check-quiz":
            response = QuizController.find_participant(self.get_request_body())
        elif self.path == "/quiz/participants":
            response = QuizController.get_quiz_participants(self.get_request_body())
        elif self.path == "/quiz/delete-participant":
            response = QuizController.delete_participant(self.get_request_body())
        elif self.path == "/conversation/create-group":
            response = MessageGroupController.create_group(self.get_request_body())
        elif self.path == "/conversation/send":
            response = MessageController.send_message(self.get_request_body())
        elif self.path == "/conversation/send-group":
            response = MessageController.send_group_message(self.get_request_body())
        elif self.path == "/conversation":
            response = MessageController.get_user_messages(self.get_request_body())
        elif self.path == "/conversation/group":
            response = MessageController.get_group_message(self.get_request_body())
        elif self.path == "/conversation/group/info":
            response = MessageGroupController.get_group(self.get_request_body())
        elif self.path == "/conversation/group/update":
            response = MessageGroupController.update_group(self.get_request_body())
        elif self.path == "/conversation/group/delete":
            response = MessageGroupController.delete_group(self.get_request_body())
        elif self.path == "/conversation/group/member/all":
            response = MessageGroupController.get_group_members(self.get_request_body())
        elif self.path == "/conversation/group/member/add":
            response = MessageGroupController.add_members(self.get_request_body())
        elif self.path == "/conversation/group/member/delete":
            response = MessageGroupController.delete_members(self.get_request_body())
        elif self.path == "/material/lecturer":
            response = MaterialController.get_lecturer_materials(self.get_request_body())
        elif self.path == "/material/upload":
            response = MaterialController.add_material(self.get_request_body())
        elif self.path == "/material/download":
            response = MaterialController.download_material(self.get_request_body())
        elif self.path == "/material/delete":
            response = MaterialController.delete_material(self.get_request_body())
        elif self.path == "/game-title/add":
            response = GameItemController.add_title(self.get_request_body())
        elif self.path == "/game-item/buy":
            response = GameItemController.add_item(self.get_request_body())
        elif self.path == "/game-item/use":
            response = GameItemController.use_item(self.get_request_body())
        elif self.path == "/user/titles":
            response = GameItemController.get_titles(self.get_request_body())
        elif self.path == "/submission/all":
            response = SubmissionController.get_submissions(self.get_request_body())
        elif self.path == "/submission/find":
            response = SubmissionController.get_submission(self.get_request_body())
        elif self.path == "/submission/add":
            response = SubmissionController.add_submission(self.get_request_body())


        self.sent_response(response)




    # Set up the header and send response to the client
    def sent_response(self, response):
        self.send_response(response[0])
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', 'http://localhost:4200')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.end_headers()
        self.wfile.write(response[1].encode('utf-8'))


    def get_request_body(self):
        content_length = int(self.headers['Content-Length'])
        request_body = self.rfile.read(content_length).decode('utf-8')
        return request_body

    def get_path_variable(self):
        paths = self.path.split("/")
        pathVariable = paths[-1] if len(paths) == 4 and paths[-1].isdigit() else -1
        return pathVariable;

# Start a web server 
def main():
    server_address = ('localhost', 8000)
    httpd = HTTPServer(server_address, ApiServer)
    print('Server running on http://{}:{}/'.format(*server_address))
    httpd.serve_forever()

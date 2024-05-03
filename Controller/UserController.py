from Service.UserService import UserService
import json


class UserController:
    def __init__(self, MySQL, Mongo):
        self.UserService = UserService(MySQL, Mongo)

    ### Get
    # Get All User
    def get_all_user(self):
        data = self.UserService.get_all_user()

        return [200, json.dumps(data)]

    # Get Specific User with the ID
    def find_user_by_id(self, id):
        try:
            if id == -1:
                raise ValueError("Invalid Url Parameter !!")

            data = self.UserService.find_user_by_id(id)

            return [200, json.dumps(data)]

        except ValueError as e:
            response = [400, json.dumps({f"error": str(e)})]
            return response

    ### Post
    # Create User
    def create_user(self, request_body):
        data = json.loads(request_body)
        status_code = 201
        response = {"success": "User Created Successfully"}
        try:
            result = self.UserService.create_user(data)

            if not result:
                status_code = 500
                response = {"error": "Failed to create user"}

            return [status_code, json.dumps(response)]
        except ValueError as e:
            return [400, json.dumps({"error": str(e)})]


    def user_login(self, request_body):
        data = json.loads(request_body)
        status_code = 200
        response = {"success": "Log in successfully"}
        try:
            self.UserService.user_login(data)

            return [status_code, response]
        except ValueError as e:
            return [400, json.dumps({"error": str(e)})]



    ### Put
    # Update User
    def update_user(self, request_body, id):
        data = json.loads(request_body)
        result = self.UserService.update_user(data, id)
        response = {"success": "User information update successfully"}
        status_code = 200

        if not result:
            status_code = 400
            response = {"error": "Failed to update user information"}

        return [status_code, response]

    ### Delete
    # Delete User
    def delete_user(self, id):
        try:
            if id == -1:
                raise ValueError('Invalid Url Parameter !!')

            result = self.UserService.delete_user(id)
            response = {"success": "User deleted"}
            status_code = 200

            if not result:
                status_code = 400
                response = {"error": "Failed to delete user"}

            return [status_code, response]

        except ValueError as e:
            return [400, {"error": str(e)}]

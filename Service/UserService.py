class UserService:
    def __init__(self, MySQL, Mongo):
        self.MySQL = MySQL
        self.Mongo = Mongo
        self.cursor = MySQL.cursor


    def get_all_user(self):
        query = "SELECT * FROM User"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        data = []
        for row in rows:
            user = {
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "password": row[3],
                "gender": row[4],
                "profile_picture": "null",
                "dob": str(row[6]),
                "isLecturer": row[7],
                "isStudent": row[8]
            }
            data.append(user)

        return data

    def find_user_by_id(self , id):
        query = "SELECT * FROM User Where User_ID = %s "
        self.cursor.execute(query, [id])
        rows = self.cursor.fetchall()

        if not rows:
            raise ValueError("Invalid User ID !! ")

        for row in rows:
            user = {
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "password": row[3],
                "gender": row[4],
                "profile_picture": "null",
                "dob": str(row[6]),
                "isLecturer": row[7],
                "isStudent": row[8]
            }
            return user



    def create_user(self, data):
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        gender = data.get('gender')
        dob = data.get('dob')
        isLecturer = data.get('isLecturer')
        isStudent = data.get('isStudent')

        self.cursor.execute("SELECT * FROM User Where Email = %s", [email])

        if self.cursor.fetchall():
            raise ValueError(f"The email {email} have been used !!")

        try:
            query = "INSERT INTO User(Name, Email, Password, Gender, DOB, isLecturer, isStudent) " \
                    "VALUES(%s , %s , %s , %s, %s , %s , %s)"
            self.cursor.execute(query, (name, email, password, gender, dob, isLecturer, isStudent))
            self.MySQL.connection.commit()
            return True

        except self.MySQL.error as e:
            print(e)
            return False

    def user_login(self, data):
        query = "SELECT Password FROM User WHERE Email = %s"

        email = data.get('email')
        password = data.get('password')

        result = self.cursor.execute(query, [email])

        if not result:
            raise ValueError("User Credential Not Found")

        if result[0] != password:
            raise ValueError("Wrong Password !!")

        return True

    def update_user(self, data, id):
        query = "UPDATE User SET" \
                "Name =  %" \
                "Gender = %s," \
                "DOB = %s," \
                "Profile_Picture = %s" \
                "WHERE USer_ID  = %i"

        name = data.get('name')
        gender = data.get('gender')
        dob = data.get('dob')
        profile = data.get('profile_picture')

        try:
            self.cursor.execute(query, (name, gender, dob, profile, id))
            self.MySQL.connection.commit()
            return True

        except self.MySQL.error as e:
            print(e)
            return False

    def delete_user(self, id):
        query = "DELETE FROM User WHERE User_ID = %i"

        try:
            self.cursor.execute(query, [id])
            self.MySQL.connection.commit()
            return True

        except self.MySQL.error as e:
            print(e)
            return False



    






import base64
import json
import dbConnection


def login(request_body):
    try:
        data = json.loads(request_body)

        email = data.get('email')
        password = data.get('password')

        query = "SELECT * FROM User  Where Email = %s"
        dbConnection.cursor.execute(query, [email])
        row = dbConnection.cursor.fetchone()

        if row is None:
            raise ValueError('User Not Found')
        if row[3] != password:
            raise ValueError('Wrong Password')

        role = "lecturer" if row[7] == 1 else "student"
        amount = 0
        if role == "student":
            dbConnection.cursor.execute("SELECT Amount FROM Student_Items WHERE Student_ID = %s", [row[0]])
            result = dbConnection.cursor.fetchone()
            amount = result[0] if result else 0
        return [200, json.dumps({"userID": row[0], "role": role, "item_amount":amount})]
    except (ValueError, dbConnection.error) as e:
        return [500, json.dumps({"failure": str(e)})]


def register(request_body):
    try:
        data = json.loads(request_body)

        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        gender = data.get('gender')
        dob = data.get('dob')
        profile_picture = base64.b64decode(data.get('profile_picture'))
        lectureKey = data.get('lectureKey')
        isLecturer = 1 if lectureKey == "APULecturer101" else 0
        isStudent = 0 if lectureKey == "APULecturer101" else 1

        query = "INSERT INTO User (Name, Email, Password, Gender, DOB, Profile_Picture, isLecturer, isStudent, Title)" \
                "VALUES( %s, %s, %s, %s, %s, %s, %s, %s, 'Beginner')"
        dbConnection.cursor.execute(query, (name, email, password, gender, dob, profile_picture, isLecturer, isStudent))
        dbConnection.connection.commit()

        return [200, json.dumps({"success": "New User Registered Successfully"})]

    except (ValueError, dbConnection.error) as e:
        return [500, json.dumps({"failure": str(e)})]


def get_all_student():
    try:
        dbConnection.cursor.execute("SELECT * FROM User WHERE isStudent = 1")
        result = dbConnection.cursor.fetchall()

        students = []
        for row in result:
            student = {
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "password": row[3],
                "gender": row[4],
                "profile_picture": base64.b64encode(row[5]).decode('utf-8'),
                "dob": str(row[6]),
                "title": row[9]
            }

            students.append(student)
        return [200, json.dumps(students)]
    except (ValueError, dbConnection.error) as e:
        return [500, json.dumps({"failure": str(e)})]


def update_profile(request_body):
    try:
        data = json.loads(request_body)

        userID = data.get('id')
        name = data.get('name')
        gender = data.get('gender')
        dob = data.get('dob')
        password = data.get('password')
        profile_picture = base64.b64decode(data.get('profile_picture'))
        title = data.get('title')

        query = "UPDATE User SET " \
                "Name =  %s," \
                "Gender = %s," \
                "DOB = %s," \
                "Password = %s, " \
                "Profile_Picture = %s," \
                "Title = %s " \
                "WHERE User_ID  = %s"

        dbConnection.cursor.execute(query, (name, gender, dob, password, profile_picture, title, userID))
        dbConnection.connection.commit()

        return [200, json.dumps({"success": "Update Successfully"})]

    except ValueError as e:
        return [500, json.dumps({"failure": str(e)})]
    except dbConnection.error as e:
        return [500, json.dumps({"failure": str(e)})]


def get_profile(request_body):
    try:
        data = json.loads(request_body)
        userID = data.get('userID')
        query = "SELECT u.*, Amount FROM User u Left Join Student_Items s on u.User_ID = s.Student_ID " \
                "WHERE u.User_ID = %s"

        dbConnection.cursor.execute(query, [userID])
        row = dbConnection.cursor.fetchone()

        if row is None:
            raise ValueError("User Not Found")

        user = {
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "password": row[3],
            "gender": row[4],
            "profile_picture": base64.b64encode(row[5]).decode('utf-8'),
            "dob": str(row[6]),
            "title": row[9],
            "gaming_point": row[10],
            "item_amount": row[11] if row[11] else 0
        }
        return [200, json.dumps(user)]
    except (dbConnection.error, ValueError) as e:
        return [500, json.dumps({"failure": str(e)})]


def get_all_user():
    dbConnection.cursor.execute("SELECT * FROM User")
    result = dbConnection.cursor.fetchall()

    users = []
    for row in result:
        role = "lecturer" if row[7] == 1 else "student"
        user = {
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "password": row[3],
            "gender": row[4],
            "profile_picture": base64.b64encode(row[5]).decode('utf-8'),
            "dob": str(row[6]),
            "role": role,
            "title": row[9]
        }


        users.append(user)
    return [200, json.dumps(users)]

import base64
import json
import dbConnection


def create_quiz(requestBody):
    try:
        data = json.loads(requestBody)
        title = data.get('title')
        admin = data.get('quizAdmin')
        createDate = data.get('createDate')
        description = data.get('description')
        thumbnail = base64.b64decode(data.get('thumbnail'))
        questions = json.dumps(data.get('questions'))

        query = "INSERT INTO Quiz(Title, Quiz_Admin, Create_Date, Description, Thumbnail, Questions)" \
                "VALUES(%s, %s, %s, %s, %s, %s)"
        dbConnection.cursor.execute(query, (title, admin, createDate, description, thumbnail, questions))
        dbConnection.connection.commit()

        return [200, json.dumps({"success": "Quiz Created Successfully"})]
    except (ValueError, dbConnection.error) as e:
        return [500, json.dumps({f"failure": str(e)})]


def update_quiz(requestBody):
    try:
        data = json.loads(requestBody)
        quizID = data.get('quizID')
        title = data.get('title')
        description = data.get('description')
        thumbnail = base64.b64decode(data.get('thumbnail'))
        questions = json.dumps(data.get('questions'))

        query = "UPDATE Quiz SET Title = %s, Description = %s, Thumbnail = %s, Questions = %s" \
                "WHERE Quiz_ID = %s"

        dbConnection.cursor.execute(query, (title, description, thumbnail, questions, quizID))
        dbConnection.connection.commit()

        return [200, json.dumps({"success": "Quiz Updated Successfully"})]
    except (ValueError, dbConnection.error) as e:
        return [500, json.dumps({f"failure": str(e)})]


def get_quiz_participants(requestBody):
    try:
        quizID = json.loads(requestBody).get('quizID')
        dbConnection.cursor.execute("SELECT u.* FROM Quiz_Participants qp Join User u "
                                    "ON qp.Participant_ID = u.User_ID WHERE Quiz_ID = %s", [quizID])

        result = dbConnection.cursor.fetchall()
        participants = []
        for row in result:
            participant = {
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "gender": row[4],
                "profile_picture": base64.b64encode(row[5]).decode('utf-8'),
                "dob": str(row[6]),
                "title": row[9]
            }
            participants.append(participant)

        return [200, json.dumps(participants)]
    except (ValueError, dbConnection.error) as e:
        return [500, json.dumps({f"failure": str(e)})]
def add_participant(requestBody):
    try:
        data = json.loads(requestBody)
        quizID = data.get('quizID')
        participants = data.get('participants')

        query = "INSERT INTO Quiz_Participants(Quiz_ID, Participant_ID)" \
                "VALUES(%s, %s)"

        for participant in participants:
            studentID = participant.get('studentID')
            dbConnection.cursor.execute("SELECT * FROM Quiz_Participants WHERE Quiz_ID = %s AND Participant_ID = %s", (quizID, studentID))
            if dbConnection.cursor.fetchone():
                continue
            if studentID:
                dbConnection.cursor.execute(query, (quizID, studentID))

        dbConnection.connection.commit()

        return [200, json.dumps({"success": "All participants added to quiz successfully"})]
    except (ValueError, dbConnection.error) as e:
        return [500, json.dumps({"failure": str(e)})]


def delete_participant(requestBody):
    try:
        data = json.loads(requestBody)
        quiz_id = data.get('quizID')
        participants = data.get('participants')

        query = "DELETE FROM Quiz_Participants WHERE Quiz_ID = %s AND Participant_ID = %s"

        for participant in participants:
            studentID = participant.get('studentID')
            if studentID:
                dbConnection.cursor.execute(query, (quiz_id, studentID))

        dbConnection.connection.commit()
        return [200, json.dumps({"success": "Participants removed from quiz successfully"})]
    except (ValueError, dbConnection.error) as e:
        return [500, json.dumps({"failure": str(e)})]


def join_quiz(requestBody):
    try:
        data = json.loads(requestBody)
        userID = data.get('userID')
        quizID = data.get('quizID')

        query = "INSERT INTO Quiz_Participants(Quiz_ID, Participant_ID)" \
                "VALUES(%s, %s)"

        dbConnection.cursor.execute(query, (quizID, userID))
        dbConnection.connection.commit()

        return [200, json.dumps({"success": "Joined Quiz Successfully"})]
    except (ValueError, dbConnection.error) as e:
        return [500, json.dumps({"failure": str(e)})]


def find_participant(requestBody):
    try:
        data = json.loads(requestBody)
        userID = data.get('userID')
        quizID = data.get('quizID')

        dbConnection.cursor.execute("SELECT * FROM Quiz_Participants WHERE Quiz_ID = %s AND Participant_ID = %s",
                                    (quizID, userID))

        result = dbConnection.cursor.fetchone()

        if not result:
            return [200, json.dumps({"success" : "ok"})]
        else:
            raise ValueError('Student Already Joined')
    except (ValueError, dbConnection.error) as e:
        return [500, json.dumps({"failure": str(e)})]


def get_quizzes():
    try:
        dbConnection.cursor.execute("SELECT Quiz.*, User.Name FROM Quiz join User ON Quiz.Quiz_Admin = User.User_ID")
        result = dbConnection.cursor.fetchall()
        quizzes = []

        for row in result:
            quiz = {
                "quizID": row[0],
                "title": row[1],
                "quizAdmin": row[2],
                "adminName": row[7],
                "createDate": str(row[3]),
                "description": row[4],
                "thumbnail": base64.b64encode(row[5]).decode('utf-8'),
                "questions": json.loads(row[6])
            }
            quizzes.append(quiz)

        return [200, json.dumps(quizzes)]
    except (ValueError, dbConnection.error) as e:
        return [500, json.dumps({"failure": str(e)})]


def get_quiz(requestBody):
    try:
        data = json.loads(requestBody)
        quizID = data.get('quizID')

        query = "SELECT Quiz.* , User.Name FROM Quiz JOIN User ON Quiz.Quiz_Admin = User.User_ID WHERE Quiz_ID = %s"
        dbConnection.cursor.execute(query, [quizID])
        result = dbConnection.cursor.fetchone()

        if result is None:
            raise ValueError("Quiz Not Found")

        quiz = {
            "quizID": result[0],
            "title": result[1],
            "quizAdmin": result[2],
            "adminName": result[7],
            "createDate": str(result[3]),
            "description": result[4],
            "thumbnail": base64.b64encode(result[5]).decode('utf-8'),
            "questions": json.loads(result[6])
        }

        return [200, json.dumps(quiz)]
    except (ValueError, dbConnection.error) as e:
        return [500, json.dumps({"failure": str(e)})]


def get_lecturer_quizzes(requestBody):
    try:
        lecturerID = json.loads(requestBody).get('lecturerID')
        dbConnection.cursor.execute("SELECT Quiz.* , User.Name FROM Quiz JOIN User "
                                    "ON Quiz.Quiz_Admin = User.User_ID WHERE Quiz_Admin = %s", [lecturerID])
        result = dbConnection.cursor.fetchall()
        quizzes = []

        for row in result:
            quiz = {
                "quizID": row[0],
                "title": row[1],
                "quizAdmin": row[2],
                "adminName": row[7],
                "createDate": str(row[3]),
                "description": row[4],
                "thumbnail": base64.b64encode(row[5]).decode('utf-8'),
                "questions": json.loads(row[6])
            }
            quizzes.append(quiz)

        return [200, json.dumps(quizzes)]
    except (ValueError, dbConnection.error) as e:
        return [500, json.dumps({"failure": str(e)})]


def delete_quiz(requestBody):
    try:
        quizID = json.loads(requestBody).get('quizID')
        dbConnection.cursor.execute("DELETE FROM Quiz WHERE Quiz_ID = %s", [quizID])
        dbConnection.connection.commit()
        return [200, json.dumps({"success": "ok"})]
    except (ValueError, dbConnection.error) as e:
        return [500, json.dumps({"failure": str(e)})]

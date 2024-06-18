import base64

import dbConnection
import json


def add_submission(requestBody):
    try:
        data = json.loads(requestBody)

        studentID = data.get('studentID')
        quizID = data.get('quizID')
        completeDate = data.get('completeDate')
        response = json.dumps(data.get('response'))
        score = data.get('score')

        query = "INSERT INTO Submission(Student_ID, Quiz_ID, Completed_Date, Response, Score)" \
                "VALUES(%s, %s, %s, %s, %s)"

        dbConnection.cursor.execute(query, (studentID, quizID, completeDate, response, score))
        dbConnection.connection.commit()

        dbConnection.cursor.execute("UPDATE User SET GamingPoint = GamingPoint + %s WHERE User_ID = %s", (score, studentID))

        return [200, json.dumps({"success": "Quiz Submission Added"})]
    except (ValueError, dbConnection.error) as e:
        return [500, json.dumps({"failure": str(e)})]


def get_submissions(requestBody):
    try:
        quizID = json.loads(requestBody).get('quizID')
        query = "SELECT s.Submission_ID, s.Quiz_ID, s.Student_ID, u.Name, u.Profile_Picture, s.Completed_Date, s.Response, s.Score " \
                "FROM Submission s Join ( Select Student_ID , Min(Submission_ID) as FirstSubmission from Submission " \
                "WHERE Quiz_ID = %s GROUP BY Student_ID) first_submission " \
                "ON s.Student_ID = first_submission.Student_ID AND " \
                "s.Submission_ID = first_submission.FirstSubmission join User u on s.Student_ID = u.User_ID " \
                " WHERE s.Quiz_ID = %s"

        dbConnection.cursor.execute(query, [quizID, quizID])
        result = dbConnection.cursor.fetchall()

        submissions = []
        for row in result:
            submission = {
                "submissionID": row[0],
                "quizID": row[1],
                "studentID": row[2],
                "studentName": row[3],
                "profile_picture": base64.b64encode(row[4]).decode('utf-8'),
                "completedDate": str(row[5]),
                "response": json.loads(row[6]),
                "score": row[7]
            }

            submissions.append(submission)
        return [200, json.dumps(submissions)]
    except (ValueError, dbConnection.error) as e:
        return [500, json.dumps({"failure": str(e)})]

def get_submission(requestBody):
    try:
        submissionID = json.loads(requestBody).get('submissionID')
        dbConnection.cursor.execute("SELECT * FROM Submission WHERE Submission_ID = %s", [submissionID])
        result = dbConnection.cursor.fetchone()

        submission = {
            "submissionID": result[0],
            "studentID": result[1],
            "quizID": result[2],
            "completedDate": str(result[3]),
            "response": json.loads(result[4]),
            "score": result[5]
        }

        return [200, json.dumps(submission)]
    except (ValueError, dbConnection.error) as e:
        return [500, json.dumps({"failure": str(e)})]

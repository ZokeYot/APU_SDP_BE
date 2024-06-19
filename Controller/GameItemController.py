import random

import dbConnection
import json


def get_titles(requestBody):
    try:
        userID = json.loads(requestBody).get('userID')

        query = "SELECT Titles FROM Student_Title WHERE Student_ID = %s"
        dbConnection.cursor.execute(query, [userID])

        result = dbConnection.cursor.fetchone()

        return [200, json.dumps(json.loads(result[0]))]


    except (ValueError, dbConnection.error) as e:
        return [500, json.dumps({"failure": str(e)})]

def add_title(requestBody):
    try:
        data = json.loads(requestBody)
        userID = data.get('userID')
        title = data.get('title')

        dbConnection.cursor.execute("SELECT Titles FROM Student_Title WHERE Student_ID = %s", [userID])
        result = dbConnection.cursor.fetchone()

        if result:
            titles = json.loads(result[0])

            if not any(entry["title"] == title for entry in titles):
                titles.append({'title': title})
                query = "UPDATE Student_Title SET Titles = %s WHERE Student_ID = %s"
                dbConnection.cursor.execute(query, (json.dumps(titles), userID))
        else:
            titles = [{"title": title}]
            query = "INSERT INTO Student_Title (Student_ID, Titles) VALUES (%s, %s)"
            dbConnection.cursor.execute(query, (userID, json.dumps(titles)))

        dbConnection.cursor.execute("Update User SET GamingPoint = GamingPoint - 500 WHERE User_ID = %s", [userID])
        dbConnection.connection.commit()
        return [200, json.dumps({"success": f"Title {title} added to ur inventory "})]

    except (ValueError, dbConnection.error) as e:
        return [500, json.dumps({"failure": str(e)})]


def add_item(requestBody):
    try:
        data = json.loads(requestBody)

        userID = data.get('userID')
        amount = data.get('amount')

        dbConnection.cursor.execute("SELECT * FROM Student_Items WHERE Student_ID = %s", [userID])
        if dbConnection.cursor.fetchone():
            query = "UPDATE Student_Items SET Amount = Amount + %s WHERE Student_ID = %s"
            dbConnection.cursor.execute(query, [amount, userID])
        else:
            query = "INSERT INTO Student_Items(Student_ID, Item_ID, Amount)" \
                    "VALUES(%s, 1, %s)"
            dbConnection.cursor.execute(query, (userID, amount))

        number = 500 * int(amount)
        dbConnection.cursor.execute("UPDATE User SET GamingPoint = GamingPoint - %s WHERE User_ID = %s", (number, userID))
        dbConnection.connection.commit()
        return [200, json.dumps({"success": "ok"})]
    except (ValueError, dbConnection.error) as e:
        return [500, json.dumps({"failure": str(e)})]


def use_item(requestBody):
    try:
        data = json.loads(requestBody)
        userID = data.get('userID')

        query = "UPDATE Student_Items SET Amount = Amount - 1 WHERE Student_ID = %s"
        dbConnection.cursor.execute(query,[userID])
        dbConnection.connection.commit()

        return [200, json.dumps({"success": "ok"})]
    except (ValueError, dbConnection.error) as e:
        return [500, json.dumps({"failure": str(e)})]

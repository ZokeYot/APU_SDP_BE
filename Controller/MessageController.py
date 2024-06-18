import base64
import collections

import dbConnection
import json


def get_user_messages(requestBody):
    try:
        userID = json.loads(requestBody).get('userID')
        dbConnection.cursor.execute("SELECT * FROM Messages WHERE Sender_ID = %s OR Receiver_ID = %s", [userID, userID])

        result = dbConnection.cursor.fetchall()
        conversations = collections.defaultdict(list)
        other_userID = 0
        for row in result:
            senderID = row[1]
            receiverID = row[2]
            date = row[3]
            content = row[4]



            conversation = {
                "senderID": senderID,
                "receiverID": receiverID,
                "date": str(date),
                "content": content
            }
            conversations[other_userID].append(conversation)

        output = []
        for other_userID, messages in conversations.items():
            output.append({
                "userID": other_userID,
                "conversation": messages
            })

        return [200, json.dumps(output)]
    except (ValueError, dbConnection.error) as e:
        return [500, json.dumps({"failure": str(e)})]

def get_messages(requestBody):
    try:
        data = json.loads(requestBody)
        userID = data.get('userID')
        query = "SELECT * FROM Messages WHERE Sender_ID = %s OR Receiver_ID = %s"

        dbConnection.cursor.execute(query, [userID, userID])
        result = dbConnection.cursor.fetchall()

        data = []
        for row in result:
            message = {
                "senderID": row[1],
                "receiverID": row[2],
                "date": str(row[3]),
                "content": row[4]
            }

            data.append(message)

        return [200, json.dumps(data)]
    except ValueError as e:
        return [500, json.dumps({"failure": str(e)})]

def get_group_message(requestBody):
    try:
        userID = json.loads(requestBody).get('userID')

        user_group = check_user_group(userID)

        if not user_group:
            return [200, json.dumps({"success": "Empty Conversation"})]
        group = []
        for groupID in user_group:
            query = "SELECT Sender_ID, Date, Content FROM Group_Messages WHERE Group_ID = %s"
            dbConnection.cursor.execute(query, [groupID])
            result = dbConnection.cursor.fetchall()
            groupMessages = []
            for row in result:
                message = {
                    "senderID": row[0],
                    "date": str(row[1]),
                    "content": row[2]
                }
                groupMessages.append(message)

            group.append({"groupID": groupID, "messages": groupMessages})
        return [200, json.dumps(group)]

    except (ValueError, dbConnection.error) as e:
        return [500, json.dumps({"failure": str(e)})]

def check_user_group(userID):
    query = "SELECT Group_ID, Members FROM Conversation_Group"
    dbConnection.cursor.execute(query)
    result = dbConnection.cursor.fetchall()

    user_group = []
    for row in result:
        group_id, members_json = row[0], row[1]
        members_data = json.loads(members_json)
        members_id = [member["memberID"] for member in members_data]

        if userID in members_id:
            user_group.append(group_id)

    return user_group

def send_group_message(requestBody):
    try:
        data = json.loads(requestBody)
        senderID = data.get('userID')
        groupID = data.get('groupID')
        date = data.get('date')
        content = data.get('content')

        query = "INSERT INTO Group_Messages(Sender_ID, Group_ID, Date, Content)" \
                "VALUES(%s, %s, %s, %s)"

        dbConnection.cursor.execute(query, (senderID, groupID, date, content))
        dbConnection.connection.commit()

        return [200, json.dumps({"success": "message sent"})]

    except (ValueError, dbConnection.error) as e:
        return [500, json.dumps({"failure": str(e)})]


def send_message(requestBody):
    try:
        data = json.loads(requestBody)
        senderID = data.get('senderID')
        receiverID = data.get('receiverID')
        content = data.get('content')
        date = data.get('date')

        query = "INSERT INTO Messages(Sender_ID, Receiver_ID, Content, Date )" \
                "VALUES (%s, %s, %s, %s)"

        dbConnection.cursor.execute(query, (senderID, receiverID, content, date))
        dbConnection.connection.commit()

        return [200, json.dumps({"success": "message sent"})]

    except dbConnection.error as e:
        return [500, json.dumps({"failure": e})]
    except ValueError as e:
        return [500, json.dumps({"failure": e})]

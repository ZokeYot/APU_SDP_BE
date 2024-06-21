import base64
import collections

import dbConnection
import json


def get_user_messages(requestBody):
    try:
        data = json.loads(requestBody)
        userID = data.get('userID')
        lastDateTime = data.get('lastDateTime')

        dbConnection.cursor.execute("SELECT * FROM Messages WHERE (Sender_ID = %s OR Receiver_ID = %s) AND Date > %s "
                                    " ORDER BY Date ASC", (userID, userID, lastDateTime))

        result = dbConnection.cursor.fetchall()
        conversations = collections.defaultdict(list)

        other_user = 0
        for row in result:
            messageID = row[0]
            senderID = row[1]
            receiverID = row[2]
            date = row[3]
            content = row[4]

            if str(senderID) == userID:
                other_user = receiverID
            elif str(receiverID) == userID:
                other_user = senderID

            conversation = {
                "messageID": messageID,
                "senderID": senderID,
                "receiverID": receiverID,
                "date": str(date),
                "content": content
            }

            conversations[other_user].append(conversation)

        output = []
        for other_userID, messages in conversations.items():
            dbConnection.cursor.execute("SELECT Name, Profile_Picture FROM User WHERE User_ID = %s", [other_userID])
            result = dbConnection.cursor.fetchone()

            output.append({
                "userID": other_userID,
                "name": result[0],
                "profile_picture": base64.b64encode(result[1]).decode('utf-8'),
                "messages": messages
            })

        return [200, json.dumps(output)]
    except (ValueError, dbConnection.error) as e:
        return [500, json.dumps({"failure": str(e)})]


def get_group_message(requestBody):
    try:
        data = json.loads(requestBody)
        userID = data.get('userID')
        lastDateTime = data.get('lastDateTime')

        user_group = check_user_group(userID)

        if not user_group:
            return [200, json.dumps({"success": "Empty Conversation"})]
        group = []
        for groupID in user_group:
            query = "SELECT Message_ID, Sender_ID, u.Name, u.Profile_Picture, Date, Content " \
                    "FROM Group_Messages gm Join User u ON gm.Sender_ID = u.User_ID " \
                    "WHERE Group_ID = %s AND Date > %s ORDER BY Date ASC"
            dbConnection.cursor.execute(query, (groupID, lastDateTime))
            result = dbConnection.cursor.fetchall()
            groupMessages = []

            for row in result:
                message = {
                    "messageID": row[0],
                    "senderID": row[1],
                    "name": row[2],
                    "profile_picture": base64.b64encode(row[3]).decode('utf-8'),
                    "date": str(row[4]),
                    "content": row[5]
                }
                groupMessages.append(message)

            dbConnection.cursor.execute("SELECT Name, Admin_ID, Profile_Picture FROM Conversation_Group "
                                        "WHERE Group_ID = %s", [groupID])
            groupInfo = dbConnection.cursor.fetchone()
            name = groupInfo[0]
            adminID = groupInfo[1]
            profile_picture = base64.b64encode(groupInfo[2]).decode('utf-8')

            group.append(
                {"groupID": groupID, "name": name, "adminID": adminID, "profile_picture": profile_picture, "messages": groupMessages})
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

        if int(userID) in members_id or str(userID) in members_id:
            user_group.append(group_id)

    return user_group


def send_group_message(requestBody):
    try:
        data = json.loads(requestBody)
        senderID = data.get('senderID')
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

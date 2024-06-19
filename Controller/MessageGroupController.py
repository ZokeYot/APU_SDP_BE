import base64

import dbConnection
import json


def get_group(requestBody):
    try:
        data = json.loads(requestBody)
        groupID = data.get('groupID')

        query = "SELECT * FROM Conversation_Group WHERE Group_ID = %s"

        dbConnection.cursor.execute(query, [groupID])
        result = dbConnection.cursor.fetchone()

        if result is None:
            raise ValueError("Group Not Found")

        group = {
            "groupID": result[0],
            "adminID": result[1],
            "name": result[2],
            "profile_picture": base64.b64encode(result[3]).decode("utf-8")
        }

        return [200, json.dumps(group)]
    except (ValueError, dbConnection.error) as e:
        return [500, json.dumps({"error": str(e)})]


def create_group(requestBody):
    try:
        data = json.loads(requestBody)
        adminID = data.get('userID')
        name = data.get('name')
        profile_picture = base64.b64decode(data.get('profile_picture'))
        members = json.dumps([{"memberID": adminID}])

        query = "INSERT INTO Conversation_Group(Admin_ID, Name, Profile_Picture, Members)" \
                "VALUES(%s, %s, %s, %s)"

        dbConnection.cursor.execute(query, (adminID, name, profile_picture, members))
        dbConnection.connection.commit()

        return [200, json.dumps({"success": "Message Group Created Successfully"})]
    except (ValueError, dbConnection.error) as e:
        return [500, json.dumps({"error": str(e)})]


def update_group(requestBody):
    try:
        data = json.loads(requestBody)
        groupID = data.get("groupID")
        name = data.get('name')
        profile_picture = base64.b64decode(data.get('profile_picture'))

        query = "UPDATE Conversation_Group " \
                "SET Name = %s," \
                "Profile_Picture = %s " \
                "WHERE Group_ID = %s"

        dbConnection.cursor.execute(query, (name, profile_picture, groupID))

        return [200, json.dumps({"success": "Group Update Successfully"})]
    except (ValueError, dbConnection.error) as e:
        return [500, json.dumps({"error": str(e)})]

def delete_group(reqeustBody):
    try:
        data = json.loads(reqeustBody)
        groupID = data.get('groupID')

        query = "DELETE FROM Conversation_Group WHERE Group_ID = %s"
        dbConnection.cursor.execute(query, [groupID])

        return[200, json.dumps({"success": "Group Delete Successfully"})]

    except (ValueError , dbConnection.error) as e:
        return [500, json.dumps({"error": str(e)})]


def add_members(requestBody):
    try:
        data = json.loads(requestBody)
        groupID = data.get('groupID')
        newMembers = data.get('members')

        query = "SELECT Members FROM Conversation_Group WHERE Group_ID = %s"
        dbConnection.cursor.execute(query, [groupID])
        result = dbConnection.cursor.fetchone()

        members = json.loads(result[0])

        existingMembersID = {member["memberID"] for member in members}

        membersToAdd = [member for member in newMembers if member["memberID"] not in existingMembersID]

        if not membersToAdd:
            raise ValueError("All the provided member are already in the group")

        updatedMembers = members + membersToAdd
        updatedMemberJson = json.dumps(updatedMembers)

        update_query = "UPDATE Conversation_Group SET Members = %s WHERE Group_ID = %s"
        dbConnection.cursor.execute(update_query, (updatedMemberJson, groupID))
        dbConnection.connection.commit()

        return [200, json.dumps({"success": "Members added successfully"})]

    except (ValueError, dbConnection.error) as e:
        return [500, json.dumps({"error": str(e)})]


def delete_members(requestBody):
    try:
        data = json.loads(requestBody)
        groupID = data.get('groupID')
        membersToRemove = data.get('members')

        query = "SELECT Members FROM Conversation_Group WHERE Group_ID = %s"
        dbConnection.cursor.execute(query, [groupID])
        result = dbConnection.cursor.fetchone()

        members = json.loads(result[0])

        membersIDToRemove = {member["memberID"] for member in membersToRemove}

        membersToKeep = [member for member in members if member["memberID"] not in membersIDToRemove]

        updatedMemberJson = json.dumps(membersToKeep)
        updateQuery = "UPDATE Conversation_Group SET Members = %s WHERE Group_ID = %s"
        dbConnection.cursor.execute(updateQuery, (updatedMemberJson, groupID))
        dbConnection.connection.commit()

        return [200, json.dumps({"success": "Members removed successfully"})]
    except ValueError as e:
        return [500, json.dumps({"error": str(e)})]


def get_group_members(requestBody):
    try:
        groupID = json.loads(requestBody).get('groupID')
        query = "SELECT Members FROM Conversation_Group WHERE Group_ID = %s"
        dbConnection.cursor.execute(query, [groupID])
        row = dbConnection.cursor.fetchone()

        members_json = row[0]
        members_data = json.loads(members_json)

        group_member = [member["memberID"] for member in members_data]
        members = []

        for member in group_member:
            dbConnection.cursor.execute("SELECT * FROM User WHERE User_ID = %s", [member])
            row = dbConnection.cursor.fetchone()
            role = "lecturer" if row[7] == 1 else "student"
            user = {
                "id": row[0],
                "name": row[1],
                "gender": row[4],
                "profile_picture": base64.b64encode(row[5]).decode('utf-8'),
                "role": role,
                "title": row[9]
            }
            members.append(user)

        return [200, json.dumps(members)]
    except (ValueError, dbConnection.error) as e:
        return [500, json.dumps({"error": str(e)})]

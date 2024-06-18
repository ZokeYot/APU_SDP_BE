import base64

import dbConnection
import json

def get_materials():
    try:
        query = "SELECT * FROM Material"
        dbConnection.cursor.execute(query)

        result = dbConnection.cursor.fetchall()
        materials = []
        for row in result:
            material = {
                "materialID": row[0],
                "lecturerID": row[1],
                "name": row[2],
                "type": row[3],
                "addedDate": str(row[4]),
                "file": base64.b64encode(row[5]).decode('utf-8')
            }

            materials.append(material)

        return [200, json.dumps(materials)]
    except (ValueError, dbConnection.error) as e:
        return [500, json.dumps({"failure": str(e)})]


def get_lecturer_materials(requestBody):
    try:
        userID = json.loads(requestBody).get('lecturerID')

        dbConnection.cursor.execute("SELECT * FROM Material WHERE Lecturer_ID = %s", [userID])
        result = dbConnection.cursor.fetchall()
        materials = []
        for row in result:
            material = {
                "materialID": row[0],
                "lecturerID": row[1],
                "name": row[2],
                "type": row[3],
                "addedDate": str(row[4]),
                "file": base64.b64encode(row[5]).decode('utf-8')
            }

            materials.append(material)

        return [200, json.dumps(materials)]
    except (ValueError, dbConnection.error) as e:
        return [500, json.dumps({"failure": str(e)})]


def add_material(requestBody):
    try:
        data = json.loads(requestBody)
        lecturerID = data.get('lecturerID')
        name = data.get('name')
        type = data.get('type')
        addDate = data.get('addedDate')
        file = base64.b64decode(data.get('file'))

        query = "INSERT INTO Material (Lecturer_ID, Name, Type, AddedDate, File)" \
                "VALUES(%s, %s, %s, %s, %s)"
        dbConnection.cursor.execute(query, (lecturerID, name, type, addDate, file))
        dbConnection.connection.commit()

        return [200, json.dumps({"success": "Material uploaded successfully"})]

    except (ValueError, dbConnection.error) as e:
        return [500, json.dumps({"failure": str(e)})]


def download_material(requestBody):
    try:
        materialID = json.loads(requestBody).get('materialID')
        query = "SELECT Name, Type, File FROM Material WHERE Material_ID = %s"
        dbConnection.cursor.execute(query, [materialID])
        result = dbConnection.cursor.fetchone()

        if not result:
            raise ValueError('Material Not Found')

        fileData = {
            "name": result[0],
            "type": result[1],
            "file": base64.b64encode(result[2]).decode('utf-8')
        }

        return [200, json.dumps(fileData)]
    except (ValueError, dbConnection.error) as e:
        return [500, json.dumps({"failure": str(e)})]


def delete_material(requestBody):
    try:
        data = json.loads(requestBody)
        materialID = data.get('materialID')

        query = "DELETE FROM Material WHERE Material_ID = %s"
        dbConnection.cursor.execute(query, [materialID])
        dbConnection.connection.commit()

        return [200, json.dumps({"success": "Material delete successfully"})]
    except (ValueError, dbConnection.error) as e:
        return [500, json.dumps({"failure": str(e)})]









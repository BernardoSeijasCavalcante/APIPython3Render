from typing import Optional
from fastapi import FastAPI
import pymssql
from pydantic import BaseModel
import json

app = FastAPI()

server = 'restdb.database.windows.net'
database = 'RestaurantDatabase'
username = 'boss'
password = 'restaurantSystem123'  # Sem `{}` ao redor da senha

# Função para obter conexão com o banco de dados
def get_connection():
    return pymssql.connect(server=server, user=username, password=password, database=database)

class User(BaseModel):
    id:int
    name:str
    lastName:str
    email:str
    phoneNumber:str
    password:str
    cpf:str
    rg:str
    gender:str
    dayBirthday:str
    monthBirthday:str
    yearBirthday:str

    emergencyCode:str
    uAudioCode:str
    commandVoice:str

class Travel(BaseModel):
    id:int
    driverId:int
    passengerId:int
    destination:str
    origin:str
    date:str
    cust:str
    duration:str
    driverName:str
    passengerName:str
    status:str

@app.post("/loginUser")
async def loginUser(user:User):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM UserPassenger WHERE (email = %s AND phoneNumber = %s) AND password = %s"
        cursor.execute(query, (user.email, user.phoneNumber, user.password))

        row = cursor.fetchone()
        
        if not row:
            query = "SELECT * FROM UserDriver WHERE (email = %s AND phoneNumber = %s) AND password = %s"
            cursor.execute(query, (user.email, user.phoneNumber, user.password))
            row = cursor.fetchone()
            if not row:
                return {"name":"Login ou senha inválidos!"}



        # Obtém os nomes das colunas
        columns = [col[0] for col in cursor.description] if cursor.description else []
        data = dict(zip(columns, row))
        
        cursor.close()
        conn.close()
        return data
    
    except Exception as e:
        return {"error": str(e)}
    
@app.post("/registerDriver")
async def registerDriver(user:User):
    try:
        conn = get_connection()
        cursor = conn.cursor()    

        query = "INSERT INTO UserDriver (name, lastName, email, phoneNumber, password, cpf, rg, gender,dayBirthday,monthBirthday,yearBirthday, emergencyCode, uAudioCode, commandVoice) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        cursor.execute(query,(user.name,
        user.lastName,
        user.email,
        user.phoneNumber,
        user.password,
        user.cpf,
        user.rg,
        user.gender,
        user.dayBirthday,
        user.monthBirthday,
        user.yearBirthday,
        user.emergencyCode,
        user.uAudioCode,
        user.commandVoice))

        conn.commit()

        query = "SELECT * FROM UserDriver WHERE (email = %s AND phoneNumber = %s) AND password = %s"
        cursor.execute(query, (user.email, user.phoneNumber, user.password))
        row = cursor.fetchone()

        columns = [col[0] for col in cursor.description] if cursor.description else []
        data = dict(zip(columns, row))

        cursor.close()
        conn.close()

        return data
    except Exception as e:
        return {"error: " : str(e)}

@app.post("/registerPassenger")
async def registerPassenger(user:User):
    try:
        conn = get_connection()
        cursor = conn.cursor()    

        query = "INSERT INTO UserPassenger (name, lastName, email, phoneNumber, password, emergencyCode, uAudioCode, commandVoice) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"
        cursor.execute(query,(user.name,user.lastName,user.email,user.phoneNumber,user.password,user.emergencyCode,user.uAudioCode, user.commandVoice))

        conn.commit()

        query = "SELECT * FROM UserPassenger WHERE (email = %s AND phoneNumber = %s) AND password = %s"
        cursor.execute(query, (user.email, user.phoneNumber, user.password))
        row = cursor.fetchone()

        columns = [col[0] for col in cursor.description] if cursor.description else []
        data = dict(zip(columns, row))

        cursor.close()
        conn.close()

        return data
    except Exception as e:
        return {"error: " : str(e)}
    
@app.post("/updateUserDriver")
async def updateUserDriver(user:User):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = "UPDATE UserDriver SET name = %s, lastName = %s, email = %s, phoneNumber = %s, password = %s, cpf = %s, rg = %s, gender = %s, dayBirthday = %s, monthBirthday = %s, yearBirthday = %s WHERE id = %s"
        cursor.execute(query, (user.name, 
        user.lastName, 
        user.email, 
        user.phoneNumber, 
        user.password, 
        user.cpf, 
        user.rg, 
        user.gender, 
        user.dayBirthday, 
        user.monthBirthday, 
        user.yearBirthday, 
        user.id))

        conn.commit()

        cursor.close()
        conn.close()

        return {"message: ": "Usuário atualizado com sucesso!"}
    except Exception as e:
        return {"error: ":str(e)}

@app.post("/updateUserPassenger")
async def updateUserPassenger(user:User):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = "UPDATE UserPassenger SET name = %s, lastName = %s, email = %s, phoneNumber = %s, password = %s WHERE id = %s"
        cursor.execute(query, (user.name, 
        user.lastName, 
        user.email, 
        user.phoneNumber, 
        user.password,  
        user.id))

        conn.commit()

        cursor.close()
        conn.close()

        return {"message: ": "Usuário atualizado com sucesso!"}
    except Exception as e:
        return {"error: ":str(e)}
    
@app.post("/deleteUserDriver")
async def deleteUserDriver(user:User):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = "DELETE FROM UserDriver WHERE id = %s"
        cursor.execute(query,(user.id))

        conn.commit()

        cursor.close()
        conn.close()

        return {"message: ": "Usuário deletado com sucesso!"}
    except Exception as e:
        return {"error: ": str(e)}

@app.post("/deleteUserPassenger")
async def deleteUserPassenger(user:User):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = "DELETE FROM UserPassenger WHERE id = %s"
        cursor.execute(query,(user.id))

        conn.commit()

        cursor.close()
        conn.close()

        return {"message: ": "Usuário deletado com sucesso!"}
    except Exception as e:
        return {"error: ": str(e)}
    
@app.post("/securityVoiceConfigurationPassenger")
async def securityVoiceConfigurationPassenger(user:User):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = "UPDATE UserPassenger SET emergencyCode = %s, uAudioCode = %s, commandVoice = %s WHERE id = %s"
        cursor.execute(query, (user.emergencyCode,user.uAudioCode,user.commandVoice,user.id))

        conn.commit()

        cursor.close()
        conn.close()
        return {"message": "Configurações de SecurityVoice salvas com sucesso!"}
    except Exception as e:
        return {"error": str(e)}
    

@app.post("/securityVoiceConfigurationDriver")
async def securityVoiceConfigurationDriver(user:User):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = "UPDATE UserDriver SET emergencyCode = %s, uAudioCode = %s, commandVoice = %s WHERE id = %s"
        cursor.execute(query, (user.emergencyCode,user.uAudioCode,user.commandVoice,user.id))

        conn.commit()

        cursor.close()
        conn.close()
        return {"message": "Configurações de SecurityVoice salvas com sucesso!"}
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/refreshDriverTravel")
async def refreshDriverTravel():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = "SELECT rt.*, up.name as passengerName FROM [dbo].[RegisterTravel] as rt INNER JOIN [dbo].[UserPassenger] AS up ON rt.passengerId = up.id WHERE rt.status = 'ap/8S8fR9vOY4zWoxmU3wA==';"
        cursor.execute(query)

        rows = cursor.fetchall()

        columns = [col[0] for col in cursor.description] if cursor.description else []
        data = [dict(zip(columns, row)) for row in rows]
        
        cursor.close()
        conn.close()
        return data
    except Exception as e:
        return {"error": str(e)}

@app.post("/requestingTravel")
async def requestingTravel(travel:Travel):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = "INSERT INTO RegisterTravel (driverId, passengerId, destination, cust, date,status,duration,origin) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query , (travel.driverId,
                                   travel.passengerId,
                                   travel.destination,
                                   travel.cust,
                                   travel.date,
                                   travel.status,
                                   travel.duration,
                                   travel.origin))

        conn.commit()

        query = "SELECT * FROM RegisterTravel WHERE passengerId = %s AND status = %s"
        cursor.execute(query, (travel.passengerId, travel.status))
        row = cursor.fetchone()

        columns = [col[0] for col in cursor.description] if cursor.description else []
        data = dict(zip(columns, row))

        cursor.close()
        conn.close()
        return data
    except Exception as e:
        return {"error": str(e)}

#SELECT solution.*, UserDriver.name FROM (SELECT rt.*, up.name as passengerName FROM [dbo].[RegisterTravel] as rt INNER JOIN [dbo].[UserPassenger] AS up ON rt.passengerId = up.id WHERE rt.status = 'ap/8S8fR9vOY4zWoxmU3wA==') as solution INNER JOIN UserDriver ON solution.driverId = [dbo].[UserDriver].id;

@app.post("/cancelTravel")
async def cancelTravel(travel:Travel):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = "UPDATE RegisterTravel SET status = 'fjlPwvXJE2eSo+BZz4DzNw==' WHERE id = %s"
        cursor.execute(query , (travel.id))

        conn.commit()

        query = "SELECT * FROM RegisterTravel WHERE id = %s"
        cursor.execute(query, (travel.id))
        row = cursor.fetchone()

        columns = [col[0] for col in cursor.description] if cursor.description else []
        data = dict(zip(columns, row))

        cursor.close()
        conn.close()
        return data
    except Exception as e:
        return {"error": str(e)}
    
@app.post("/waitingDriver")
async def waitingDriver(travel:Travel):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = "SELECT rt.*, ud.name as driverName FROM [dbo].[RegisterTravel] as rt INNER JOIN [dbo].[UserDriver] AS ud ON rt.driverId = ud.id WHERE rt.id = %s;"
        cursor.execute(query, (travel.id))
        row = cursor.fetchone()

        if not row:
            query = "SELECT rt.* FROM [dbo].[RegisterTravel] as rt WHERE rt.id = %s;"
            cursor.execute(query, (travel.id))
            row = cursor.fetchone()

        columns = [col[0] for col in cursor.description] if cursor.description else []
        data = dict(zip(columns, row))

        cursor.close()
        conn.close()
        return data
    except Exception as e:
        return {"error": str(e)}
    
@app.post("/acceptingTravel")
async def acceptingTravel(travel:Travel):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = "UPDATE RegisterTravel SET status = 'IMt9PpewSWpLdtZ4x4abgw==', driverId = %s WHERE id = %s"
        cursor.execute(query , (travel.driverId,travel.id))

        conn.commit()

        query = "SELECT * FROM RegisterTravel WHERE id = %s"
        cursor.execute(query, (travel.id))
        row = cursor.fetchone()

        columns = [col[0] for col in cursor.description] if cursor.description else []
        data = dict(zip(columns, row))

        cursor.close()
        conn.close()
        return data
    except Exception as e:
        return {"error": str(e)}
    

@app.post("/travelFinish")
async def travelFinish(travel:Travel):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = "UPDATE RegisterTravel SET status = 'kdmwhSorOfGpDVUp9saoKg==' WHERE id = %s"
        cursor.execute(query , (travel.id))

        conn.commit()

        query = "SELECT * FROM RegisterTravel WHERE id = %s"
        cursor.execute(query, (travel.id))
        row = cursor.fetchone()

        columns = [col[0] for col in cursor.description] if cursor.description else []
        data = dict(zip(columns, row))

        cursor.close()
        conn.close()
        return data
    except Exception as e:
        return {"error": str(e)}
    
@app.post("/activityRefresh")
async def activityRefresh(user:User):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        if(user.cpf == "NV9uEyh7kNQ+tuVcXGjOfA=="):
            query = "SELECT * FROM [dbo].[RegisterTravel] WHERE passengerId = %s;"
        else:
            query = "SELECT * FROM [dbo].[RegisterTravel] WHERE driverId = %s;"
        cursor.execute(query , (user.id))

        conn.commit()

        query = "SELECT * FROM RegisterTravel WHERE id = %s"
        cursor.execute(query, (travel.id))
        row = cursor.fetchone()

        columns = [col[0] for col in cursor.description] if cursor.description else []
        data = dict(zip(columns, row))

        cursor.close()
        conn.close()
        return data
    except Exception as e:
        return {"error": str(e)}
    
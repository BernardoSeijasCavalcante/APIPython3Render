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
    dayBirthday:int
    monthBirthday:str
    yearBirthday:int
        

@app.post("/loginUser")
async def loginUser(user:User):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM UserPassenger WHERE (email = %s OR phoneNumber = %s) AND password = %s"
        cursor.execute(query, (user.email, user.phoneNumber, user.password))

        row = cursor.fetchone()
        
        if not row:
            query = "SELECT * FROM UserDriver WHERE (email = %s OR phoneNumber = %s) AND password = %s"
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

        query = "INSERT INTO UserDriver (name, lastName, email, phoneNumber, password, cpf, rg, gender,dayBirthday,monthBirthday,yearBirthday) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
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
        user.yearBirthday))

        conn.commit()

        query = "SELECT * FROM UserDriver WHERE (email = %s OR phoneNumber = %s) AND password = %s"
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

        query = "INSERT INTO UserPassenger (name, lastName, email, phoneNumber, password) VALUES (%s,%s,%s,%s,%s);"
        cursor.execute(query,(user.name,user.lastName,user.email,user.phoneNumber,user.password))

        conn.commit()

        query = "SELECT * FROM UserPassenger WHERE (email = %s OR phoneNumber = %s) AND password = %s"
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
        cursor.execute(query, user.name, 
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
                       user.id)

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
        cursor.execute(query, user.name, 
                       user.lastName, 
                       user.email, 
                       user.phoneNumber, 
                       user.password,  
                       user.id)

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
        cursor.execute(query,user.id)

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
        cursor.execute(query,user.id)

        conn.commit()

        cursor.close()
        conn.close()

        return {"message: ": "Usuário deletado com sucesso!"}
    except Exception as e:
        return {"error: ": str(e)}



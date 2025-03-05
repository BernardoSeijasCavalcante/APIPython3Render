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

        cursor.close()
        conn.close()

        return {"message" : "Usuário Cadastrado com sucesso!"}
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

        cursor.close()
        conn.close()
        
        return {"message" : "Usuário Cadastrado com sucesso!"}
    except Exception as e:
        return {"error: " : str(e)}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


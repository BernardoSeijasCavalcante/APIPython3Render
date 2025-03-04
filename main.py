from typing import Optional
from fastapi import FastAPI
import pymssql
import json

app = FastAPI()

server = 'restdb.database.windows.net'
database = 'RestaurantDatabase'
username = 'boss'
password = 'restaurantSystem123'  # Sem `{}` ao redor da senha

# Função para obter conexão com o banco de dados
def get_connection():
    return pymssql.connect(server=server, user=username, password=password, database=database)

class User():
    def __init__(self,name:str, lastName:str, email:str, phoneNumber:str,password:str):
        self.name = name
        self.lastName = lastName
        self.email = email
        self.phoneNumber = phoneNumber
        self.password = password
        

@app.post("/loginUser")
async def root(user:User):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT * FROM UserPassenger WHERE (email = {user.email} || phoneNumber = {user.phoneNumber}) && password = {user.password}")
        rows = cursor.fetchall()
        
        # Obtém os nomes das colunas
        columns = [col[0] for col in cursor.description]
        data = [dict(zip(columns, row)) for row in rows]
        
        conn.close()
        return {"data": data}
    
    except Exception as e:
        return {"error": str(e)}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


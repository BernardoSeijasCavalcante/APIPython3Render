from typing import Optional
from fastapi import FastAPI
import pyodbc
import json

app = FastAPI()

server = 'restdb.database.windows.net'
database = 'RestaurantDatabase'
username = 'boss'
password = 'restaurantSystem123'  # Sem `{}` ao redor da senha
driver = '{ODBC Driver 18 for SQL Server}'

# Função para obter conexão com o banco de dados
def get_connection():
    return pyodbc.connect(
        f'DRIVER={driver};SERVER=tcp:{server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
    )

@app.get("/")
async def root():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Product")
        rows = cursor.fetchall()

        products = []
        for row in rows:
            products.append({"ID": row[0], "Description": row[1]})

        conn.close()
        return json.dumps(products, indent=2)

    except Exception as e:
        return {"error": str(e)}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

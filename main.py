from typing import Optional

from fastapi import FastAPI

import pyodbc

app = FastAPI()

server = 'restdb.database.windows.net'
database = 'RestaurantDatabase'
username = 'boss'
password = '{restaurantSystem123}'
driver= '{ODBC Driver 18 for SQL Server}'






@app.get("/")
async def root():
    textJson : str
    textJson = ""
    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Product")
    row = cursor.fetchone()
    while row:
            textJson = textJson + "{ \n" + f"ID: {row[0]} , \n Description: {row[1]}" + "\n }"
            row = cursor.fetchone()
    return textJson

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
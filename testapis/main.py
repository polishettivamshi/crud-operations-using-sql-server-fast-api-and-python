from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pyodbc

conn = pyodbc.connect(driver='{ODBC Driver 17 for SQL Server}',
                      server='3.87.50.246',
                      database='CStoreiQDB_dev',
                      uid='DBUser', pwd='CStore@db123')

app = FastAPI()

class Item(BaseModel):
    id :int
    name: str
    description: str = None
    SellingPrice: float
    
@app.get('/api/get/items/')
def read_items():
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM items')
        items = []
        for row in cursor.fetchall():
            items.append({'id': row.id, 'name': row.name, 'description': row.description, 'SellingPrice': row.SellingPrice})
            return {'items': items}
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/api/post/items/')
def create_item(item: Item):
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO items (id,name, description, SellingPrice) VALUES (?, ?, ?, ?)',
                       (item.id, item.name, item.description, item.SellingPrice))
        conn.commit()
        return {'message': 'Item created successfully'}
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/api/Getitemsbyid/{item_id}')
def read_item(item_id: int):
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM items WHERE id = ?', (item_id,))
        row = cursor.fetchone()
        if row:
            return {'id': row.id, 'name': row.name, 'description': row.description, 'SellingPrice': row.SellingPrice}
        else:
            raise HTTPException(status_code=404, detail='Item not found')
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put('/api/update/items/{item_id}')
def update_item(item_id: int, item: Item):
    try:
        cursor = conn.cursor()
        cursor.execute('UPDATE items SET name = ?, description = ?, SellingPrice = ? WHERE id = ?',
                       (  item.name, item.description, item.SellingPrice, item_id))
        conn.commit()
        return {'message': 'Item updated successfully'}
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete('/api/delete/items/{item_id}')
def delete_item(item_id: int):
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM items WHERE id = ?', (item_id,))
        conn.commit()
        return {'message': 'Item deleted successfully'}
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

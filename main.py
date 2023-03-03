from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

# model input
class charModel(BaseModel):
    nama: str
    senjata: str 
    ultimate: str
    role: str

# database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="datakarakter"
)

#perintah
perintah = db.cursor()

# tampil
@app.get("/list/")
async def read_items():
    perintah.execute("SELECT * FROM karakter")
    hasil = perintah.fetchall()
    return hasil

# nambah
@app.post("/tambah/")
async def tambah(karakter: charModel):
    perintah.execute("INSERT INTO karakter (nama, senjata, role, ultimate) VALUES (%s, %s, %s, %s)",
    (karakter.nama, karakter.senjata, karakter.role, karakter.ultimate))
    db.commit()
    return{"data berhasil ditambahkan"}

#cari nama    
@app.get("/cari/{id}")
async def baca(id: int):
    perintah.execute("SELECT * FROM karakter WHERE id= %s", (id,))
    hasil = perintah.fetchone()
    return hasil

#hapus
@app.delete("/hapus/{id}")
async def hapus_char(id: int):
    perintah.execute("DELETE FROM karakter WHERE id= %s", (id,))
    db.commit()
    return{"data berhasil dihapus"}

#ganti seluruh data
@app.put("/update/{id}")
async def update_char(id: int, karakter: charModel):
    perintah.execute("UPDATE karakter SET nama= %s, senjata=%s, role= %s, ultimate= %s WHERE id= %s",
    (karakter.nama, karakter.senjata, karakter.role, karakter.ultimate, id))
    db.commit()
    return{"data berhasil di update"}

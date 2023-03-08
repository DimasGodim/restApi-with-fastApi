from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
import mysql.connector
from fastapi.responses import JSONResponse

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
#panggil jika butuh inpo ip dan user web browser 
def headers(request: Request):
    user = request.headers.get("user-agent")
    ip = request.headers.get("x-forwarded-for")
    if user is None:
        user = "data user ini tidak ditemukan"
    if ip is None:
        ip = "ip tidak ditemukan"    
    return{"user": user, "IP": ip}

#perintah
perintah = db.cursor()

# tampil
@app.get("/list/", tags=["READ"])
async def read_items(request: Request):
    atas = headers(request)
    perintah.execute("SELECT * FROM karakter")
    hasil = perintah.fetchall()
    db.close()
    return JSONResponse(content={"hasil": hasil}, headers=atas)
    

# nambah
@app.post("/tambah/", tags=["CREATE"])
async def tambah(karakter: charModel, request: Request):
    atas = headers(request)
    perintah.execute("INSERT INTO karakter (nama, senjata, role, ultimate) VALUES (%s, %s, %s, %s)",
    (karakter.nama, karakter.senjata, karakter.role, karakter.ultimate))
    db.commit()
    db.close()
    return JSONResponse(content={"status": "data berhasil ditambahkan"}, headers=atas)
    

#cari nama    
@app.get("/cari/{id}", tags=["READ"])
async def baca(id: int, request: Request):
    atas = headers(request)
    perintah.execute("SELECT * FROM karakter WHERE id= %s", (id,))
    hasil = perintah.fetchone()
    db.close()
    return JSONResponse(content={"hasil": hasil}, headers=atas)
    

#hapus
@app.delete("/hapus/{id}", tags=["DELETE"])
async def hapus_char(id: int, request:Request):
    atas = headers(request)
    perintah.execute("DELETE FROM karakter WHERE id= %s", (id,))
    db.commit()
    db.close()
    return JSONResponse(content={"status": "data berhasil dihapus"}, headers=atas)
    

#ganti seluruh data
@app.put("/update/{id}", tags=["UPDATE"])
async def update_char(id: int, karakter: charModel, request: Request):
    atas = headers(request)
    perintah.execute("UPDATE karakter SET nama= %s, senjata=%s, role= %s, ultimate= %s WHERE id= %s",
    (karakter.nama, karakter.senjata, karakter.role, karakter.ultimate, id))
    db.commit()
    db.close()
    return JSONResponse(content={"status": "data berhasil di update"}, headers=atas)
    

#ganti data dari tables yang dipilih saja
@app.patch("/patch/{id}", tags=["UPDATE"])
async def perbarui_item(id: int, char: charModel, request:Request):
    atas =headers(request)
    query = "UPDATE karakter SET "
    values = []
    if char.nama:
        query += "nama=%s, "
        values.append(char.nama)
    if char.senjata:
        query += "senjata=%s, "
        values.append(char.senjata)
    if char.ultimate:
        query += "ultimate=%s, "
        values.append(char.ultimate)
    if char.role:
        query += "role=%s, "
        values.append(char.role)
    # hapus koma terakhir pada query
    query = query[:-2]
    query += " WHERE id=%s"
    values.append(id)
    perintah.execute(query, tuple(values))
    db.commit()
    db.close()
    return JSONResponse(content={"status": "data berhasil di update"}, headers=atas)
    

#detail keselahan
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    error_msg = f"Error occurred: {str(exc)}"
    return JSONResponse(status_code=500, content={"message": error_msg})    
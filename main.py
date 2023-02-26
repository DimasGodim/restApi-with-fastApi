from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# model input
class charModel(BaseModel):
    nama: str
    senjata: str 
    ultimate: str
    role: str

# data awal
charList = {
    "godim": {"nama": "godim", "senjata": "maken", "ultimate": "honouu slash", "role": "makenshi"},
    "ivana": {"nama": "ivana", "senjata": "Suee", "ultimate": "Fiiaaa Bollll", "role": "mahotskai"},
    "cuki": {"nama": "cukiiii", "senjata": "kawai kao", "ultimate": "moe moe kyun", "role": "sapotaaa"}
}

# tampil
@app.get("/list/")
async def read_items():
    return charList

# nambah
@app.post("/tambah/")
async def tambah(karakter: charModel):
    dic = karakter.dict()
    nama = dic["nama"].lower()
    charList[nama] = dic
    return {"message": "Character added successfully"}

@app.get("/cari/{nama}")
async def baca(nama: str):
    nama = nama.lower()
    if nama in charList:
        return charList[nama]
    else:
        return {"message": "Character not found"}
        
#hapus
@app.delete("/hapus/{namaChar}")
async def hapus_char(namaChar: str):
    namaChar = namaChar.lower()
    if namaChar in charList:
        del charList[namaChar]
        return {"terhapus"}
    else:
        return{"nama tidak ada"}

#ganti seluruh data
@app.put("/update/{nama}")
async def update_char(nama:str, karakter:charModel):
    nama = nama.lower()
    if nama in charList:
        charList[nama] = karakter.dict()
        return{"update berhasil"}
    else:
        return{"nama tidak ditemukan"}    

#mengganti data yang diinginkan
@app.patch("/patch/{nama}")
async def patch_char(nama: str, karakter:charModel):
    nama= nama.lower()
    if nama in charList:
        up = karakter.dict(exclude_unset = True)
        charList[nama].update(up)
        return{"update pada" + nama + "berhasi"}
    else:
        return{"data tidak ditemukan"}


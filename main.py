from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# model input
class charModel(BaseModel):
    nama: str
    senjata: str 
    ultimate: str

# data awal
charList = {
    "makenshi": {nama: "godim", senjata: "maken", ultimate: "honouu slash"},
    "mahotskai": {nama: "ivana", senjata: "Suee", ultimate: "Fiiaaa Bollll"},
    "sapotaaa": {nama: "cukiiii", senjata: "kawai kao", ultimate: "moe moe kyun"}
}

# tampil
@app.get("/charList/")
async def read_items():
    return charList

# nambah
@app.post("/addChar")
async def add_character(character: charModel):
    char_dict = character.dict()
    charList[char_dict["nama"].lower] = char_dict
    return {"message": "Character added successfully"}

# cari
@app.get("/Seacrh/{nama}")
async def get_character(nama: str):
    if nama in charList:
        return charList[nama]
    else:
        return {"message": "Karakter tidak ditemukan"}


from pymongo import MongoClient

def conectar_mongo():
    client = MongoClient("mongodb://localhost:27017/")  # ajuste se usar outro host
    db = client["poliglota"]
    return db

def inserir_local(nome_local, cidade, latitude, longitude, descricao=""):
    db = conectar_mongo()
    colecao = db["locais"]
    documento = {
        "nome_local": nome_local,
        "cidade": cidade,
        "coordenadas": {"latitude": latitude, "longitude": longitude},
        "descricao": descricao
    }
    colecao.insert_one(documento)

def listar_locais():
    db = conectar_mongo()
    return list(db["locais"].find({}, {"_id": 0}))

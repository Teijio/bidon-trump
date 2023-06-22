from pymongo import MongoClient

COLLECTIONS = {
    "bidon_cnn": "bidon_cnn",
    "trump_cnn": "trump_cnn",
    "bidon_politico": "bidon_politico",
    "trump_politico": "trump_politico",
}


def insert_data(title, pub_date, description, collection):
    uri = "mongodb+srv://ridpfrep:Assass1n@cluster0.tkeemd2.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri)
    db = client.testdata
    call = db[collection]
    call.insert_one(
        {"title": title, "pub_date": pub_date, "description": description}
    )
    print("Данные успешно добавлены в базу данных.")

if __name__ == "__main__":
    insert_data()

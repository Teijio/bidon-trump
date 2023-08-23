from pymongo import MongoClient
import json

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


def read_data(collection):
    uri = "mongodb+srv://ridpfrep:Assass1n@cluster0.tkeemd2.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri)
    db = client.testdata
    call = db[collection]
    documents = call.find({})
    data = {}

    for document in documents:
        pub = document["pub_date"]
        print('yo')
        description = document["description"]
        pub = pub.strip()
        data[pub] = description 

    client.close()

    # Сохраняем данные в файл
    with open("data_3.json", "w") as file:
        json.dump(data, file)

read_data(COLLECTIONS["trump_politico"])

# def read_json_file(filename):
#     with open(filename, "r") as file:
#         data = json.load(file)
#     return data

# filename = "data_3.json"
# data = read_json_file(filename)
# values_list = list(data.keys())

# print(values_list)
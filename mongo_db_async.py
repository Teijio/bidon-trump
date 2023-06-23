import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

COLLECTIONS = {
    "bidon_cnn": "bidon_cnn",
    "trump_cnn": "trump_cnn",
    "bidon_politico": "bidon_politico",
    "trump_politico": "trump_politico",
}

async def insert_data_async(title, pub_date, description, collection):
    uri = "mongodb+srv://ridpfrep:Assass1n@cluster0.tkeemd2.mongodb.net/?retryWrites=true&w=majority"
    client = AsyncIOMotorClient(uri)
    db = client.testdata
    call = db[collection]
    await call.insert_one(
        {"title": title, "pub_date": pub_date, "description": description}
    )
    print("Данные успешно добавлены в базу данных.")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(insert_data_async())
    loop.close()

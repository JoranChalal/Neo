import pymongo

CLIENT_PATH = "mongodb://localhost:27017/"
DB_NAME = "LeBonCoin"
LOCATIONS_COLLECTION = "locations"


def insert_locations_href(locations_href_dict):
    # first remove old records
    # locations_collection.delete_one({"_id": "locations_href"})
    # print(len(locations_href_dict["locations_href"]))
    locations_collection = get_locations_href_collection()
    locations_collection.update_one({"_id": "locations_href"},
                                    {'$set': {"locations_href": locations_href_dict[next(iter(locations_href_dict))]}},
                                    upsert=True)
    print(len(get_all_locations_href()))


def get_all_locations_href():
    for x in get_locations_href_collection().find():
        if x["locations_href"] is None:
            return []
        else:
            return x["locations_href"]
    return []


def get_locations_href_collection():
    client = pymongo.MongoClient(CLIENT_PATH)
    db = client[DB_NAME]
    return db[LOCATIONS_COLLECTION]


def drop_database():
    client = pymongo.MongoClient(CLIENT_PATH)
    client.drop_database(DB_NAME)


def init_db():
    client = pymongo.MongoClient(CLIENT_PATH)
    db = client[DB_NAME]
    locations_collection = db[LOCATIONS_COLLECTION]
    locations_collection.insert_one({"_id": "locations_href", "locations_href": []})


print(get_all_locations_href())
#drop_database()
#init_db()

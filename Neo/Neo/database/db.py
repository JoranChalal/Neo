import pymongo
import os
from pathlib import Path

CLIENT_PATH = "mongodb://localhost:27017/"
DB_NAME = "LeBonCoin"
LOCATIONS_COLLECTION = "locations"
LOCATIONS_DATA_COLLECTION = "locations_data"


def insert_locations_href(locations_href_dict):
    locations_collection = get_locations_href_collection()
    # upsert
    locations_collection.update_one({"_id": next(iter(locations_href_dict))},
                                    {'$set': {next(iter(locations_href_dict)):
                                              locations_href_dict[next(iter(locations_href_dict))]}},
                                    upsert=True)


def insert_locations_data(locations_data_dict):
    locations_data_collection = get_locations_data_collection()
    # upsert
    locations_data_collection.update_one({"_id": locations_data_dict["full_url"]},
                                         {'$set': locations_data_dict},
                                         upsert=True)


def get_all_locations_href(postal_code):
    for x in get_locations_href_collection().find():
        if postal_code in x:
            if x[postal_code] is None:
                return []
            else:
                return x[postal_code]
    return []


def get_all_postal_code():
    postal_code_list = []
    for x in get_locations_href_collection().find():
        postal_code_list.append(x["_id"])
    return postal_code_list


def print_db():
    for x in get_locations_href_collection().find():
        print(x)
    for x in get_locations_data_collection().find():
        print(x)


def get_locations_data_collection():
    client = pymongo.MongoClient(CLIENT_PATH)
    db = client[DB_NAME]
    return db[LOCATIONS_DATA_COLLECTION]


def get_locations_href_collection():
    client = pymongo.MongoClient(CLIENT_PATH)
    db = client[DB_NAME]
    return db[LOCATIONS_COLLECTION]


def get_94_postal_codes():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    parent_dir = os.path.abspath(current_dir + "/../")
    with open(parent_dir + "/data/94") as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    return content


def drop_database():
    client = pymongo.MongoClient(CLIENT_PATH)
    client.drop_database(DB_NAME)


#drop_database()
#print_db()
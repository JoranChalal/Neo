from peewee import *
import datetime
import os


def get_postal_codes():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    parent_dir = os.path.abspath(current_dir + "/../")
    with open(parent_dir + "/data/postal_codes_93") as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    return content


class BaseModel(Model):
    class Meta:
        current_dir = os.path.abspath(os.path.dirname(__file__))
        parent_dir = os.path.abspath(current_dir + "/../")
        db = SqliteDatabase(parent_dir + '/database/database.db')
        database = db


class Location(BaseModel):
    last_scraping_date = DateTimeField(default=datetime.datetime.now)
    first_scraping_date = DateField(default=datetime.datetime.now)
    postal_code = CharField(default="00000")
    title = CharField(default="")
    price = DecimalField(default=0)
    creation_date = DateField(default=datetime.datetime.now)
    description = TextField(default="")
    charges_included = BooleanField(default=False)
    real_estate_type = CharField(default="")
    rooms = DecimalField(default=0)
    square = DecimalField(default=0)
    images = TextField(default="")
    full_url = CharField(unique=True)


class Property(BaseModel):
    last_scraping_date = DateTimeField(default=datetime.datetime.now)
    first_scraping_date = DateField(default=datetime.datetime.now)
    postal_code = CharField(default="00000")
    title = CharField(default="")
    price = DecimalField(default=0)
    creation_date = DateField(default=datetime.datetime.now)
    description = TextField(default="")
    real_estate_type = CharField(default="")
    rooms = DecimalField(default=0)
    square = DecimalField(default=0)
    images = TextField(default="")
    full_url = CharField(unique=True)


def print_count_locations():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    parent_dir = os.path.abspath(current_dir + "/../")
    db = SqliteDatabase(parent_dir + '/database/database.db')
    db.connect()
    #db.create_tables([Location])
    query_total = Location.select()
    query_count = Location.select().where(Location.title == "")
    print(str((len(query_total) - len(query_count))) + " / " + str(len(query_total)))


def print_count_properties():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    parent_dir = os.path.abspath(current_dir + "/../")
    db = SqliteDatabase(parent_dir + '/database/database.db')
    db.connect()
    #db.create_tables([Property])
    #query_total = Property.select()
    #query_count = Property.select().where(Property.title == "")
    #print(str((len(query_total) - len(query_count))) + " / " + str(len(query_total)))
    #db.drop_tables([Property])


#print_count_locations()
#print_count_properties()

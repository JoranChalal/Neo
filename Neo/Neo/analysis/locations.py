from Neo.Neo.database.db import get_locations_data_collection, get_locations_href_collection
from Neo.Neo.utils.log import log_info
from Neo.Neo.utils.math import get_interpolate_value
import statistics
import operator

MAX_Z_SCORE_AUTHORIZED = 1.75


def get_cleared_data_from_postal_code(postal_code):
    mean, st_dev = get_postal_code_z_score_data(postal_code)

    price_list = []
    for item in get_locations_href_collection().find():
        if item["_id"] == postal_code:
            for href_item in item[postal_code]:
                for x in get_locations_data_collection().find():
                    if "https://www.leboncoin.fr" + href_item["href"] == x["_id"]:
                        if is_location_flagged(x):
                            # check the z-score of the location
                            price = (float(x["price"]) / float(x["square"]))
                            z_score = round((price - mean) / st_dev, 2)
                            if z_score < MAX_Z_SCORE_AUTHORIZED:
                                price_list.append((x["_id"],
                                                   float(x["price"]),
                                                   float(x["square"])))
    return price_list


def get_mean_location_price_from_postal_code(postal_code):

    price_list = get_cleared_data_from_postal_code(postal_code)

    clean_mean_price = round(statistics.mean([i[1]/i[2] for i in price_list]), 2)
    log_info(postal_code
             + " mean price per square meter : "
             + str(clean_mean_price)
             + " EUR." + "\n"
             + "(Based on " + str(len(price_list)) + " goods)")


def print_price_from_postal_code_and_square_meters(postal_code, square_meters):
    price_list = get_cleared_data_from_postal_code(postal_code)
    data_list = [i[1]/i[2] for i in price_list]
    mean = statistics.mean(data_list)

    log_info("Price for "
             + str(square_meters)
             + " m2 in "
             + postal_code
             + " (from mean price/square): "
             + str(round(mean * square_meters, 2)) + " EUR.")


def print_interpolated_price_from_postal_code_and_square_meters(postal_code, square_meters):
    price_list = get_cleared_data_from_postal_code(postal_code)

    data_list = [(i[2], i[1]) for i in price_list]
    data_list.sort(key=operator.itemgetter(0))

    x_list = [i[0] for i in data_list]
    y_list = [i[1] for i in data_list]

    y = get_interpolate_value(x_list, y_list, float(square_meters))
    # plot(x_list, y_list)

    log_info("Interpolated value for "
             + str(square_meters)
             + " m2 in "
             + postal_code
             + " : "
             + str(round(y, 2)) + " EUR.")


def get_postal_code_z_score_data(postal_code):
    price_list = []
    for item in get_locations_href_collection().find():
        if item["_id"] == postal_code:
            for href_item in item[postal_code]:
                for x in get_locations_data_collection().find():
                    if "https://www.leboncoin.fr" + href_item["href"] == x["_id"]:
                        if is_location_flagged(x):
                            price_list.append(float(x["price"]) / float(x["square"]))

    mean = statistics.mean(price_list)
    st_dev = statistics.stdev(price_list)
    return mean, st_dev


def is_location_flagged(location):
    if location["price"] is None and location["square"] is None:
        return False
    if "colocation" in location["description"] or "coloc" in location["description"]:
        return False
    if float(location["price"]) > 1 and float(location["square"]) > 1:
        return True
    return False


print_price_from_postal_code_and_square_meters("94230", 38)
print_interpolated_price_from_postal_code_and_square_meters("94230", 38)

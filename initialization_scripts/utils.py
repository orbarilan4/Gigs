import datetime

# Create city_id from city_list
def names_to_ids(my_list):
    idx = 0
    seen_first = {}
    for row in my_list:
        if row not in seen_first:
            seen_first[row] = idx
            idx += 1
    return list([seen_first[row] for row in my_list])


# Convert to string and if doesnt get anything return str("")
def xstr(s):
    if s is None:
        return ''
    return str(s)


# This is a very sensitive function !!!
# When we got a record for purchase - It was like string that seems like a tuple
# That logic is the responsible for convert it to a real record
def get_record(record):
    # Fixing HTML value format
    record = list(record[::-1].replace(")", "", 1)[::-1].replace("(", "", 1).replace("'", "").split(","))
    for index in range(len(record)):
        if index != 0:
            record[index] = record[index][1:]
    # Build the record architecture
    record = [record[0], record[1] + "," + record[2] + "," + record[3] + "," + record[4] + "," + record[5], record[6],
              record[7],
              record[8], record[9], record[10], record[11]]
    # Convert string to datetime
    date_data = list(map(int, record[1].split("(")[1][:-1].split(",")))

    if len(date_data) == 6:
        record[1] = datetime.datetime(date_data[0], date_data[1], date_data[2], date_data[3],
                                      date_data[4], date_data[5]).strftime('%Y-%m-%d %H:%M:%S')
    else:
        record[1] = datetime.datetime(date_data[0], date_data[1], date_data[2], date_data[3],
                                      date_data[4]).strftime('%Y-%m-%d %H:%M:%S')
    return record

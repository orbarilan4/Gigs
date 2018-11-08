

# Create city_id from city_list
def names_to_ids(my_list):
    idx = 0
    seen_first = {}
    for row in my_list:
        if row not in seen_first:
            seen_first[row] = idx
            idx += 1
    return list([seen_first[row] for row in my_list])
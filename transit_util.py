import csv

def get_stop_list(filepath = 'google_transit/stops.txt'):
    with open(filepath) as f:
        reader = csv.DictReader(f)
        data = [x for x in reader]

    return [(d['stop_id'], d['stop_name']) for d in data if len(d['stop_id']) == 3]

def get_stop_dict(filepath = 'google_transit/stops.txt'):
    return dict(get_stop_list(filepath))
import pickle

def make_lot_info_map(lot_ids, num_topics, lot_to_id):
  id_to_lot = {lot_id: name for (name, lot_id) in lot_to_id.items()}
  lot_info_map = {}

  for i in range (lot_ids):
    lot_name = id_to_lot[i]
    lot_info = []

    with open("data/" + lot_name + ".csv") as f:
      f.readline()
      lot_info = f.readline().strip().split(",")

    LATITUDE_COL = 5
    LONGITUDE_COL = 6
    lot_info_map[i] = {
        "TopicID": (i % num_topics),
        "Name": lot_name,
        "Latitude": float(lot_info[LATITUDE_COL]),
        "Longitude": float(lot_info[LONGITUDE_COL]),
    }
  return lot_info_map

lots = [
  u'Beach Lot',
  u'Civic Center',
  u'Library',
  u'Lot 1',
  u'Lot 3',
  u'Lot 4',
  u'Lot 5',
  u'Lot 8',
  u'Pier Deck',
  u'Structure 1',
  u'Structure 2',
  u'Structure 3',
  u'Structure 4',
  u'Structure 5',
  u'Structure 6',
  u'Structure 7',
  u'Structure 8',
  u'Structure 9',
]

lot_to_id = {name: lot_id for (lot_id, name) in enumerate(lots)}
num_total_lots = len(lot_to_id.keys())

NUM_TOPICS = 3
lot_info_map = make_lot_info_map(num_total_lots, NUM_TOPICS, lot_to_id)

# Store mapping of lots to a lotid, and mapping of a lot
pickle.dump(lot_to_id, open("lot_to_id.p", "wb"))
pickle.dump(lot_info_map, open("lot_info_map.p", "wb"))


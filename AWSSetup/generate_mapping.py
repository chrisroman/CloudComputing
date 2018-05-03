import pickle

def mapping_lots_topics(lot_ids, num_topics):
  lots_to_topics = {}
  for i in range (lot_ids):
    lots_to_topics[i] = (i % num_topics)
  return lots_to_topics

lot_to_id = {
    u'Beach House Lot': 0,
    u'Structure 1': 1,
    u'Structure 2': 2,
    u'Structure 3': 3,
    u'Structure 4': 4,
    u'Structure 5': 5,
    u'Structure 6': 6,
    u'Structure 9': 7,
    u'Lot 8 North': 8,
    u'Lot 3 North': 9,
    u'Lot 1 North': 10,
    u'Pier Deck': 11,
    u'Lot 4 South': 12,
    u'Lot 5 South': 13,
    u'Civic Center': 14,
    u'Library': 15,
    u'Structure 7': 16,
    u'Structure 8': 17
}
num_total_lots = len(lot_to_id.keys())

NUM_TOPICS = 3
lots_to_topics = mapping_lots_topics(num_total_lots, NUM_TOPICS)

# Store mapping of lots to a lotid, and mapping of a lot
pickle.dump(lot_to_id, open("lot_to_id.p", "wb"))
pickle.dump(lots_to_topics, open("lotid_to_topics.p", "wb"))


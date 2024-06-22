import pymongo
from pymongo.write_concern import WriteConcern

class MongoHandler:
    def __init__(self, host, port, database, collection, document_class):
        self.client = pymongo.MongoClient(host=host, port=port, document_class=document_class)
        self.collection = self.client[database][collection]
    def get_indices(self):
        return self.collection.index_information()

    def create_index(self, index):
        return self.collection.create_index(index, unique=False)
    def insert_docs(self, docs):
        return self.collection.with_options(write_concern=WriteConcern(w=0)).insert_many(docs)

    def find_no_content_docs(self):
        return self.collection.find({'has_content': False})

    def replace_one_by_id(self, doc):
        return self.collection.find_one_and_replace({'_id': doc['_id']}, doc)

    def close(self):
        self.client.close()
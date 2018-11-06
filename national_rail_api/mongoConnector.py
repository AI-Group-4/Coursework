import pymongo as mongo

class mongoConnector:
    conn = None
    db = None
    def __init__(self, url, db_name):
        self.conn = mongo.MongoClient(url)
        self.db = self.conn[db_name]

    def listDbs(self):
        return self.conn.list_database_names()
    
    def listCollections(self):
        return self.db.list_collections_names()

    def store(self, collectionName, data):
        if self.conn != None and self.db != None:
            return self.db[collectionName].insert_one(data)
        return None
    
    def findAll(self, collectionName, query):
        if self.conn != None and self.db != None:
            return self.db[collectionName].find(query)
        return None

    def findOne(self, collectionName, query):
        if self.conn != None and self.db != None:
            return self.db[collectionName].find_one(query)
        return None 

def main():
    mongoConn = mongoConnector("mongodb://127.0.0.1:27017/", "train_data")
    dat = { "name": "John", "address": "Highway 59" }
    print(mongoConn.store("test", dat))
    

if __name__ == '__main__':
    main()
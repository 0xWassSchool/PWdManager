from pymongo import MongoClient


class Database:
    __client = MongoClient("mongodb://localhost:27017")
    __db = __client["oculuspwd"]
    __collection = __db["pwd"]

    def addPassword(self,
                    password: str,
                    service: str,
                    ) -> int:
        
        try:
            self.__collection.insert_one({
                "service": service,
                "pwd": password
            })
            return 0
        except:
            return 1
    
    def deletePassword(self,
                    password: str,
                    service: str,
                    ) -> int:
        try:
            self.__collection.delete_one({
                "service": service,
                "pwd": password
            })
            return 0
        except:
            return 1
    
    def getAll(self) -> list:
        documents = []

        for document in self.__collection.find({}, {'_id': 0}):
            documents.append(document)
        
        return documents
    
    def searchSingleElement(self, service: str) -> dict | int:
        try:
            documents = []

            for document in self.__collection.find({"service": service}, {"_id": 0, "pwd": 1}):
                documents.append(document)
            
            return documents
        except:
            return 1
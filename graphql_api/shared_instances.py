from utils.mongo_client import MongoClient

# Share a single instance of mongo db clients between modules.
mongo_client = MongoClient()

import os


class Config:
    MONGO_URI        = os.getenv('MONGO_URI', 'mongodb://root:example@localhost:27017')
    MONGO_DB         = os.getenv('MONGO_DB', 'watchdb')
    MONGO_COL        = os.getenv('MONGO_COL', 'users')

    INFLUX_URL       = os.getenv('INFLUX_URL', 'http://localhost:8086')
    INFLUX_TOKEN     = os.getenv('INFLUX_TOKEN')
    INFLUX_ORG       = os.getenv('INFLUX_ORG', 'myorg')
    INFLUX_BUCKET    = os.getenv('INFLUX_BUCKET', 'runs')

    QDRANT_HOST      = os.getenv('QDRANT_HOST', 'localhost')
    QDRANT_PORT      = int(os.getenv('QDRANT_PORT', 6333))
    QDRANT_COLLECTION= os.getenv('QDRANT_COLLECTION', 'ecg')
    ECG_VEC_SIZE     = int(os.getenv('ECG_VEC_SIZE', 1024))
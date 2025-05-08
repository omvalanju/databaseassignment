from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from flask import current_app


def get_qdrant_client():
    client = QdrantClient(
        url=current_app.config['QDRANT_HOST'],
        port=current_app.config['QDRANT_PORT']
    )

    try:
        client.get_collection(collection_name=current_app.config['QDRANT_COLLECTION'])
    except Exception:
        client.recreate_collection(
            collection_name=current_app.config['QDRANT_COLLECTION'],
            vectors_config=VectorParams(
                size=current_app.config['ECG_VEC_SIZE'],
                distance=Distance.COSINE
            )
        )
    return client
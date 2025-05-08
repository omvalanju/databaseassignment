import os, time, numpy as np
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance
from flask import current_app

class ECGService:
    @staticmethod
    def search_similarity(hea_file, dat_file):
        stamp = int(time.time()*1e3)
        hea_path = f"tmp_{stamp}_{hea_file.filename}"
        dat_path = f"tmp_{stamp}_{dat_file.filename}"
        hea_file.save(hea_path)
        dat_file.save(dat_path)

        try:
            raw = np.fromfile(dat_path, dtype=np.int16)
            vec_size = current_app.config['ECG_VEC_SIZE']
            if raw.size < vec_size:
                vec = np.pad(raw, (0, vec_size - raw.size), 'constant')
            else:
                vec = raw[:vec_size]
            vector = vec.tolist()

            client = QdrantClient(
                url=current_app.config['QDRANT_HOST'],
                port=current_app.config['QDRANT_PORT']
            )
            hits = client.search(
                collection_name=current_app.config['QDRANT_COLLECTION'],
                query_vector=vector,
                limit=3
            )

            return [{'id': h.id, 'score': h.score} for h in hits]

        finally:
            os.remove(hea_path)
            os.remove(dat_path)

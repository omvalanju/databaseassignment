import os
import time
import numpy as np
from flask import Blueprint, request, jsonify, current_app
from qdrant_client.http.models import PointStruct
from app.database.qdrant_client import get_qdrant_client

ecg_bp = Blueprint('ecg', __name__, url_prefix='/ecg')

@ecg_bp.route('', methods=['POST'])
def ingest_ecg():
    if 'ecg_hea' not in request.files or 'ecg_dat' not in request.files:
        return jsonify({'error': 'ecg_hea + ecg_dat files required'}), 400

    hea_f = request.files['ecg_hea']
    dat_f = request.files['ecg_dat']
    hea_fn = hea_f.filename
    dat_fn = dat_f.filename
    hea_f.save(hea_fn)
    dat_f.save(dat_fn)

    raw = np.fromfile(dat_fn, dtype=np.int16)
    vec_size = current_app.config['ECG_VEC_SIZE']
    if raw.size < vec_size:
        vec = np.pad(raw, (0, vec_size - raw.size), 'constant')
    else:
        vec = raw[:vec_size]
    vector = vec.tolist()

    client = get_qdrant_client()
    point_id = str(int(time.time() * 1e3))
    client.upsert(
        collection_name=current_app.config['QDRANT_COLLECTION'],
        points=[PointStruct(id=point_id, vector=vector, payload={'file': hea_fn})]
    )
    hits = client.search(
        collection_name=current_app.config['QDRANT_COLLECTION'],
        query_vector=vector,
        limit=3
    )

    os.remove(hea_fn)
    os.remove(dat_fn)

    return jsonify({
        'result': [{'id': hit.id, 'score': hit.score} for hit in hits]
    }), 200
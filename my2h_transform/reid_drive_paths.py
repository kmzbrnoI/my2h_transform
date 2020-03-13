from typing import Dict

from storage import Drive_Path
from reid_blocks import AREAS_REMAP


def ids_old_to_new(session) -> Dict[int, int]:
    remap = {}
    next_ids = {}
    for orig_id, new_id in AREAS_REMAP.items():
        next_ids[(orig_id, 1)] = new_id
        next_ids[(orig_id, 2)] = new_id + 500

    paths = session.query(Drive_Path).order_by(Drive_Path.start_id, Drive_Path.id).all()

    for path in paths:
        remap[path.id] = next_ids[(path.control_area, path.typ)]
        next_ids[(path.control_area, path.typ)] += 1

    return remap

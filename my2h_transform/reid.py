from storage import Control_Area, Railway, Track_Section, Signal, Junction, Disconnector
from typing import Dict


AREAS_REMAP = {
    1: 1000,     # Skuhrov
    4: 2000,     # Odbocka Skuhrov
    279: 3000,   # Hrad
    69: 4000,    # Lesna
    71: 5000,    # Skaly
    532: 6000,   # Brizky
    # 7000 Honzikov
    394: 8000,   # Podhradi
    366: 9000,   # Metro
    319: 10000,  # Ivancice
    584: 11000,  # Namest
    626: 20000,  # Depo
}


def ids_old_to_new(session) -> Dict[int, int]:
    junctions = session.query(Junction).order_by(Junction.id, Junction.control_area).all()
    print(junctions[:10])
    return {}

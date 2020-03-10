from storage import Track_Section, Signal, Junction, Disconnector, BLK, BLM, Control_Area
from typing import Dict, List, Any, Iterable


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
    # 100 000+ 'trať' + everyting about 'trať'
}


def _blocks(session, block: type) -> List[Any]:
    return session.query(block).order_by(block.control_area, block.id).all()


def _blocks_old_to_new(blocks: Iterable[Any], start: int, limit: int) -> Dict[int, int]:
    remap = {}
    count_per_area: Dict[int, int] = {}

    for block in blocks:
        remap[block.id] = AREAS_REMAP[block.control_area] + count_per_area.get(block.control_area, 0) + start
        count_per_area[block.control_area] = count_per_area.get(block.control_area, 0) + 1

    for area_id, count in count_per_area.items():
        assert count < limit, f'Count in area {area_id} overflow!'
        if count > limit - 10:
            print(f'WARN: in area {area_id} less than 10 free IDs left!')

    return remap


def ids_old_to_new(session) -> Dict[int, int]:
    remap = {}

    # junctions 0-99
    remap.update(_blocks_old_to_new(
        _blocks(session, Junction), start=0, limit=100,
    ))

    # station railway 100-149
    blks = _blocks(session, BLK)
    remap.update(_blocks_old_to_new(
        filter(lambda blk: blk.name.endswith('K'), blks),
        start=100, limit=50,
    ))

    # weird start railway (like "vlečka") 150-169
    remap.update(_blocks_old_to_new(
        filter(lambda blk: not blk.name.endswith('K'), blks),
        start=150, limit=20,
    ))

    # railways with junction in 'zhlavi' part of the station 170-219
    remap.update(_blocks_old_to_new(
        _blocks(session, BLM), start=170, limit=50,
    ))

    # IR: 300-399

    # Signals main: 400-449
    signals = _blocks(session, Signal)
    remap.update(_blocks_old_to_new(
        filter(lambda signal: signal.signal_type == 'hlavni', signals),
        start=400, limit=50,
    ))

    # Signals shunting: 450-499
    remap.update(_blocks_old_to_new(
        filter(lambda signal: signal.signal_type == 'seradovaci', signals),
        start=450, limit=50,
    ))

    # 500-599 disconnector
    remap.update(_blocks_old_to_new(
        _blocks(session, Disconnector), start=500, limit=100,
    ))

    TRAT_HARD_ORDER = [
        343, 344,  # Sk-hr
        339, 340,  # Hr-Sk
        322,  # Os-Sk
        345,  # Sk-Po
        363,  # Po-Me
        628,  # Os-Me
        290,  # Po-Hr
        342,  # Sy-Os
        341,  # Le-Sy
        578,  # Br-Le
        422,  # Iv-Os
        619,  # Na-Iv
    ]

    i = 0
    for trat in TRAT_HARD_ORDER:
        trat_id = 100000 + i * 100
        remap[trat] = trat_id

        railways = session.query(Track_Section).filter(Track_Section.railway == trat).\
            order_by(Track_Section.id).all()
        for j, railway in enumerate(railways):
            remap[railway.id] = trat_id + 10 + j

        signals = session.query(Signal).filter(Signal.signal_type == 'autoblok', Signal.trat1 == trat).\
            order_by(Signal.id).all()
        for j, signal in enumerate(signals):
            remap[signal.id] = trat_id + 50 + j

        i += 1

    # areas temporary reid to 1-100 (this will never be used in hJOP)
    areas = session.query(Control_Area).order_by(Control_Area.id).all()
    for i, area in enumerate(areas):
        remap[area.id] = i+1

    return remap

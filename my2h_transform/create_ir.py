from storage import IR, BLK, Control_Area, Track_Section, Railway

CONTROL_AREA_IDS = {
    1: 1000,    # Skuhrov
    2: 2000,    # Odbocka Skuhrov
    3: 4000,    # Lesna
    4: 5000,    # Skaly
    5: 3000,    # Hrad
    6: 10000,   # Ivancice
    7: 9000,    # Metro
    8: 8000,    # Podhradi
    9: 6000,    # Brizky
    10: 11000,  # Namest
    11: 20000,  # Depo
}


def process_blk(session, block, next_id_per_area, areas_names) -> None:
    # required: det1, det2, det3, det4, in1L, in2L, in1S, in2S
    dets = set([block.det1, block.det2, block.det3, block.det4])
    if '0:0' in dets:
        dets.remove('0:0')

    assert block.in1L == '0:0' or block.in1L in dets, f'Break not in detectors: {block}!'
    assert block.in1S == '0:0' or block.in1S in dets, f'Break not in detectors: {block}!'

    for name, inp in [('L', block.in2L), ('S', block.in2S)]:
        if inp != '0:0' and inp not in dets:
            name_ = areas_names[block.control_area] + ' ' + block.name + ' IR ' + name
            ir = IR(
                id=next_id_per_area[block.control_area],
                name=name_,
                inp=inp,
            )
            session.add(ir)
            next_id_per_area[block.control_area] += 1


def process_railway(session, block, railway_names, next_id_per_railway) -> None:
    # required: det1, det2, det3, det4, in1L, in2L, in1S, in2S
    dets = set([block.det1, block.det2, block.det3, block.det4])
    if '0:0' in dets:
        dets.remove('0:0')

    if block.in1L != '0:0' and block.in1L not in dets:
        print(f'WARN: Break not in detectors: {block}!')
    if block.in1S != '0:0' and block.in1S not in dets:
        print(f'WARN: Break not in detectors: {block}!')

    for name, inp in [('L', block.in2L), ('S', block.in2S)]:
        if inp != '0:0' and inp not in dets:
            name_ = railway_names[block.railway] + ' ' + block.name + ' IR ' + name
            ir = IR(
                id=next_id_per_railway[block.railway],
                name=name_,
                inp=inp,
            )
            session.add(ir)
            next_id_per_railway[block.railway] += 1


def create_ir(session) -> None:
    next_id_per_area = {
        id_: start_of_blocks + 300 for id_, start_of_blocks in CONTROL_AREA_IDS.items()
    }
    areas_names = {
        area.id: area.output_name() for area in session.query(Control_Area).all()
    }

    blks = session.query(BLK).order_by(BLK.id).all()
    for block in blks:
        process_blk(session, block, next_id_per_area, areas_names)

    next_id_per_railway = {
        railway.id: railway.id + 50 for railway in session.query(Railway).all()
    }
    railway_names = {
        railway.id: railway.shortname.split(' ')[0] for railway in session.query(Railway).all()
    }

    railways = session.query(Track_Section).order_by(Track_Section.id).all()
    for railway in railways:
        process_railway(session, railway, railway_names, next_id_per_railway)

    session.commit()

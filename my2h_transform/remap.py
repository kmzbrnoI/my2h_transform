from sqlalchemy.orm.session import make_transient

from utils import get_table_by_id
from storage import PNL, Control_Area, Railway, Track_Section, Signal, Junction, Disconnector, BLM, BLK, Drive_Path, BLUV, BLQ, BLEZ, BLP


def _remap(reid, id_):

    if id_ == 0 or id_ == '0':
        return str(0)
    else:
        return reid[str(id_)]


def _remap_id(reid, source_session, output_session, entity, control_area=True):

    data = []
    for item in source_session.query(entity).all():
        source_session.expunge(item)
        make_transient(item)
        item.id = _remap(reid, item.id)
        if control_area:
            item.control_area = _remap(reid, item.control_area)
        data.append(item)

    output_session.add_all(data)
    output_session.commit()


def remap_control_area(reid, source_session, output_session):

    _remap_id(reid, source_session, output_session, Control_Area, control_area=False)


def remap_railway(reid, source_session, output_session):

    _remap_id(reid, source_session, output_session, Railway, control_area=False)


def remap_track_section(reid, source_session, output_session):

    data = []
    for item in source_session.query(Track_Section).all():
        source_session.expunge(item)
        make_transient(item)
        item.id = _remap(reid, item.id)
        item.railway = _remap(reid, item.railway)
        data.append(item)

    output_session.add_all(data)
    output_session.commit()


def remap_blm(reid, source_session, output_session):

    _remap_id(reid, source_session, output_session, BLM)


def remap_blk(reid, source_session, output_session):

    _remap_id(reid, source_session, output_session, BLK)


def remap_signal(reid, source_session, output_session):

    data = []
    for item in source_session.query(Signal).all():
        source_session.expunge(item)
        make_transient(item)
        item.id = _remap(reid, item.id)
        item.control_area = _remap(reid, item.control_area) if item.control_area else None
        item.trat1 = _remap(reid, item.trat1) if item.trat1 else None
        data.append(item)

    output_session.add_all(data)
    output_session.commit()


def remap_junction(reid, source_session, output_session):

    data = []
    for item in source_session.query(Junction).all():
        source_session.expunge(item)
        make_transient(item)
        item.id = _remap(reid, item.id)
        item.control_area = _remap(reid, item.control_area)
        item.second_ref = _remap(reid, item.second_ref)
        data.append(item)

    output_session.add_all(data)
    output_session.commit()


def remap_disconnector(reid, source_session, output_session):

    _remap_id(reid, source_session, output_session, Disconnector)


def _remap_blocks_in_path(reid, session, data):

    ids = []

    for old_id in data.split(';'):
        if get_table_by_id(session, old_id) == "<class 'storage.BLUV'>":
            continue
        ids.append(_remap(reid, old_id))

    return ';'.join(ids)


def remap_drive_path(reid, source_session, output_session):

    data = []
    for item in source_session.query(Drive_Path).all():
        source_session.expunge(item)
        make_transient(item)

        item.control_area = _remap(reid, item.control_area)
        item.start_id = _remap(reid, item.start_id)
        item.end_id = _remap(reid, item.end_id)
        item.var_bod_0 = _remap(reid, item.var_bod_0)
        item.var_bod_1 = _remap(reid, item.var_bod_1)
        item.var_bod_2 = _remap(reid, item.var_bod_2)
        item.var_bod_3 = _remap(reid, item.var_bod_3)
        item.var_bod_4 = _remap(reid, item.var_bod_4)
        item.blocks_in_path = _remap_blocks_in_path(reid, source_session, item.blocks_in_path)



#            'prestavniky': ';'.join(prestavniky),
#            'odvraty_mimo_cestu': ';'.join(odvraty_mimo_cestu),
#            'odvraty_v_ceste': ';'.join(odvraty_v_ceste),
#            'volnosti': ';'.join(volnosti),
#

        data.append(item)

    output_session.add_all(data)
    output_session.commit()

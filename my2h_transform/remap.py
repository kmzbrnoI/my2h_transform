from sqlalchemy.orm.session import make_transient

from storage import PNL, Control_Area, Railway, Track_Section, Signal, Junction, Disconnector, BLM, BLK, Drive_Path, BLUV, BLQ, BLEZ, BLP


def remap_control_area(reid, source_session, output_session):

    for item in source_session.query(Control_Area).all():
        source_session.expunge(item)
        make_transient(item)
        item.id = reid[str(item.id)]
        output_session.add(item)
        output_session.commit()


def remap_railway(reid, source_session, output_session):

    for item in source_session.query(Railway).all():
        source_session.expunge(item)
        make_transient(item)
        item.id = reid[str(item.id)]
        output_session.add(item)
        output_session.commit()


def remap_track_section(reid, source_session, output_session):

    for item in source_session.query(Track_Section).all():
        source_session.expunge(item)
        make_transient(item)
        item.id = reid[str(item.id)]
        item.railway = reid[str(item.railway)]
        output_session.add(item)
        output_session.commit()


def remap_blm(reid, source_session, output_session):

    for item in source_session.query(BLM).all():
        source_session.expunge(item)
        make_transient(item)
        item.id = reid[str(item.id)]
        item.control_area = reid[str(item.control_area)]
        output_session.add(item)
        output_session.commit()


def remap_blk(reid, source_session, output_session):

    for item in source_session.query(BLK).all():
        source_session.expunge(item)
        make_transient(item)
        item.id = reid[str(item.id)]
        item.control_area = reid[str(item.control_area)]
        output_session.add(item)
        output_session.commit()


def remap_signal(reid, source_session, output_session):

    for item in source_session.query(Signal).all():
        source_session.expunge(item)
        make_transient(item)
        item.id = reid[str(item.id)]
        item.control_area = reid[str(item.control_area)] if item.control_area else None
        item.trat1 = reid[str(item.trat1)] if item.trat1 else None
        output_session.add(item)
        output_session.commit()


def remap_junction(reid, source_session, output_session):

    for item in source_session.query(Junction).all():
        source_session.expunge(item)
        make_transient(item)
        item.id = reid[str(item.id)]
        item.control_area = reid[str(item.control_area)]
        if item.second_ref != 0:
            item.second_ref = reid[str(item.second_ref)]
        output_session.add(item)
        output_session.commit()


def remap_disconnector(reid, source_session, output_session):

    for item in source_session.query(Disconnector).all():
        source_session.expunge(item)
        make_transient(item)
        item.id = reid[str(item.id)]
        item.control_area = reid[str(item.control_area)]
        output_session.add(item)
        output_session.commit()


def remap_drive_path(reid, source_session, output_session):

    for item in source_session.query(Drive_Path).all():
        source_session.expunge(item)
        make_transient(item)

        item.control_area = reid[str(item.control_area)]
        item.start_id = reid[str(item.start_id)]
        item.end_id = reid[str(item.end_id)]
        item.var_bod_0 = reid[str(item.var_bod_0)]
        item.var_bod_1 = reid[str(item.var_bod_1)]
        item.var_bod_2 = reid[str(item.var_bod_2)]
        item.var_bod_3 = reid[str(item.var_bod_3)]
        item.var_bod_4 = reid[str(item.var_bod_4)]

#        print('pred: ', item.id, item.blocks_in_path)
#        item.blocks_in_path = ';'.join([ reid[str(e)] for e in item.blocks_in_path.split(';') ])
#        print('po: ', item.id, item.blocks_in_path)

#            'prestavniky': ';'.join(prestavniky),
#            'odvraty_mimo_cestu': ';'.join(odvraty_mimo_cestu),
#            'odvraty_v_ceste': ';'.join(odvraty_v_ceste),
#            'volnosti': ';'.join(volnosti),
#

        output_session.add(item)
        output_session.commit()

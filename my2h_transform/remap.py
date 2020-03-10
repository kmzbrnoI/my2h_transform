from sqlalchemy.orm.session import make_transient

from storage import PNL, Control_Area, Railway, Track_Section, Signal, Junction, Disconnector, BLM, BLK, BLUV, BLQ, BLEZ, BLP


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

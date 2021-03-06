import logging
from utils import get_block_by_id
from storage import Control_Area, Railway, Track_Section, BLM, BLK, Signal, Junction, Disconnector, IR, Drive_Path, \
        Composite_Drive_Path
from booster_reid import BOOSTER_REMAP, BOOSTER_FROM_CONTROL_AREA, BOOSTER_FROM_BLOCK_ID
from railway import section_directions


def prepare_data_for_section(section, parent, capitalize=True, track=False):

    if capitalize:
        title = '{} {}'.format(parent.shortname.split(' ', 1)[0].capitalize(), section.name)
    else:
        title = '{} {}'.format(parent.shortname.split(' ', 1)[0], section.name)

    data = {
        'nazev': title,
        'typ': 9 if track else 1,
    }

    rcs_count = 0
    for det in (section.det1, section.det2, section.det3, section.det4):
        if det != '0:0':
            rcs_count = rcs_count + 1

    RCSb0 = int(section.det1.split(':', 1)[0])
    RCSp0 = int(section.det1.split(':', 1)[1])
    RCSb1 = int(section.det2.split(':', 1)[0])
    RCSp1 = int(section.det2.split(':', 1)[1])
    RCSb2 = int(section.det3.split(':', 1)[0])
    RCSp2 = int(section.det3.split(':', 1)[1])
    RCSb3 = int(section.det4.split(':', 1)[0])
    RCSp3 = int(section.det4.split(':', 1)[1])

    if rcs_count != 0:
        data['RCScnt'] = rcs_count

    if RCSb0 != 0:
        data['RCSb0'] = RCSb0
        data['RCSp0'] = RCSp0

    if RCSb1 != 0:
        data['RCSb1'] = RCSb1
        data['RCSp1'] = RCSp1

    if RCSb2 != 0:
        data['RCSb2'] = RCSb2
        data['RCSp2'] = RCSp2

    if RCSb3 != 0:
        data['RCSb3'] = RCSb3
        data['RCSp3'] = RCSp3

    # TODO: delka neni nactena z dat
    data['delka'] = 100

    booster = int(section.boost)
    if booster != 0:
        data['zesil'] = BOOSTER_REMAP[int(section.boost)]
    elif section.control_area in BOOSTER_FROM_CONTROL_AREA:
        data['zesil'] = BOOSTER_FROM_CONTROL_AREA[section.control_area]
    else:
        assert section.id in BOOSTER_FROM_BLOCK_ID, f'Block {section.id} missing from BOOSTER_FROM_BLOCK_ID!'
        data['zesil'] = BOOSTER_FROM_BLOCK_ID[section.id]

    if track:
        data['rychlost'] = section.velocity

    return data


def write_track_section(session):

    blocks = []
    for section, railway in session.query(
            Track_Section, Railway).filter(Track_Section.railway == Railway.id).order_by(Track_Section.id).all():
        blocks.append({
            'id': section.id,
            'data': prepare_data_for_section(section, railway, capitalize=False, track=True),
        })

    return blocks


def write_section(session):

    blocks = []

    # BLM (also with BLS dataset)
    for section, area in session.query(
            BLM, Control_Area).filter(BLM.control_area == Control_Area.id).order_by(BLM.id).all():
        blocks.append({
            'id': section.id,
            'data': prepare_data_for_section(section, area),
        })

    # BLK
    for section, area in session.query(
            BLK, Control_Area).filter(BLK.control_area == Control_Area.id).order_by(BLK.id).all():
        blocks.append({
            'id': section.id,
            'data': prepare_data_for_section(section, area),
        })

    return blocks


def signal_data(signal, name):
    data = {
        'nazev': name,
        'typ': 3,
    }

    rcs_count = 0
    for det in (signal.out1, signal.out2, signal.out3, signal.out4):
        if det != '0:0':
            rcs_count = rcs_count + 1

    RCSb0 = int(signal.out1.split(':', 1)[0])
    RCSp0 = int(signal.out1.split(':', 1)[1])
    RCSb1 = int(signal.out2.split(':', 1)[0])
    RCSp1 = int(signal.out2.split(':', 1)[1])
    RCSb2 = int(signal.out3.split(':', 1)[0])
    RCSp2 = int(signal.out3.split(':', 1)[1])
    RCSb3 = int(signal.out4.split(':', 1)[0])
    RCSp3 = int(signal.out4.split(':', 1)[1])

    if rcs_count != 0:
        data['RCScnt'] = rcs_count

    if RCSb0 != 0:
        data['RCSb0'] = RCSb0
        data['RCSp0'] = RCSp0

    if RCSb1 != 0:
        data['RCSb1'] = RCSb1
        data['RCSp1'] = RCSp1

    if RCSb2 != 0:
        data['RCSb2'] = RCSb2
        data['RCSp2'] = RCSp2

    if RCSb3 != 0:
        data['RCSb3'] = RCSb3
        data['RCSp3'] = RCSp3

    if rcs_count:
        data['OutType'] = 0

    return data


def write_signal(session):

    blocks = []

    # area signals
    for signal, area in session.query(
            Signal, Control_Area).filter(Signal.control_area == Control_Area.id).order_by(Signal.id).all():
        name = area.shortname.split(' ', 1)[0].capitalize() + ' ' + signal.name
        data = signal_data(signal, name)

        blocks.append({
            'id': signal.id,
            'data': data,
        })

    # railway signals
    for signal, railway in session.query(
        Signal, Railway).filter(
        Signal.control_area.is_(None), Signal.trat1 == Railway.id).order_by(
            Signal.id).all():
        name = railway.shortname + ' ' + signal.name
        data = signal_data(signal, name)

        blocks.append({
            'id': signal.id,
            'data': data,
        })

    return blocks


def write_junction(session):

    blocks = []
    for junction, area in session.query(
            Junction, Control_Area).filter(Junction.control_area == Control_Area.id).order_by(Junction.id).all():

        data = {
            'nazev': '{} {}'.format(area.shortname.split(' ', 1)[0].capitalize(), junction.name),
            'typ': 0,
        }

        RCSb0 = int(junction.in1.split(':', 1)[0])
        RCSp0 = int(junction.in1.split(':', 1)[1])
        RCSb1 = int(junction.in2.split(':', 1)[0])
        RCSp1 = int(junction.in2.split(':', 1)[1])
        RCSb2 = int(junction.out1.split(':', 1)[0])
        RCSp2 = int(junction.out1.split(':', 1)[1])
        RCSb3 = int(junction.out2.split(':', 1)[0])
        RCSp3 = int(junction.out2.split(':', 1)[1])

        data['RCScnt'] = 4 if junction.hw else 0

        if RCSb0 != 0:
            data['RCSb0'] = RCSb0
            data['RCSp0'] = RCSp0

        if RCSb1 != 0:
            data['RCSb1'] = RCSb1
            data['RCSp1'] = RCSp1

        if RCSb2 != 0:
            data['RCSb2'] = RCSb2
            data['RCSp2'] = RCSp2

        if RCSb3 != 0:
            data['RCSb3'] = RCSb3
            data['RCSp3'] = RCSp3

        if junction.second_ref != 0:
            data['spojka'] = junction.second_ref

        blocks.append({
            'id': junction.id,
            'data': data,
        })

    return blocks


def write_disconnector(session):

    blocks = []
    for disconnector, area in session.query(
        Disconnector, Control_Area).filter(
        Disconnector.control_area == Control_Area.id).order_by(
            Disconnector.id).all():

        data = {
            'nazev': '{} {}'.format(area.shortname.split(' ', 1)[0].capitalize(), disconnector.name),
            'typ': 8,
        }

        RCSb0 = int(disconnector.out.split(':', 1)[0])
        RCSp0 = int(disconnector.out.split(':', 1)[1])

        data['RCScnt'] = 1

        data['RCSb0'] = RCSb0
        data['RCSp0'] = RCSp0

        blocks.append({
            'id': disconnector.id,
            'data': data,
        })

    return blocks


def write_railway(session):

    blocks = []
    for railway in session.query(Railway).order_by(Railway.id).all():

        splitted_name = railway.shortname.split(' ', 1)
        if len(splitted_name) == 1:
            name = splitted_name[0]
            nazev0 = '{}>>{}'.format(name.split('-', 1)[0], name.split('-', 1)[1])
            nazev1 = '{}--{}'.format(name.split('-', 1)[0], name.split('-', 1)[1])
            nazev2 = '{}--{}'.format(name.split('-', 1)[1], name.split('-', 1)[0])
        elif len(splitted_name) == 2:
            name = splitted_name[0]
            number = splitted_name[1][0] if len(splitted_name[1]) == 2 else None
            if number:
                nazev0 = '{}>>{} {}'.format(name.split('-', 1)[0], name.split('-', 1)[1], number)
                nazev1 = '{}--{} {}'.format(name.split('-', 1)[0], name.split('-', 1)[1], number)
                nazev2 = '{}--{} {}'.format(name.split('-', 1)[1], name.split('-', 1)[0], number)
            else:
                nazev0 = '{}>>{}'.format(name.split('-', 1)[0], name.split('-', 1)[1])
                nazev1 = '{}--{}'.format(name.split('-', 1)[0], name.split('-', 1)[1])
                nazev2 = '{}--{}'.format(name.split('-', 1)[1], name.split('-', 1)[0])
        else:
            print('Error: unexpected name!')

        sections = session.query(Track_Section).filter(
            Track_Section.railway == str(
                railway.id)).order_by(
            Track_Section.id).all()

        data0 = {
            'nazev': nazev0,
            'typ': 5,
            'uvazkaA': railway.id + 1,
            'uvazkaB': railway.id + 2,
            'zabzar': 0,
            'navestidla': 1 if railway.safeguard == 'AH' else 0,
            'useky': ','.join([str(section.id) for section in sections]) + ',',
        }

        data1 = {
            'nazev': nazev1,
            'typ': 6,
            'parent': railway.id,
        }

        data2 = {
            'nazev': nazev2,
            'typ': 6,
            'parent': railway.id,
        }

        blocks.append({
            'id': railway.id,
            'data': data0,
        })

        blocks.append({
            'id': railway.id + 1,
            'data': data1,
        })

        blocks.append({
            'id': railway.id + 2,
            'data': data2,
        })

    return blocks


def write_ir(session):
    blocks = []
    for ir in session.query(IR).order_by(IR.id).all():
        blocks.append({
            'id': ir.id,
            'data': {
                'nazev': ir.name,
                'typ': 2,
                'RCScnt': 1,
                'RCSb0': ir.inp.split(':')[0],
                'RCSp0': ir.inp.split(':')[1],
            }
        })

    return blocks


def _prepare_useky(session, path, blocks):

    items = []
    for item in blocks.split(';'):
        items.append({
            'id': item,
            'block': get_block_by_id(session, item),
        })

    if (not isinstance(items[-1]['block'], Signal) and
        not isinstance(get_block_by_id(session, path.end_id), Track_Section) and
            path.typ == 1):
        logging.warning(
            'JC Blocks doesn\'t ends with Signal for JC.id {}, drive_path.end_id [{}]'.format(
                path.id, type(
                    get_block_by_id(
                        session, path.end_id))))

    sections = []
    for item in items:

        assert isinstance(
            item['block'], Track_Section) or isinstance(
            item['block'], BLM) or isinstance(
            item['block'], BLK) or isinstance(
                item['block'], Signal), f"WARN: {item['id']} has wrong type"

        if isinstance(item['block'], Track_Section) or isinstance(item['block'], BLM) or isinstance(item['block'], BLK):
            sections.append(item['id'])

    signals = []
    for i in range(len(items) - 1):  # len(items) - 1 => vynechavame posledni Signal, pokud chybi, nema to vliv
        if isinstance(items[i]['block'], Signal) and i == 0:
            logging.warning('JC Blocks starts with Signal for JC.id {}'.format(path.id))

        if isinstance(items[i]['block'], Signal) and i != 0:
            signals.append('({},{})'.format(items[i - 1]['id'], items[i]['id']))

    return sections, signals


def _prepare_vyhybky(session, id_, blocks):

    if blocks is None:
        return None

    items = []
    for item in blocks.split(';'):
        items.append({
            'id': item.split('-')[0],
            'poloha': item.split('-')[1],
            'block': get_block_by_id(session, item.split('-')[0]),
        })

    vyhybky = []
    for item in items:
        poloha = int(item['poloha']) - 1
        vyhybky.append('({},{})'.format(item['id'], poloha))

        # TODO: Je jedna iterace pres second_ref dostatecna?
        if item['block'].second_ref:
            vyhybky.append('({},{})'.format(item['block'].second_ref, poloha))

    return vyhybky


def _drive_path_name(session, start_path, end_path) -> str:
    signal1 = get_block_by_id(session, start_path.start_id)
    # railway signals
    if signal1.control_area is None:
        railway = get_block_by_id(session, signal1.trat1)
        name1 = railway.shortname + ' ' + signal1.name
    # area signals
    else:  #
        area1 = get_block_by_id(session, signal1.control_area)
        name1 = area1.shortname.split(' ', 1)[0].capitalize() + ' ' + signal1.name

    section2 = get_block_by_id(session, end_path.end_id)
    if isinstance(section2, Track_Section):
        railway2 = get_block_by_id(session, section2.railway)
        name2 = prepare_data_for_section(section2, railway2, capitalize=False, track=True)['nazev']
    elif isinstance(section2, BLK) or isinstance(section2, BLM):
        area2 = get_block_by_id(session, section2.control_area)
        name2 = prepare_data_for_section(section2, area2)['nazev']
    else:
        logging.warning('JC end_id contains unexpected block {}, JC.id {}'.format(type(section2), end_path.id))

    return '{} > {}'.format(name1, name2)


def _prepare_drive_path_name(session, path):
    return _drive_path_name(session, path, path)


def _prepare_odvraty(session, id_, blocks):

    if not blocks:
        return None

    odvraty = []
    for item in blocks.split(';'):

        d0 = item.split('-')[0]
        d1 = item.split('-')[1]
        d2 = item.split('-')[2]
        d3 = item.split('-')[3]

        assert int(d3) == 0, f"WARN: {id_} has wrong last odvrat"

        odvraty.append('({},{},{})'.format(d0, int(d1) - 1, d2))

    return odvraty


def prepare_variantni_body(path):

    variantni_body = []
    for bod in [path.var_bod_0, path.var_bod_1, path.var_bod_2, path.var_bod_3]:
        if int(bod) != 0:
            variantni_body.append(str(bod))

    return variantni_body if len(variantni_body) else None


def prepare_trat(session, path):

    last_block = get_block_by_id(session, path.end_id)
    if isinstance(last_block, Track_Section):
        return last_block.railway
    else:
        return None


def write_drive_path(session):

    sect_dirs = section_directions(session)

    blocks = []
    for drive_path in session.query(Drive_Path).order_by(Drive_Path.id).all():

        useky, prisl = _prepare_useky(session, drive_path, drive_path.blocks)
        vyhybky = _prepare_vyhybky(session, drive_path.id, drive_path.prestavniky)
        odvraty = _prepare_odvraty(session, drive_path.id, drive_path.odvraty_mimo)
        variantni_body = prepare_variantni_body(drive_path)
        trat = prepare_trat(session, drive_path)

        data = {
            'nazev': _prepare_drive_path_name(session, drive_path),
            'nav': drive_path.start_id,
            'typ': drive_path.typ,
        }

        if trat:
            assert drive_path.blocks.split(';')[-1] == useky[-1], \
                f'Last block of "trat" drive path {drive_path} is a signal!'
            data['dalsiNTyp'] = 1
        elif drive_path.typ == 1:
            assert drive_path.blocks.split(';')[-1] != useky[-1], \
                f'Last block of "non-trat" drive path {drive_path} is not a signal!'
            data['dalsiNTyp'] = 2
            data['dalsiN'] = drive_path.blocks.split(';')[-1]

        data['rychDalsiN'] = '{:d}'.format(drive_path.velocity // 10)
        data['rychNoDalsiN'] = '{:d}'.format(drive_path.velocity // 10)

        if trat:
            data['trat'] = trat
            data['tratSmer'] = sect_dirs[(trat, drive_path.control_area)]

        data['useky'] = ','.join(useky) + ','
        # data['prisl'] = ''.join(prisl)  # avoided due to new hJOP version

        if vyhybky:
            data['vyhybky'] = ''.join(vyhybky)
        if odvraty:
            data['odvraty'] = ''.join(odvraty)
        if variantni_body:
            data['vb'] = ';'.join(variantni_body) + ';'

        blocks.append({
            'id': drive_path.id,
            'data': data,
        })

    return blocks


def _prepare_composite_drive_path_name(session, cpath):
    paths = cpath.paths.split(',')
    start_path = session.query(Drive_Path).get(paths[0])
    end_path = session.query(Drive_Path).get(paths[-1])

    return _drive_path_name(session, start_path, end_path)


def write_composite_drive_path(session):

    paths = []
    for drive_path in session.query(Composite_Drive_Path).order_by(Composite_Drive_Path.id).all():
        data = {
            'nazev': _prepare_composite_drive_path_name(session, drive_path),
            'JCs': drive_path.paths.replace(',', ';') + ';',
        }
        if drive_path.vb != '':
            data['vb'] = drive_path.vb.replace(',', ';') + ';'
        paths.append({
            'id': drive_path.id,
            'data': data,
        })

    return paths

from utils import get_table_by_id
from storage import Drive_Path


def load_drive_paths(fname):

    drive_paths = []
    with open(fname, encoding='cp1250') as jc_file:
        lines = jc_file.readlines()
        for line in lines:
            drive_paths.append(line.strip('\n').split(';'))

    return drive_paths


def save_drive_paths(session, data):

    drive_paths = []
    for item in data:

        if item[0] != 'ZT':
            continue

        blocks_in_path = []
        for i in range(13, 34):
            # blokID, tabulka v niz je blok
            blocks_in_path.append('{}-{}'.format(item[i], get_table_by_id(session, item[i])))

        prestavniky = []
        for i in range(34, 76, 2):
            # blokID, poloha
            prestavniky.append('{}-{}'.format(item[i], item[i + 1]))

        odvraty_mimo_cestu = []
        for i in range(76, 160, 4):
            # blokID, poloha, vazbaID1, vazbaID2
            odvraty_mimo_cestu.append('{}-{}-{}-{}'.format(item[i], item[i + 1], item[i + 2], item[i + 3]))

        odvraty_v_ceste = []
        for i in range(160, 202, 2):
            # blokID, poloja
            odvraty_v_ceste.append('{}-{}'.format(item[i], item[i + 1]))

        volnosti = []
        for i in range(202, 217, 3):
            # blokID, vazbaID1, vazbaID2
            volnosti.append('{}-{}-{}'.format(item[i], item[i + 1], item[i + 2]))

        kwargs = {
            'id': item[1],
            'typ': item[2],  # 1=VC, 2=PC
            'control_area': item[3],
            'start_id': item[4],
            'start_id_type': get_table_by_id(session, item[4]),
            'end_id': item[5],
            'end_id_type': get_table_by_id(session, item[5]),
            'velocity': item[6],
            'nedostVzdalenost': item[7],
            'var_bod_0': item[8],
            'var_bod_0_typ': get_table_by_id(session, item[8]),
            'var_bod_1': item[9],
            'var_bod_1_typ': get_table_by_id(session, item[9]),
            'var_bod_2': item[10],
            'var_bod_2_typ': get_table_by_id(session, item[10]),
            'var_bod_3': item[11],
            'var_bod_3_typ': get_table_by_id(session, item[11]),
            'var_bod_4': item[12],
            'var_bod_4_typ': get_table_by_id(session, item[12]),
            'blocks_in_path': ';'.join(blocks_in_path),
            'prestavniky': ';'.join(prestavniky),
            'odvraty_mimo_cestu': ';'.join(odvraty_mimo_cestu),
            'odvraty_v_ceste': ';'.join(odvraty_v_ceste),
            'volnosti': ';'.join(volnosti),
        }

        drive_paths.append(Drive_Path(**kwargs))

    session.add_all(drive_paths)
    session.commit()

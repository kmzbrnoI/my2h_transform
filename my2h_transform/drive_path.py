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

        drive_path = Drive_Path(
            id=item[1],
            typ=item[2],  # 1 = VC, 2 = PC
            control_area=item[3],
            start_id=item[4],
            start_id_type=get_table_by_id(session, item[4]),
            end_id=item[5],
            end_id_type=get_table_by_id(session, item[5]),
            velocity=item[6],
            nedostVzdalenost=item[7],
            var_bod_0=item[8],
            var_bod_0_typ=get_table_by_id(session, item[8]),
            var_bod_1=item[9],
            var_bod_1_typ=get_table_by_id(session, item[9]),
            var_bod_2=item[10],
            var_bod_2_typ=get_table_by_id(session, item[10]),
            var_bod_3=item[11],
            var_bod_3_typ=get_table_by_id(session, item[11]),
            var_bod_4=item[12],
            var_bod_4_typ=get_table_by_id(session, item[12]),
        )
        drive_paths.append(drive_path)

    session.add_all(drive_paths)
    session.commit()

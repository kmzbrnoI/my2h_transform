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

        blocks = []
        for i in range(13, 34):
            if item[i] == '0':
                break
            # blokID
            blocks.append('{}'.format(item[i]))

        prestavniky = []
        for i in range(34, 76, 2):
            if item[i] == '0':
                break
            # blokID, poloha
            prestavniky.append('{}-{}'.format(item[i], item[i + 1]))

        odvraty_mimo = []
        for i in range(76, 160, 4):
            if item[i] == '0':
                break
            # blokID, poloha, vazbaID1, vazbaID2
            odvraty_mimo.append('{}-{}-{}-{}'.format(item[i], item[i + 1], item[i + 2], item[i + 3]))

        odvraty_v = []
        for i in range(160, 202, 2):
            if item[i] == '0':
                break
            # blokID, poloha
            odvraty_v.append('{}-{}'.format(item[i], item[i + 1]))

        volnosti = []
        for i in range(202, 217, 3):
            if item[i] == '0':
                break
            # blokID, vazbaID1, vazbaID2
            volnosti.append('{}-{}-{}'.format(item[i], item[i + 1], item[i + 2]))

        kwargs = {
            'id': item[1],
            'typ': item[2],  # 1=VC, 2=PC
            'control_area': item[3],
            'start_id': item[4],
            'end_id': item[5],
            'velocity': 40 if int(item[6]) == 0 else item[6],
            'nedostVzdalenost': item[7],
            'var_bod_0': item[8],
            'var_bod_1': item[9],
            'var_bod_2': item[10],
            'var_bod_3': item[11],
            'var_bod_4': item[12],
            'blocks': ';'.join(blocks),
            'prestavniky': ';'.join(prestavniky),
            'odvraty_mimo': ';'.join(odvraty_mimo),
            'odvraty_v': ';'.join(odvraty_v),
            'volnosti': ';'.join(volnosti),
        }

        drive_paths.append(Drive_Path(**kwargs))

    session.add_all(drive_paths)
    session.commit()

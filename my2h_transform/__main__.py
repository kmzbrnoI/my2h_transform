"""My2h JOP Transform Utility
Usage:
  my2h_transform.py blocks <myjop_blk_file>
  my2h_transform.py (-h | --help)
  my2h_transform.py --version

Options:
  -h --help          Show this screen.
  --version          Show version.
"""

import os
import json
from docopt import docopt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from storage import BASE, PNL, BLOR, BLOPM, BLOPD, BLT, BLW, BLH, BLB, BLC, BLE, BLV, BLM, BLK, BLUV, BLQ


DB_FILE = './blk.db'


def main():
    '''Entry point'''
    args = docopt(__doc__, version='0.0.1')  # pylint: disable=unused-variable

    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print('File [{}] removed.'.format(DB_FILE))

    SQLEngine = create_engine('sqlite:///blk.db', echo=False)
    BASE.metadata.create_all(SQLEngine)
    SQLSession = sessionmaker(bind=SQLEngine)
    session = SQLSession()

    if args['blocks']:

        block_types = ['PNL', 'OR', 'OPM', 'OPD', 'L', 'W', 'T', 'H', 'B', 'C', 'A',
                       'D', 'E', 'V', 'M', 'S', 'K', 'UV', 'Q', 'PST', 'EZ', 'N', 'R', 'P']

        datasets = []
        with open(args['<myjop_blk_file>'], encoding='cp1250') as blk_file:
            lines = blk_file.readlines()
            dataset = []
            type_number = 0
            for line in lines:
                if line == '\n':
                    datasets.append({'type': block_types[type_number], 'data': dataset})
                    dataset = []
                    type_number = type_number + 1
                else:
                    dataset.append(line.strip('\n'))

        print('--- Datasets ---')
        for dataset in datasets:
            print(dataset['type'])

        print('--- PNL dataset ---')
        print('Názvy panelů')
        pnls = []
        for dataset in datasets[block_types.index('PNL')]['data'][2:]:
            data = dataset.split(';')
            pnl = PNL(
                id=data[1],
                name=data[2])
            pnls.append(pnl)

        session.add_all(pnls)
        session.commit()

        print('--- OR dataset ---')
        print('Oblasti řízení')
        blors = []
        for dataset in datasets[block_types.index('OR')]['data'][1:]:
            data = dataset.split(';')
            blor = BLOR(
                id=data[3],
                shortname=data[4],
                name=data[4])
            blors.append(blor)

        session.add_all(blors)
        session.commit()

        print('--- OPM dataset ---')
        blopms = []
        for dataset in datasets[block_types.index('OPM')]['data'][1:]:
            data = dataset.split(';')
            blopm = BLOPM(id=data[3], name=data[5], blor=data[4], pnl=data[6], direction_L=data[8])
            blopms.append(blopm)

        session.add_all(blopms)
        session.commit()

        print('--- OPD dataset ---')
        blopds = []
        for dataset in datasets[block_types.index('OPD')]['data'][1:]:
            data = dataset.split(';')
            blopd = BLOPD(id=data[3], name=data[5], blor=data[4], pnl=data[6])
            blopds.append(blopd)

        session.add_all(blopds)
        session.commit()

        print('--- TR L dataset ---')
        print('Nepřináší žádnou novou informaci')

        print('--- BL W dataset ---')
        print('Koleje propojeny do tratí')
        blws = []
        for dataset in datasets[block_types.index('W')]['data'][1:]:
            data = dataset.split(';')
            blw = BLW(
                id=data[3],
                label=data[4],
                name=data[6],
                gate_type=data[7],
                conn_1=data[10],
                conn_2=data[11],
                conn_3=data[12],
                conn_4=data[13],
                conn_5=data[14],
                conn_6=data[15] if data[3] == str(341) else None)
            blws.append(blw)

        session.add_all(blws)
        session.commit()

        print('--- BL T dataset ---')
        print('Zřejmě se jedná o koleje')
        blts = []
        for dataset in datasets[block_types.index('T')]['data'][1:]:
            data = dataset.split(';')
            blt = BLT(
                id=data[3],
                group=data[4],
                label=data[5],
                label_text_part=data[6],
                gate_type=data[7],
                velocity=data[12],
                det1=data[15],
                det2=data[16],
                det3=data[17],
                det4=data[18],
                boost=data[19],
                power_source=data[20],
                one_L=data[21],
                two_L=data[22],
                one_S=data[23],
                two_S=data[24],
                nvLtype=data[25],
                hw_L=data[26],
                out1_L=data[27],
                out2_L=data[28],
                out3_L=data[29],
                out4_L=data[30],
                out5_L=data[31],
                nvStype=data[32],
                hw_S=data[33],
                out1_S=data[34],
                out2_S=data[35],
                out3_S=data[36],
                out4_S=data[37],
                out5_S=data[38])
            blts.append(blt)

        session.add_all(blts)
        session.commit()

        print('--- H dataset ---')
        blhs = []
        for dataset in datasets[block_types.index('H')]['data'][1:]:
            data = dataset.split(';')
            blh = BLH(
                id=data[3],
                blor=data[4].split(':', 1)[0],
                name=data[5],
                posun=data[6],
                direction=data[8],
                skupinNv=data[9],
                pst1=data[11],
                pst2=data[12],
                typ=data[13],
                hw=data[14],
                out1=data[15],
                out2=data[16],
                out3=data[17],
                out4=data[18],
                out5=data[19],
                usek1=data[21],
                usek2=data[22],
                blokUV=data[23])
            blhs.append(blh)

        session.add_all(blhs)
        session.commit()

        print('--- B dataset ---')
        blbs = []
        for dataset in datasets[block_types.index('B')]['data'][1:]:
            data = dataset.split(';')
            blb = BLB(
                id=data[3],
                blor=data[4].split(':', 1)[0],
                name=data[5],
                direction=data[8],
                skupinNv=data[9],
                pst1=data[11],
                pst2=data[12],
                typ=data[13],
                hw=data[14],
                out1=data[15],
                out2=data[16],
                out3=data[17],
                out4=data[18],
                out5=data[19],
                usek1=data[21],
                usek2=data[22])
            blbs.append(blb)

        session.add_all(blbs)
        session.commit()

        print('--- C dataset ---')
        blcs = []
        for dataset in datasets[block_types.index('C')]['data'][1:]:
            data = dataset.split(';')
            blc = BLC(
                id=data[3],
                blor=data[4].split(':', 1)[0],
                name=data[5],
                typ=data[13],
                hw=data[14],
                out1=data[15],
                out2=data[16],
                out3=data[17],
                out4=data[18],
                out5=data[19],
                skupina1=data[24] if data[3] == str(329) else None,
                skupina2=data[25] if data[3] == str(329) else None,
                skupina3=data[26] if data[3] == str(329) else None)
            blcs.append(blc)

        session.add_all(blcs)
        session.commit()

        # TODO: Blok A došetřit, zatím nedává smysl
        # Blok D je prázdný

        print('--- E dataset ---')
        bles = []
        for dataset in datasets[block_types.index('E')]['data'][1:]:
            data = dataset.split(';')
            ble = BLE(
                id=data[3],
                name=data[5],
                trat1=data[6],
                trat2=data[7],
                direction=data[8],
                typ=data[13],
                hw=data[14],
                out1=data[15],
                out2=data[16],
                out3=data[17],
                out4=data[18],
                out5=data[19])
            bles.append(ble)

        session.add_all(bles)
        session.commit()

        print('--- V dataset ---')
        blvs = []
        for dataset in datasets[block_types.index('V')]['data'][1:]:
            data = dataset.split(';')
            blv = BLV(
                id=data[3],
                blor=data[4].split(':', 1)[0],
                name=data[5],
                blok_s1=data[6],
                blok_s2=data[7],
                ez=data[10],
                pst1=data[11],
                pst2=data[12],
                hw=data[14],
                out1=data[15],
                out2=data[16],
                in1=data[17],
                in2=data[18],
                outB1=data[19],
                outB2=data[20],
                inB1=data[21],
                inB2=data[22],
                zdroj=data[23])
            blvs.append(blv)

        session.add_all(blvs)
        session.commit()

        print('--- M dataset ---')
        blms = []
        for dataset in datasets[block_types.index('M')]['data'][1:]:
            data = dataset.split(';')
            blm = BLM(
                id=data[3],
                blor=data[4].split(':', 1)[0],
                name=data[5],
                pst1=data[10],
                pst2=data[11],
                velocity=data[12],
                det1=data[15],
                det2=data[16],
                det3=data[17],
                det4=data[18],
                boost=data[19],
                power_source=data[20])
            blms.append(blm)

        session.add_all(blms)
        session.commit()

        print('--- S dataset ---')
        # nacteno do tabulky pro M dataset
        blms = []
        for dataset in datasets[block_types.index('S')]['data'][1:]:
            data = dataset.split(';')
            blm = BLM(
                id=data[3],
                blor=data[4].split(':', 1)[0],
                name=data[5],
                pst1=data[10],
                pst2=data[11],
                velocity=data[12],
                det1=data[15],
                det2=data[16],
                det3=data[17],
                det4=data[18],
                boost=data[19],
                power_source=data[20])
            blms.append(blm)

        session.add_all(blms)
        session.commit()

        print('--- K dataset ---')
        blks = []
        for dataset in datasets[block_types.index('K')]['data'][1:]:
            data = dataset.split(';')
            blk = BLK(
                id=data[3],
                blor=data[4].split(':', 1)[0],
                name=data[5],
                pst1=data[10],
                pst2=data[11],
                velocity=data[12],
                det1=data[15],
                det2=data[16],
                det3=data[17],
                det4=data[18],
                boost=data[19],
                power_source=data[20],
                in1L=data[21],
                in2L=data[22],
                in1S=data[23],
                in2S=data[24])
            blms.append(blk)

        session.add_all(blks)
        session.commit()

        print('--- UV dataset ---')
        bluvs = []
        for dataset in datasets[block_types.index('UV')]['data'][1:]:
            data = dataset.split(';')
            bluv = BLUV(
                id=data[3],
                blor=data[4].split(':', 1)[0],
                name=data[5],
                direction=data[6],
                souhlas=data[7],
                nvID=data[8],
                pocetID=data[9])
            blms.append(bluv)

        session.add_all(bluvs)
        session.commit()

        print('--- Q dataset ---')
        blqs = []
        for dataset in datasets[block_types.index('Q')]['data'][1:]:
            data = dataset.split(';')
            blq = BLQ(
                id=data[3],
                blor=data[4].split(':', 1)[0],
                name=data[5],
                bluv=data[6],
                pocetID=data[7])
            blqs.append(blq)

        session.add_all(blqs)
        session.commit()


if __name__ == '__main__':
    main()

"""
Save datasets into database
"""

from utils import DATASET_TYPES
from storage import PNL, Control_Area, Railway, Track_Section, Signal, Junction, Disconnector, BLM, BLK, BLUV, BLQ, BLEZ, BLP


def save_control_area(session, datasets):

    print('Control Area')
    control_areas = []
    for dataset in datasets[DATASET_TYPES.index('OR')]['data'][1:]:
        data = dataset.split(';')
        control_area = Control_Area(
            id=data[3],
            shortname=data[4],
            name=data[5])
        control_areas.append(control_area)

    session.add_all(control_areas)
    session.commit()


def save_railway(session, datasets):

    print('Railway')
    railways = []
    for dataset in datasets[DATASET_TYPES.index('W')]['data'][1:]:
        data = dataset.split(';')
        railway = Railway(
            id=data[3],
            shortname=data[4],
            name=data[6],
            safeguard=data[7])
        railways.append(railway)

    session.add_all(railways)
    session.commit()


def save_track_section(session, datasets):

    print('Track Section')
    track_sections = []
    for dataset in datasets[DATASET_TYPES.index('T')]['data'][1:]:
        data = dataset.split(';')
        track_section = Track_Section(
            id=data[3],
            railway=data[4].split(':', 1)[0],
            name=data[6],
            safeguard=data[7],
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
        track_sections.append(track_section)

    session.add_all(track_sections)
    session.commit()


def save_signal(session, datasets):

    signals = []
    print('Signal from H')
    for dataset in datasets[DATASET_TYPES.index('H')]['data'][1:]:
        data = dataset.split(';')
        signal = Signal(
            id=data[3],
            signal_type='hlavni',
            control_area=data[4].split(':', 1)[0],
            name=data[5],
            shunt=data[6],
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
            blokUV=data[23],
            skupina1=None,
            skupina2=None,
            skupina3=None,
            trat1=None,
            trat2=None)
        signals.append(signal)

    print('Signal from B')
    for dataset in datasets[DATASET_TYPES.index('B')]['data'][1:]:
        data = dataset.split(';')
        signal = Signal(
            id=data[3],
            signal_type='seradovaci',
            control_area=data[4].split(':', 1)[0],
            name=data[5],
            shunt=None,
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
            blokUV=None,
            skupina1=None,
            skupina2=None,
            skupina3=None,
            trat1=None,
            trat2=None)
        signals.append(signal)

#    print('Signal from C')
#    for dataset in datasets[DATASET_TYPES.index('C')]['data'][1:]:
#        data = dataset.split(';')
#        signal = Signal(
#            id=data[3],
#            signal_type='skupinove',
#            control_area=data[4].split(':', 1)[0],
#            name=data[5],
#            shunt=None,
#            direction=None,
#            skupinNv=None,
#            pst1=None,
#            pst2=None,
#            typ=data[13],
#            hw=data[14],
#            out1=data[15],
#            out2=data[16],
#            out3=data[17],
#            out4=data[18],
#            out5=data[19],
#            usek1=None,
#            usek2=None,
#            blokUV=None,
#            skupina1=data[24] if data[3] == str(329) else None,
#            skupina2=data[25] if data[3] == str(329) else None,
#            skupina3=data[26] if data[3] == str(329) else None,
#            trat1=None,
#            trat2=None)
#        signals.append(signal)
#
    print('Signal from E')
    for dataset in datasets[DATASET_TYPES.index('E')]['data'][1:]:
        data = dataset.split(';')
        signal = Signal(
            id=data[3],
            signal_type='autoblok',
            control_area=None,
            name=data[5],
            shunt=None,
            direction=data[8],
            skupinNv=None,
            pst1=None,
            pst2=None,
            typ=data[13],
            hw=data[14],
            out1=data[15],
            out2=data[16],
            out3=data[17],
            out4=data[18],
            out5=data[19],
            usek1=None,
            usek2=None,
            blokUV=None,
            skupina1=None,
            skupina2=None,
            skupina3=None,
            trat1=data[6].split(':', 1)[0],
            trat2=data[7])
        signals.append(signal)

    session.add_all(signals)
    session.commit()


def save_junction(session, datasets):

    print('Junction')
    junctions = []
    for dataset in datasets[DATASET_TYPES.index('V')]['data'][1:]:
        data = dataset.split(';')
        junction = Junction(
            id=data[3],
            control_area=data[4].split(':', 1)[0],
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
        junctions.append(junction)

    session.add_all(junctions)
    session.commit()


def save_disconnector(session, datasets):

    print('Disconnector')
    disconnectors = []
    for dataset in datasets[DATASET_TYPES.index('R')]['data'][1:]:
        data = dataset.split(';')
        disconnector = Disconnector(
            id=data[3],
            control_area=data[4].split(':', 1)[0],
            name=data[5],
            blk=data[6],
            out=data[15])
        disconnectors.append(disconnector)

    session.add_all(disconnectors)
    session.commit()


def save_datasets(session, datasets):

    print('--- PNL dataset ---')
    pnls = []
    for dataset in datasets[DATASET_TYPES.index('PNL')]['data'][2:]:
        data = dataset.split(';')
        pnl = PNL(
            id=data[1],
            name=data[2])
        pnls.append(pnl)

    session.add_all(pnls)
    session.commit()

    save_control_area(session, datasets)
    save_railway(session, datasets)
    save_track_section(session, datasets)
    save_signal(session, datasets)
    save_junction(session, datasets)
    save_disconnector(session, datasets)

    # TODO: Blok A došetřit, zatím nedává smysl
    # Blok D je prázdný

    print('--- M dataset ---')
    blms = []
    for dataset in datasets[DATASET_TYPES.index('M')]['data'][1:]:
        data = dataset.split(';')
        blm = BLM(
            id=data[3],
            control_area=data[4].split(':', 1)[0],
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
    for dataset in datasets[DATASET_TYPES.index('S')]['data'][1:]:
        data = dataset.split(';')
        blm = BLM(
            id=data[3],
            control_area=data[4].split(':', 1)[0],
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
    for dataset in datasets[DATASET_TYPES.index('K')]['data'][1:]:
        data = dataset.split(';')
        blk = BLK(
            id=data[3],
            control_area=data[4].split(':', 1)[0],
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
        blks.append(blk)

    session.add_all(blks)
    session.commit()

    print('--- UV dataset ---')
    bluvs = []
    for dataset in datasets[DATASET_TYPES.index('UV')]['data'][1:]:
        data = dataset.split(';')
        bluv = BLUV(
            id=data[3],
            control_area=data[4].split(':', 1)[0],
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
    for dataset in datasets[DATASET_TYPES.index('Q')]['data'][1:]:
        data = dataset.split(';')
        blq = BLQ(
            id=data[3],
            control_area=data[4].split(':', 1)[0],
            name=data[5],
            bluv=data[6],
            pocetID=data[7])
        blqs.append(blq)

    session.add_all(blqs)
    session.commit()

    # PST je prazdne
    # N je prazdne

    print('--- EZ dataset ---')
    blezs = []
    for dataset in datasets[DATASET_TYPES.index('EZ')]['data'][1:]:
        data = dataset.split(';')
        blez = BLEZ(
            id=data[3],
            control_area=data[4].split(':', 1)[0],
            name=data[5],
            blv=data[24])
        blezs.append(blez)

    session.add_all(blezs)
    session.commit()

    print('--- P dataset ---')
    blps = []
    for dataset in datasets[DATASET_TYPES.index('P')]['data'][1:]:
        data = dataset.split(';')
        blp = BLP(
            id=data[3],
            control_area=data[4].split(':', 1)[0],
            name=data[5],
            typ=data[14],
            inUzav=data[15],
            inOtev=data[16],
            inAnulace=data[17],
            inUzZav=data[18],
            outUzav=data[19],
            outNouzOtev=data[20],
            outBlokPoz=data[21])
        blps.append(blp)

    session.add_all(blps)
    session.commit()

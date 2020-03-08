"""
Database handler
"""

from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String
#from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


BASE = declarative_base()


class PNL(BASE):

    __tablename__ = 'pnls'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Control_Area(BASE):

    __tablename__ = 'control_areas'

    id = Column(Integer, primary_key=True)
    shortname = Column(String)
    name = Column(String)


class BLT(BASE):

    __tablename__ = 'blts'

    id = Column(Integer, primary_key=True)
    group = Column(String)
    label = Column(String)
    label_text_part = Column(String)
    gate_type = Column(String)
    velocity = Column(Integer)
    det1 = Column(String)
    det2 = Column(String)
    det3 = Column(String)
    det4 = Column(String)
    boost = Column(Integer)
    power_source = Column(String)
    one_L = Column(String)
    two_L = Column(String)
    one_S = Column(String)
    two_S = Column(String)
    nvLtype = Column(String)
    hw_L = Column(String)
    out1_L = Column(String)
    out2_L = Column(String)
    out3_L = Column(String)
    out4_L = Column(String)
    out5_L = Column(String)
    nvStype = Column(String)
    hw_S = Column(String)
    out1_S = Column(String)
    out2_S = Column(String)
    out3_S = Column(String)
    out4_S = Column(String)
    out5_S = Column(String)


class BLW(BASE):

    __tablename__ = 'blws'

    id = Column(Integer, primary_key=True)
    label = Column(String)
    name = Column(String)
    gate_type = Column(String)
    conn_1 = Column(String)
    conn_2 = Column(String)
    conn_3 = Column(String)
    conn_4 = Column(String)
    conn_5 = Column(String)
    conn_6 = Column(String)


class BLH(BASE):

    __tablename__ = 'blhs'

    id = Column(Integer, primary_key=True)
    control_area = Column(Integer, ForeignKey('control_areas.id'))
    name = Column(String)
    posun = Column(Integer)
    direction = Column(Integer)
    skupinNv = Column(String)
    pst1 = Column(String)
    pst2 = Column(String)
    typ = Column(Integer)
    hw = Column(Integer)
    out1 = Column(String)
    out2 = Column(String)
    out3 = Column(String)
    out4 = Column(String)
    out5 = Column(String)
    usek1 = Column(String)
    usek2 = Column(String)
    blokUV = Column(String)


class BLB(BASE):

    __tablename__ = 'blbs'

    id = Column(Integer, primary_key=True)
    control_area = Column(Integer, ForeignKey('control_areas.id'))
    name = Column(String)
    direction = Column(Integer)
    skupinNv = Column(String)
    pst1 = Column(String)
    pst2 = Column(String)
    typ = Column(Integer)
    hw = Column(Integer)
    out1 = Column(String)
    out2 = Column(String)
    out3 = Column(String)
    out4 = Column(String)
    out5 = Column(String)
    usek1 = Column(String)
    usek2 = Column(String)


class BLC(BASE):

    __tablename__ = 'blcs'

    id = Column(Integer, primary_key=True)
    control_area = Column(Integer, ForeignKey('control_areas.id'))
    name = Column(String)
    typ = Column(Integer)
    hw = Column(Integer)
    out1 = Column(String)
    out2 = Column(String)
    out3 = Column(String)
    out4 = Column(String)
    out5 = Column(String)
    skupina1 = Column(String)
    skupina2 = Column(String)
    skupina3 = Column(String)


class BLE(BASE):

    __tablename__ = 'bles'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    trat1 = Column(String)
    trat2 = Column(String)
    direction = Column(Integer)
    typ = Column(Integer)
    hw = Column(Integer)
    out1 = Column(String)
    out2 = Column(String)
    out3 = Column(String)
    out4 = Column(String)
    out5 = Column(String)


class BLV(BASE):

    __tablename__ = 'blvs'

    id = Column(Integer, primary_key=True)
    control_area = Column(Integer, ForeignKey('control_areas.id'))
    name = Column(String)
    blok_s1 = Column(String)
    blok_s2 = Column(String)
    ez = Column(Integer)
    pst1 = Column(String)
    pst2 = Column(String)
    hw = Column(Integer)
    out1 = Column(String)
    out2 = Column(String)
    in1 = Column(String)
    in2 = Column(String)
    outB1 = Column(String)
    outB2 = Column(String)
    inB1 = Column(String)
    inB2 = Column(String)
    zdroj = Column(String)


class BLM(BASE):

    __tablename__ = 'blms'

    id = Column(Integer, primary_key=True)
    control_area = Column(Integer, ForeignKey('control_areas.id'))
    name = Column(String)
    pst1 = Column(String)
    pst2 = Column(String)
    velocity = Column(Integer)
    det1 = Column(String)
    det2 = Column(String)
    det3 = Column(String)
    det4 = Column(String)
    boost = Column(String)
    power_source = Column(String)


class BLK(BASE):

    __tablename__ = 'blks'

    id = Column(Integer, primary_key=True)
    control_area = Column(Integer, ForeignKey('control_areas.id'))
    name = Column(String)
    pst1 = Column(String)
    pst2 = Column(String)
    velocity = Column(Integer)
    det1 = Column(String)
    det2 = Column(String)
    det3 = Column(String)
    det4 = Column(String)
    boost = Column(String)
    power_source = Column(String)
    in1L = Column(String)
    in2L = Column(String)
    in1S = Column(String)
    in2S = Column(String)


class BLUV(BASE):

    __tablename__ = 'bluvs'

    id = Column(Integer, primary_key=True)
    control_area = Column(Integer, ForeignKey('control_areas.id'))
    name = Column(String)
    direction = Column(Integer)
    souhlas = Column(Integer)
    nvID = Column(String)
    pocetID = Column(Integer)


class BLQ(BASE):

    __tablename__ = 'blqs'

    id = Column(Integer, primary_key=True)
    control_area = Column(Integer, ForeignKey('control_areas.id'))
    name = Column(String)
    bluv = Column(String)
    pocetID = Column(Integer)


class BLEZ(BASE):

    __tablename__ = 'blezs'

    id = Column(Integer, primary_key=True)
    control_area = Column(Integer, ForeignKey('control_areas.id'))
    name = Column(String)
    blv = Column(String)


class BLR(BASE):

    __tablename__ = 'blrs'

    id = Column(Integer, primary_key=True)
    control_area = Column(Integer, ForeignKey('control_areas.id'))
    name = Column(String)
    blk = Column(String)
    out = Column(String)


class BLP(BASE):

    __tablename__ = 'blps'

    id = Column(Integer, primary_key=True)
    control_area = Column(Integer, ForeignKey('control_areas.id'))
    name = Column(String)
    typ = Column(String)
    inUzav = Column(String)
    inOtev = Column(String)
    inAnulace = Column(String)
    inUzZav = Column(String)
    outUzav = Column(String)
    outNouzOtev = Column(String)
    outBlokPoz = Column(String)

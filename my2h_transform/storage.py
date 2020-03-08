"""
Database handler
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

BASE = declarative_base()


class PNL(BASE):

    __tablename__ = 'pnls'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class BLOR(BASE):

    __tablename__ = 'blors'

    id = Column(Integer, primary_key=True)
    shortname = Column(String)
    name = Column(String)


class BLOPM(BASE):

    __tablename__ = 'blopms'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    blor = Column(Integer)
    pnl = Column(String)
    direction_L = Column(Integer)


class BLOPD(BASE):

    __tablename__ = 'blopds'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    blor = Column(Integer)
    pnl = Column(String)


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
    blor = Column(Integer)
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
    blor = Column(Integer)
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
    blor = Column(Integer)
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
    blor = Column(Integer)
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

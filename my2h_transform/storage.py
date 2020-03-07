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

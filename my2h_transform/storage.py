"""
Database handler
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

SQLBase = declarative_base()


class BLT(SQLBase):

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

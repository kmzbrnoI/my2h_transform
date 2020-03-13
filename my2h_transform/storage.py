"""
Database handler
"""

from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String, Boolean
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

    def __str__(self) -> str:
        return self.shortname

    def output_name(self) -> str:
        return self.shortname.title()

    __repr__ = __str__


class Railway(BASE):

    __tablename__ = 'railways'

    id = Column(Integer, primary_key=True)
    shortname = Column(String)
    name = Column(String)
    safeguard = Column(String)

    def __str__(self) -> str:
        return self.shortname

    __repr__ = __str__


class Track_Section(BASE):

    __tablename__ = 'track_sections'

    id = Column(Integer, primary_key=True)
    railway = Column(Integer, ForeignKey(Railway.id))
    name = Column(String)
    safeguard = Column(String)
    velocity = Column(Integer)
    det1 = Column(String)  # tohle ukazuje do tabulky B
    det2 = Column(String)
    det3 = Column(String)
    det4 = Column(String)
    boost = Column(Integer)
    power_source = Column(String)
    in1L = Column(String)
    in2L = Column(String)
    in1S = Column(String)
    in2S = Column(String)
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

    def __str__(self) -> str:
        return self.name

    __repr__ = __str__


class Signal(BASE):

    __tablename__ = 'signals'

    id = Column(Integer, primary_key=True)
    signal_type = Column(String)
    control_area = Column(Integer, ForeignKey(Control_Area.id))
    name = Column(String)
    shunt = Column(Integer)
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
    skupina1 = Column(String)
    skupina2 = Column(String)
    skupina3 = Column(String)
    trat1 = Column(Integer, ForeignKey(Railway.id))
    trat2 = Column(String)

    def __str__(self) -> str:
        return f'{self.control_area}: {self.name}'

    __repr__ = __str__


class Junction(BASE):

    __tablename__ = 'junctions'

    id = Column(Integer, primary_key=True)
    control_area = Column(Integer, ForeignKey(Control_Area.id))
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
    second_ref = Column(Integer, default=0)

    def __str__(self) -> str:
        return f'{self.control_area}: {self.name}'

    __repr__ = __str__


class BLM(BASE):

    __tablename__ = 'blms'

    id = Column(Integer, primary_key=True)
    control_area = Column(Integer, ForeignKey(Control_Area.id))
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

    def __str__(self) -> str:
        return f'{self.control_area}: {self.name}'

    __repr__ = __str__


class BLK(BASE):

    __tablename__ = 'blks'

    id = Column(Integer, primary_key=True)
    control_area = Column(Integer, ForeignKey(Control_Area.id))
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

    def __str__(self) -> str:
        return f'{self.control_area}: {self.name}'

    __repr__ = __str__


class BLUV(BASE):

    __tablename__ = 'bluvs'

    id = Column(Integer, primary_key=True)
    control_area = Column(Integer, ForeignKey(Control_Area.id))
    name = Column(String)
    direction = Column(Integer)
    souhlas = Column(Integer)
    nvID = Column(String)
    pocetID = Column(Integer)

    def __str__(self) -> str:
        return f'{self.control_area}: {self.name}'

    __repr__ = __str__


class BLQ(BASE):

    __tablename__ = 'blqs'

    id = Column(Integer, primary_key=True)
    control_area = Column(Integer, ForeignKey(Control_Area.id))
    name = Column(String)
    bluv = Column(String)
    pocetID = Column(Integer)

    def __str__(self) -> str:
        return f'{self.control_area}: {self.name}'

    __repr__ = __str__


class BLEZ(BASE):

    __tablename__ = 'blezs'

    id = Column(Integer, primary_key=True)
    control_area = Column(Integer, ForeignKey(Control_Area.id))
    name = Column(String)
    blv = Column(String)


class Disconnector(BASE):

    __tablename__ = 'disconnectors'

    id = Column(Integer, primary_key=True)
    control_area = Column(Integer, ForeignKey(Control_Area.id))
    name = Column(String)
    blk = Column(String)
    out = Column(String)

    def __str__(self) -> str:
        return f'{self.control_area}: {self.name}'

    __repr__ = __str__


class BLP(BASE):

    __tablename__ = 'blps'

    id = Column(Integer, primary_key=True)
    control_area = Column(Integer, ForeignKey(Control_Area.id))
    name = Column(String)
    typ = Column(String)
    inUzav = Column(String)
    inOtev = Column(String)
    inAnulace = Column(String)
    inUzZav = Column(String)
    outUzav = Column(String)
    outNouzOtev = Column(String)
    outBlokPoz = Column(String)

    def __str__(self) -> str:
        return f'{self.control_area}: {self.name}'

    __repr__ = __str__


class IR(BASE):

    __tablename__ = 'irs'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    inp = Column(String)

    def __str__(self) -> str:
        return self.name

    __repr__ = __str__


class Drive_Path(BASE):

    __tablename__ = 'drive_paths'

    id = Column(Integer, primary_key=True)
    typ = Column(Integer)
    control_area = Column(Integer, ForeignKey(Control_Area.id))
    start_id = Column(Integer)
    end_id = Column(Integer)
    velocity = Column(Integer)
    nedostVzdalenost = Column(Integer)
    var_bod_0 = Column(Integer)
    var_bod_1 = Column(Integer)
    var_bod_2 = Column(Integer)
    var_bod_3 = Column(Integer)
    var_bod_4 = Column(Integer)
    blocks = Column(String)
    prestavniky = Column(String)
    odvraty_mimo = Column(String)
    odvraty_v = Column(String)
    volnosti = Column(String)

    def __str__(self) -> str:
        return str(self.id)

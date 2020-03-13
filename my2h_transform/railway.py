from typing import Dict, Tuple

from storage import Control_Area, Railway

DIR_A_TO_B = 1
DIR_B_TO_A = 2
Railway_Id = int
Control_Area_Id = int
Direction = int


def section_directions(session) -> Dict[Tuple[Railway_Id, Control_Area_Id], Direction]:
    result = {}
    railways = session.query(Railway).all()
    for railway in railways:
        areas = railway.shortname.split(' ')[0].split('-')
        area1_name, area2_name = list(map(lambda x: x.lower(), areas))

        area1 = session.query(Control_Area).filter(Control_Area.shortname == area1_name).first()
        area2 = session.query(Control_Area).filter(Control_Area.shortname == area2_name).first()

        assert area1 is not None, f'{area1_name} not found!'
        assert area2 is not None, f'{area2_name} not found!'

        result[(railway.id, area1.id)] = DIR_A_TO_B
        result[(railway.id, area2.id)] = DIR_B_TO_A

    return result

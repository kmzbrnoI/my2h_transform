from utils import get_block_by_id
from storage import Signal, Drive_Path, Composite_Drive_Path

from typing import Dict, List


def _ignore(drive_path):
    if (drive_path.start_id in [3415, 3416, 3417, 3418, 3419, 3420, 3421, 3422, 3423, 3424] and
        drive_path.end_id in [3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109]):
        # Hrad smycka
        return True

    return False


class Valued_Drive_Path:
    def __init__(self, id_: int, typ: int, start: Signal, variant_points: List['Block'],
                 target: 'Block', last_block: 'Block'):
        self.id = id_
        self.typ = typ
        self.start = start
        self.variant_points = variant_points
        self.target = target
        self.last_block = last_block

    def __str__(self) -> str:
        return self.start.name + ' > ' + self.last_block.name

    __repr__ = __str__


def _get_drive_paths(session) -> List[Valued_Drive_Path]:

    all_paths = []

    drive_paths = session.query(Drive_Path).order_by(Drive_Path.id).all()
    for path in drive_paths:
        if _ignore(path):
            continue

        variant_points = []
        for bod in [path.var_bod_0, path.var_bod_1, path.var_bod_2, path.var_bod_3]:
            variant_point = get_block_by_id(session, bod)
            if variant_point:
                variant_points.append(variant_point)

        last_block = get_block_by_id(session, path.blocks.split(';')[-1])

        all_paths.append(Valued_Drive_Path(
            id_=path.id,
            typ=path.typ,
            start=get_block_by_id(session, path.start_id),
            variant_points=variant_points,
            target=get_block_by_id(session, path.end_id),
            last_block=last_block,
        ))

    return all_paths


def _get_paths_by_signals(all_paths, path_type) -> Dict[int, List[Valued_Drive_Path]]:

    paths_by_signals = {}

    for path in all_paths:

        assert isinstance(path.start, Signal), 'ERROR: Path [{}] doesn\'t start with Signal'.format(path.id)

        if path.typ == path_type:
            signal_id = path.start.id
            if signal_id not in paths_by_signals.keys():
                paths_by_signals[signal_id] = []
            paths_by_signals[signal_id].append(path)

    return paths_by_signals


def _trace_paths(session, all_paths, paths_by_signals, path) -> List[List[Valued_Drive_Path]]:

    if not isinstance(path.last_block, Signal):
        return [[path]]

    end_signal = path.last_block.id
    direction = path.last_block.direction

    if end_signal not in paths_by_signals:
        return [[path]]  # no next paths

    next_paths = filter(lambda p: p.start.direction == path.last_block.direction,
                        paths_by_signals[end_signal])

    traces = []
    for possible_path in next_paths:
        traces_ = _trace_paths(session, all_paths, paths_by_signals, possible_path)
        for trace in traces_:
            trace.insert(0, path)
        traces.extend(traces_)

    return traces


def create_jmc(session):

    all_paths = _get_drive_paths(session)
    train_paths_by_signals = _get_paths_by_signals(all_paths, 1)
    shunt_paths_by_signals = _get_paths_by_signals(all_paths, 2)

    train_traces = []
    for path in all_paths:
        train_traces.append(_trace_paths(session, all_paths, train_paths_by_signals, path))

    # shunt_traces = []
    # for path in all_paths:
    #     shunt_traces.append(_trace_paths(session, all_paths, shunt_paths_by_signals, path))

    for trace in train_traces[0]:
        print(trace)
    # for item in train_traces:
    #     print(item)

    # for item in shunt_traces:
    #     print(item)

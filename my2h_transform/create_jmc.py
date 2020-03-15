from utils import get_block_by_id
from storage import Signal, Drive_Path, Composite_Drive_Path


def _get_drive_paths(session):

    all_paths = []

    drive_paths = session.query(Drive_Path).order_by(Drive_Path.id).all()
    for path in drive_paths:

        variant_points = []
        for bod in [path.var_bod_0, path.var_bod_1, path.var_bod_2, path.var_bod_3]:
            variant_point = get_block_by_id(session, bod)
            if variant_point:
                variant_points.append(variant_point)

        last_block = get_block_by_id(session, path.blocks.split(';')[-1])

        all_paths.append({
            'id': path.id,
            'typ': path.typ,
            'start': get_block_by_id(session, path.start_id),
            'variant_points': variant_points,
            'target': get_block_by_id(session, path.end_id),
            'last_block': last_block,
        })

    return all_paths


def _get_paths_by_signals(all_paths, path_type):

    paths_by_signals = []

    for path in all_paths:

        assert isinstance(path['start'], Signal), 'ERROR: Path [{}] doesn\'t start with Signal'.format(path['id'])

        if path['start'].id not in [ e['signal_id'] for e in paths_by_signals ] and path['typ'] == path_type:

            paths_from_signal = []
            for other_path in all_paths:
                if path['start'].id == other_path['start'].id and other_path['typ'] == path_type:
                    paths_from_signal.append(other_path)

            paths_by_signals.append({
                'signal_id': path['start'].id,
                'paths': paths_from_signal,
            })

    return paths_by_signals


def _trace_paths(session, all_paths, paths_by_signals, path):

    if isinstance(path['last_block'], Signal):
        pass
    else:
        return path

    end_signal = path['last_block'].id
    direction = path['last_block'].direction

    possible_paths = []
    for item in paths_by_signals:
        if end_signal == item['signal_id'] and get_block_by_id(session, item['signal_id']).direction == direction:
            possible_paths = item['paths']

    traces = []
    for possible_path in possible_paths:
        trace = _trace_paths(session, all_paths, paths_by_signals, possible_path)
        traces.append(trace)

    return traces


def create_jmc(session):

    all_paths = _get_drive_paths(session)
    train_paths_by_signals  = _get_paths_by_signals(all_paths, 1)
    shunt_paths_by_signals  = _get_paths_by_signals(all_paths, 2)

    train_traces = []
    for path in all_paths:
        train_traces.append(_trace_paths(session, all_paths, train_paths_by_signals, path))

    shunt_traces = []
    for path in all_paths:
        shunt_traces.append(_trace_paths(session, all_paths, train_paths_by_signals, path))

    for item in train_traces:
        print(item)

    for item in shunt_traces:
        print(item)

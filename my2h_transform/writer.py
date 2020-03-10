from storage import Control_Area, Railway, Track_Section, BLM, BLK, Signal, Junction, Disconnector


def prepare_data_for_section(section, parent, capitalize=True):

    if capitalize:
        title = '{} {}'.format(parent.shortname.split(' ', 1)[0].capitalize(), section.name)
    else:
        title = '{} {}'.format(parent.shortname.split(' ', 1)[0], section.name)

    data = {
        'nazev': title,
        'typ': 1,
    }

    rcs_count = 0
    for det in (section.det1, section.det2, section.det3, section.det4):
        if det != '0:0':
            rcs_count = rcs_count + 1

    RCSb0 = int(section.det1.split(':', 1)[0])
    RCSp0 = int(section.det1.split(':', 1)[1])
    RCSb1 = int(section.det2.split(':', 1)[0])
    RCSp1 = int(section.det2.split(':', 1)[1])
    RCSb2 = int(section.det3.split(':', 1)[0])
    RCSp2 = int(section.det3.split(':', 1)[1])
    RCSb3 = int(section.det4.split(':', 1)[0])
    RCSp3 = int(section.det4.split(':', 1)[1])

    if rcs_count != 0:
        data['RCScnt'] = rcs_count

    if RCSb0 != 0:
        data['RCSb0'] = RCSb0
        data['RCSp0'] = RCSp0

    if RCSb1 != 0:
        data['RCSb1'] = RCSb1
        data['RCSp1'] = RCSp1

    if RCSb2 != 0:
        data['RCSb2'] = RCSb2
        data['RCSp2'] = RCSp2

    if RCSb3 != 0:
        data['RCSb3'] = RCSb3
        data['RCSp3'] = RCSp3

    # TODO: delka neni nactena z dat
    data['delka'] = 100
    data['zesil'] = section.boost

    return data


def write_track_section(session, config):

    for section, railway in session.query(
            Track_Section, Railway).filter(Track_Section.railway == Railway.id).order_by(Track_Section.id):

        config[section.id] = prepare_data_for_section(section, railway, capitalize=False)


def write_section(session, config):

    # BLM (also with BLS dataset)
    for section, area in session.query(
            BLM, Control_Area).filter(BLM.control_area == Control_Area.id).order_by(BLM.id):

        config[section.id] = prepare_data_for_section(section, area)

    # BLK
    for section, area in session.query(
            BLK, Control_Area).filter(BLM.control_area == Control_Area.id).order_by(BLM.id):

        config[section.id] = prepare_data_for_section(section, area)


def write_signal(session, config):

    for signal, area in session.query(
            Signal, Control_Area).filter(Signal.control_area == Control_Area.id).order_by(Signal.id):

        data = {
            'nazev': '{} {}'.format(area.shortname.split(' ', 1)[0].capitalize(), signal.name),
            'typ': 3,
        }

        rcs_count = 0
        for det in (signal.out1, signal.out2, signal.out3, signal.out4):
            if det != '0:0':
                rcs_count = rcs_count + 1

        RCSb0 = int(signal.out1.split(':', 1)[0])
        RCSp0 = int(signal.out1.split(':', 1)[1])
        RCSb1 = int(signal.out2.split(':', 1)[0])
        RCSp1 = int(signal.out2.split(':', 1)[1])
        RCSb2 = int(signal.out3.split(':', 1)[0])
        RCSp2 = int(signal.out3.split(':', 1)[1])
        RCSb3 = int(signal.out4.split(':', 1)[0])
        RCSp3 = int(signal.out4.split(':', 1)[1])

        if rcs_count != 0:
            data['RCScnt'] = rcs_count

        if RCSb0 != 0:
            data['RCSb0'] = RCSb0
            data['RCSp0'] = RCSp0

        if RCSb1 != 0:
            data['RCSb1'] = RCSb1
            data['RCSp1'] = RCSp1

        if RCSb2 != 0:
            data['RCSb2'] = RCSb2
            data['RCSp2'] = RCSp2

        if RCSb3 != 0:
            data['RCSb3'] = RCSb3
            data['RCSp3'] = RCSp3

        if rcs_count:
            data['OutType'] = 0

        config[signal.id] = data


def write_junction(session, config):

    for junction, area in session.query(
            Junction, Control_Area).filter(Junction.control_area == Control_Area.id).order_by(Junction.id):

        data = {
            'nazev': '{} {}'.format(area.shortname.split(' ', 1)[0].capitalize(), junction.name),
            'typ': 0,
        }

        RCSb0 = int(junction.in1.split(':', 1)[0])
        RCSp0 = int(junction.in1.split(':', 1)[1])
        RCSb1 = int(junction.in2.split(':', 1)[0])
        RCSp1 = int(junction.in2.split(':', 1)[1])
        RCSb2 = int(junction.out1.split(':', 1)[0])
        RCSp2 = int(junction.out1.split(':', 1)[1])
        RCSb3 = int(junction.out2.split(':', 1)[0])
        RCSp3 = int(junction.out2.split(':', 1)[1])

        data['RCScnt'] = 4 if junction.hw else 0

        if RCSb0 != 0:
            data['RCSb0'] = RCSb0
            data['RCSp0'] = RCSp0

        if RCSb1 != 0:
            data['RCSb1'] = RCSb1
            data['RCSp1'] = RCSp1

        if RCSb2 != 0:
            data['RCSb2'] = RCSb2
            data['RCSp2'] = RCSp2

        if RCSb3 != 0:
            data['RCSb3'] = RCSb3
            data['RCSp3'] = RCSp3

        config[junction.id] = data


def write_disconnector(session, config):

    for disconnector, area in session.query(
            Disconnector, Control_Area).filter(Disconnector.control_area == Control_Area.id).order_by(Disconnector.id):

        data = {
            'nazev': '{} {}'.format(area.shortname.split(' ', 1)[0].capitalize(), disconnector.name),
            'typ': 8,
        }

        RCSb0 = int(disconnector.out.split(':', 1)[0])
        RCSp0 = int(disconnector.out.split(':', 1)[1])

        data['RCScnt'] = 1

        data['RCSb0'] = RCSb0
        data['RCSp0'] = RCSp0

        config[disconnector.id] = data

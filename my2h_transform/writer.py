from storage import Control_Area, Railway, Track_Section, Signal


def write_track_section(session, config):

    for section, railway in session.query(
            Track_Section, Railway).filter(Track_Section.railway == Railway.id).order_by(Track_Section.id):

        data = {
            'nazev': '{} {}'.format(railway.shortname.split(' ', 1)[0], section.name),
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

        config[section.id] = data


def write_signal(session, config):

    for signal, area in session.query(
            Signal, Control_Area).filter(Signal.control_area == Control_Area.id).order_by(Signal.id):

        data = {
            'nazev': '{} {}'.format(area.shortname.split(' ', 1)[0], signal.name),
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

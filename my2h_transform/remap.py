from storage import Control_Area

def remap_control_area(reid, source_session, output_session):

    items = []
    for old_item in source_session.query(Control_Area).all():

        print(old_item.id)
        print(reid[old_item.id])

        item = Control_Area(
            id=reid[old_item.id],
            shortname=old_item.shortname,
            name=old_item.name
        )
        items.append(item)

    output_session.add_all(items)
    output_session.commit()

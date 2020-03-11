from utils import get_block_by_id


def show_path(session, path) -> None:
    print(f'ID: {path.id}')
    print('Typ: ' + str(path.typ))
    print('Start: ' + str(get_block_by_id(session, int(path.start_id))))
    print('End: ' + str(get_block_by_id(session, int(path.end_id))))

    print('Blocks:')
    print('\n'.join(
        '\t'+str(get_block_by_id(session, int(block)))
        for block in path.blocks.split(';')
    ))

    print('Prestavniky:')
    for prest in path.prestavniky.split(';'):
        id_, poloha = prest.split('-')
        name = str(get_block_by_id(session, int(id_)))
        poloha = '+' if poloha == '1' else '-'
        print(f'\t{name} {poloha}')

    if path.odvraty_mimo is not None:
        print('Odvraty mimo:')
        for odvrat in path.odvraty_mimo.split(';'):
            id1, poloha1, id2, poloha2 = odvrat.split('-')
            name1 = str(get_block_by_id(session, int(id1)))
            name2 = str(get_block_by_id(session, int(id2)))
            poloha1 = '+' if poloha1 == '1' else '-'
            poloha2 = '+' if poloha2 == '1' else '-'
            print(f'\t{name1} {poloha1}, {name2} {poloha2}')


    if path.odvraty_v is not None:
        print('Odvraty v:')
        for odvrat in path.odvraty_v.split(';'):
            id_, poloha = prest.split('-')
            name = str(get_block_by_id(session, int(id_)))
            poloha = '+' if poloha == '1' else '-'
            print(f'\t{name} {poloha}')

    if path.var_bod_0 != 0:
        print('Var bod 0: ' + str(get_block_by_id(session, int(path.var_bod_0))))

    if path.volnosti is not None:
        print('Volnosti:')
        for volnost in path.volnosti.split(';'):
            id1, id2, poloha = volnost.split('-')
            name1 = str(get_block_by_id(session, int(id1)))
            name2 = str(get_block_by_id(session, int(id2)))
            print(f'\t{name1} {name2} {poloha}')

import csv
import os.path

FACTS_PATH = "KB_PathSearchAgent/facts.pl"
CSV_PATH = "planimetry.csv"

"""
script che automatizza l'immissione di fatti nella base di conoscenza basandosi sui dati della planimetria dell'edificio
"""


def populate_kb_facts(path):
    """
    scrive su 2 file prolog le clausole che assiomatizzano i fatti riguardanti planimetria e impianto elettrico
    :param path: percorso del file
    """
    hallways, offices, elevators, stairs, baths, relax_areas, misc = read_and_process_planimetry(CSV_PATH)

    # inserisco le informazioni sottoforma di clausole all'interno della lista clauses
    clauses = []
    # clausole per l'impianto elettrico
    ee_clauses = []

    # office(X), X è un ufficio
    for office in offices:
        clauses.append(f'office({office[0]})')

    # hallway(X), X è un corridoio
    for hallway in hallways:
        clauses.append(f'hallway({hallway[0]})')

    # stair(X), X è una scala
    for stair in stairs:
        clauses.append(f'stair({stair[0]})')

    # elevator(X), X è un ascensore
    for elevator in elevators:
        clauses.append(f'elevator({elevator[0]})')

    # bath(X), X è un bagno
    for bathroom in baths:
        clauses.append(f'bath({bathroom[0]})')

    # relax(X), X è un'area relax
    for relax in relax_areas:
        clauses.append(f'relax({relax[0]})')

    for m in misc:
        clauses.append(f'misc({m[0]})')

    places = offices + hallways + stairs + elevators + baths + relax_areas + misc

    for place in places:
        # is_light(Luce), Luce è una luce
        ee_clauses.append(f"is_light(light_{place[0]})")
        # location(Luce,Stanza), Luce è nella Stanza
        ee_clauses.append(f"location(light_{place[0]},{place[0]})")
        # controlled_by(Luce, Switch), Luce è controllata dall'interrutore Switch
        ee_clauses.append(f"controlled_by(light_{place[0]},switch_{place[0]})")
        # is_heater(Device), Device è un climatizzatore
        ee_clauses.append(f"is_heater(heater_{place[0]})")
        # location(Device, Stanza), il dispositivo (non luce) è nella stanza
        ee_clauses.append(f"location(heater_{place[0]},{place[0]})")

        # coordinate(Nodo,X,Y,Z), Nodo ha coordinate X, Y
        clauses.append(f'coordinates({place[0]},{place[1]},{place[2]},{place[3]})')
        # floor(X,Y), X è al piano Y
        clauses.append(f'floor({place[0]},{place[3]})')
        for neighbor in place[4]:
            # edge(X,Y), X è collegato direttamente a Y
            clauses.append(f'edge({place[0]},{neighbor})')

    clauses.sort()
    ee_clauses.sort()

    # scrittura su file della KB riguardante la planimetria
    f_prolog = open(path, "w")
    # scrive tutte le clausole mettendo un punto alla fine e andando a capo per ognuna
    f_prolog.writelines('.\n'.join(clauses) + '.\n')
    f_prolog.close()

    # scrittura su file della KB riguardante l' impianto elettrico
    ee_f_prolog = open("KB_DiagnosticAgent/ee_facts.pl", "w")
    ee_f_prolog.writelines('.\n'.join(ee_clauses) + '.\n')
    ee_f_prolog.close()


def parse_name(name):
    """
    suddivide la stringa nomeStruttura_X_Y_piano in nomeStruttura_X_Y_piano, int X, int Y, int piano
    :param name:
    :return: nomeStruttura_X_Y_piano, int X, int Y, int piano
    """
    parts = name.split('_')
    return [name] + [int(part) for part in parts[1:]]


def read_and_process_planimetry(filename):
    """
    Legge da filename.csv i nodi e i vicini della planimetria e li formatta in questo modo:
    [nomeStruttura_X_Y_piano, X, Y, piano, [lista dei nodi adiacenti]],
    li salva in liste diverse a seconda dell'individuo
    :param filename: file .csv strutturato: nomeStruttura_X_Y_piano;vicino1,vicino2,...
    :return: lista per ogni individuo identificato
    """
    hallways = []
    offices = []
    elevators = []
    stairs = []
    baths = []
    relax_areas = []
    misc = []

    with open(filename, mode='r', encoding='utf-8-sig') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            if row:
                entity_type, *entity_data = row
                main_entity_data = parse_name(entity_type)
                # crea una lista di stringhe, ciascuna contenente un vicino
                sub_entities_list = [entity for entity in entity_data[0].split(',')]
                main_entity_data.append(sub_entities_list)

                # se inizia per "X" inseriscilo nella stringa adatta
                if entity_type.startswith('corridoio'):
                    hallways.append(main_entity_data)
                elif entity_type.startswith('ascensore'):
                    elevators.append(main_entity_data)
                elif entity_type.startswith('ufficio'):
                    offices.append(main_entity_data)
                elif entity_type.startswith('scala'):
                    stairs.append(main_entity_data)
                elif entity_type.startswith('bagno'):
                    baths.append(main_entity_data)
                elif entity_type.startswith('areaRelax'):
                    relax_areas.append(main_entity_data)
                elif entity_type.startswith('salaConsiliare'):
                    misc.append(main_entity_data)

        # correzione di salaConsiliare in sala_consiliare
        misc[0][0] = "sala_consiliare_5_12_0"
        # correzione di areaRelax in area_relax
        relax_areas[0][0] = "area_relax_5_28_0"

    return hallways, offices, elevators, stairs, baths, relax_areas, misc


# Avvio dello script
populate_kb_facts(FACTS_PATH)

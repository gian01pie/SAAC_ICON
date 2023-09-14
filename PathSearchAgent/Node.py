from KnowledgeBase import KnowledgeBase


class Node:
    """
    Classe Node che modella un nodo del grafo di ricerca
    """

    def __init__(self, name, kb: KnowledgeBase):
        self.kb = kb
        self.label = name
        # faccio una query per le coordinate, raccolgo i risultati in una lista,
        # poichè so che esiste un solo valore di X e uno solo di Y per questo nodo,
        # so che la lista avrà un solo element, quindi prendo il primo elemento
        # che so essere un dizionario con chiavi X e Y ed i valori ad esso associati
        # sono le coordinate
        q_coordinates = kb.query_kb(f"coordinates({self.label}, X, Y, Z)")[0]
        self.x = q_coordinates['X']
        self.y = q_coordinates['Y']
        self.floor = q_coordinates["Z"]

        self.neighbors = []
        for neighbor in list(kb.prolog.query(f"edge({self.label}, X)")):
            self.neighbors.append(neighbor["X"])

    def __repr__(self):
        """
        rappresentazione di un nodo come stringa
        """
        return f"nodo: {self.label}, ({self.x},{self.y}), piano: {self.floor}, " \
               f"\n\tvicini: {self.neighbors}\n"

    def get_label(self) -> str:
        return self.label

    def get_floor(self):
        return self.floor

    def get_neighbors(self) -> list:
        return self.neighbors

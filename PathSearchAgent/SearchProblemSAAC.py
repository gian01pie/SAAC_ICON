import math

from AILibraries.searchProblem import Search_problem_from_explicit_graph, Arc
from KnowledgeBase import KnowledgeBase
from PathSearchAgent.Node import Node
from DiagnosticAgent import ElectricalDiagnosticAgent


class SearchProblemSAAC(Search_problem_from_explicit_graph):
    def __init__(self, kb: KnowledgeBase, da : ElectricalDiagnosticAgent, start, goals):
        """
        Elabora le informazioni della planimetria in nodi e costruisce gli archi tra i nodi se sono disponibili
        :param kb: riferimoento alla base di conoscenza
        :param da: riferimento all'agente diagnostico
        :param start: nodo di partenza del percorso
        :param goals: nodo di arrivo del percorso
        """
        self.kb = kb
        hmap_heuristic = {}
        arcs = []

        # per prima cosa creo l'insieme dei nodi
        nodes = self.get_set_of_nodes()
        node_labels = self.get_set_of_node_names()

        # calcolo l'euristica per ogni nodo
        for node in nodes:
            # Se il nodo è un ascensore
            if "ascensore" in node.get_label():
                # Se il magnetotermico è attivo l'ascensore non funziona
                if da.check_magnetothermal_in_room(node.get_label()):
                    # Quindi non è utilizzabile e non lo inserisco nel grafo
                    continue
            hmap_heuristic[node.get_label()] = self.underestimate_euclidean_distance(node.get_label(), goals)
            for neighbor in node.get_neighbors():
                # Se il nodo è un ascensore
                if "ascensore" in neighbor:
                    # Se il magnetotermico è attivo l'ascensore non funziona
                    if da.check_magnetothermal_in_room(neighbor):
                        # Quindi non è utilizzabile e non lo inserisco nel grafo
                        continue
                # per ogni vicino del nodo analizzato aggiungo un arco
                distance = self.euclidean_distance(node.get_label(), neighbor)
                arcs.append(Arc(node.get_label(), neighbor, distance))

        super().__init__(nodes=node_labels, arcs=arcs, start=start, goals=goals, hmap=hmap_heuristic)
        print("Creazione del grafo di ricerca terminata con successo\n")

    def get_set_of_nodes(self):
        """
        :return: restituisce un insieme di oggetti di tipo Node
        """
        nodes = set()
        for node in self.kb.query_kb("node(X)"):
            nodes.add(Node(node['X'], self.kb))
        return nodes

    def get_set_of_node_names(self):
        """
        :return: restituisce un insieme di stringhe contenenti le etichette dei nodi
        """
        nodes_label = set()
        for node in self.get_set_of_nodes():
            nodes_label.add(node.get_label())
        return nodes_label

    def euclidean_distance(self, start, goal):
        """
        Calcola la distanza euclidea tra due nodi interrogando la KB:
        sqrt((x2-x1)^2 + (y2-y1)^2 + (z2-z1)^2)
        :param start: nome nodo di partenza
        :param goal: nome nodo di arrivo
        :return: restituisce la distanza euclidea tra start e goal
        """
        dist = self.kb.query_kb(f"distance({start},{goal},D)")[0]["D"]
        return dist

    def underestimate_euclidean_distance(self, start, goal_list):
        """
        Calcola la sottostima delle distanze euclidee tra un nodo e una lista di nodi:
        sqrt((x2-x1)^2 + (y2-y1)^2 + (z2-z1)^2)
        :param start: nome nodo di partenza
        :param goal_list: lista di stringhe dei nomi dei nodi di arrivo
        :return: restituisce la distanza euclidea minima tra start e tutti i nodi goal
        """
        d = math.inf
        for goal in goal_list:
            # facendo il minimo delle distanze si ottiene una sottostima di tutte le distanze
            d = min(d, self.euclidean_distance(start, goal))
        return d

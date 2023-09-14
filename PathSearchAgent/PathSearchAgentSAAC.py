import time

from AILibraries.searchGeneric import AStarSearcher
from AILibraries.searchMPP import SearcherMPP
from KnowledgeBase import KnowledgeBase
from PathSearchAgent.SearchProblemSAAC import SearchProblemSAAC
from DiagnosticAgent import ElectricalDiagnosticAgent

DEFAULT_START_NODE = "corridoio_16_7_0"
DEFAULT_GOAL_NODE = ["ascensore_20_4_1"]

class PathSearchAgentSAAC:
    def __init__(self, kb: KnowledgeBase, da : ElectricalDiagnosticAgent):
        self.kb = kb
        # riferimento all'agente diagnostico
        self.da = da

    def run(self):
        """
        esegue la logica principale dell'agente
        """
        while True:
            self.da.check_devices()

            self.print_menu()

            # scelta dei nodi di partenza e arrivo
            start = self.get_start_node()
            if not self.is_correct_node(start):
                continue
            goal = self.get_goal_node()
            if not self.is_correct_node(goal[0]):
                continue

            # creazione grafo di ricerca
            problem = SearchProblemSAAC(self.kb, self.da, start, goal)

            # soluzione al problema di ricerca
            solution = self.search_mpp(problem)
            if solution is not None:
                print(f"Cammino trovato: {solution}")
                print(f"costo: {solution.cost}\n")
            else :
                print("Non è stato possibile trovare un cammino")


            while True:
                choice = input("\nVuoi cercare un percorso tra altri 2 nodi ? (y/n)\n")
                if choice.lower() == 'y':
                    break
                if choice.lower() == 'n':
                    return


    def search_a_star(self, problem):
        a_star_searcher = AStarSearcher(problem)
        return a_star_searcher.search()

    def search_mpp(self, problem):
        mpp = SearcherMPP(problem)
        return mpp.search()

    def test_algorithm(self, problem):
        start_time = time.time()
        a_star_searcher = AStarSearcher(problem)
        print(f"Creazione avvenuta in {time.time() - start_time} secondi.\n")
        start_time = time.time()
        solution = a_star_searcher.search()
        print(f"Ricerca terminata in {time.time() - start_time} secondi.\n")
        print("\nA*Searcher:")
        print(f"Cammino trovato: {solution}")
        print(f"costo: {solution.cost}\n")

        start_time = time.time()
        mpp = SearcherMPP(problem)
        print(f"Creazione avvenuta in {time.time() - start_time} secondi.\n")
        start_time = time.time()
        solution_mpp = mpp.search()
        print(f"Ricerca terminata in {time.time() - start_time} secondi.\n")
        print("\nA*Searcher con MPP:")
        print(f"Soluzione: {solution_mpp}")
        print(f"costo: {solution_mpp.cost}\n")

    # def main_menu(self):
    #     self.print_menu()
    #     scelta = input()
    #     if scelta == "1":
    #         pass
    #     elif scelta == "2":
    #         pass
    #     else:
    #         print("Scelta non valida.")

    def print_menu(self):
        print("------------------------------------------------------------------")
        print("SAAC: Ricerca percorso più efficiente tra 2 punti")
        print("------------------------------------------------------------------")
        print("Benvenuto :")

    def get_start_node(self):
        print("Inserisci il luogo di partenza:")
        choice = input("Partenza: ")
        if choice == "":
            return DEFAULT_START_NODE
        return choice

    def get_goal_node(self):
        print("Inserisci il luogo di arrivo:")
        goals = []
        choice = input("Arrivo: ")
        goals.append(choice)
        if choice == "":
            return DEFAULT_GOAL_NODE
        return goals

    def is_correct_node(self, node_name):
        if not self.kb.boolean_query_kb(f"node({node_name})"):
            print(f"Il nodo {node_name} è sbagliato")
            return False
        return True
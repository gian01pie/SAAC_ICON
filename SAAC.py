from DiagnosticAgent.ElectricalDiagnosticAgent import ElectricalDiagnosticAgent
from KnowledgeBase import KnowledgeBase
from PathSearchAgent.PathSearchAgentSAAC import PathSearchAgentSAAC
from PathSearchAgent.SearchProblemSAAC import SearchProblemSAAC


class SAAC:
    """
    Classe che media l'interazione tra il DiagnosticAgent e il PathSearchAgent
    """
    @staticmethod
    def main_menu():
        kb = KnowledgeBase()
        da = ElectricalDiagnosticAgent(kb)
        psa = PathSearchAgentSAAC(kb, da)
        while True:
            SAAC.print_menu()
            choice = input("Inserisci il numero dell'operazione da svolgere:")
            if choice == '1':
                print("Scelto la 1...")
                psa.run()
                continue
            elif choice == '2':
                print("Scelto la 2...")
                da.run()
                continue
            elif choice == 'q':
                print("Arrivederci...")
                return
    @staticmethod
    def print_menu():
        print("------------------------------------------------------------------")
        print("SAAC")
        print("------------------------------------------------------------------")
        print("Menu:")
        print("Scegli una delle possibili operazioni (scrivi \"q\" per uscire):")
        print("\n")
        print("1) Percorso più efficientre tra 2 punti")
        print("2) Stato della rete elettrica")
        print("\n")


if __name__ == '__main__':
    SAAC.main_menu()

    # kb = KnowledgeBase()
    # da = ElectricalDiagnosticAgent(kb)
    # psa = PathSearchAgentSAAC(kb, da)

    # Test diagnostic Agent
    # da.check_devices()
    # da.diagnose("heater_corridoio_11_4_0")

    # Test search algorithm
    # problem = SearchProblemSAAC(kb, da, "corridoio_16_1_0", ["bagno_47_25_1"])
    # psa.test_algorithm(problem)



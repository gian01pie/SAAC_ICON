from pyswip import Prolog
from pyswip.prolog import PrologError

PATH_KB_EE_FACTS = 'KB/KB_DiagnosticAgent/ee_facts.pl'
PATH_KB_EE_RULES = 'KB/KB_DiagnosticAgent/ee_rules.pl'
PATH_KB_PSA_FACTS = "KB/KB_PathSearchAgent/facts.pl"
PATH_KB_PSA_RULES = "KB/KB_PathSearchAgent/rules.pl"
FILES = [PATH_KB_EE_FACTS,PATH_KB_EE_RULES,PATH_KB_PSA_FACTS,PATH_KB_PSA_RULES]


class KnowledgeBase:
    """
    Modella la Knowledge Base in Prolog all'interno di python e fornisce i metodi per effettuare le query
    """

    def __init__(self):
        self.prolog = Prolog()
        for file in FILES:
            self.prolog.consult(file)  # carica i file della KB prolog in memoria

    def query_kb(self, query):
        """
        Interroga la base di conoscenza restituisce una lista di dizionari
        che ha come chiave una variabile e come valore
        il valore assunto da quella variabile per soddisfare la query.
        In caso di query con risposta si/no restituisce un dizionario vuoto
        :param query: query da eseguire
        :return: valore assunto dalla variabile per soddisfare la query o {}
        """
        # Interroga la base di conoscenza Prolog
        try:
            solutions = list(self.prolog.query(query))
        except PrologError as e:
            print("\nIl predicato della query che hai inserito non è corretto")
            print(e)
            print("\n")
            return []
        return solutions

    def boolean_query_kb(self, query):
        """
        Interroga la base di conoscenz acon una query di tipo booleana
        :param query: query booleana da eseguire
        :return: true se la query è soddisfatta false altrimenti
        """
        solutions = False
        try:
            solutions = bool(list(self.prolog.query(query)))
        except PrologError as e:
            print("\nIl predicato della query che hai inserito non è corretto")
            print(e)
            print("\n")
        return solutions

    def add_clause(self, clause):
        """
        Aggiunge una clausola in cima alla base di conoscenza
        :param clause: clausola da inserire
        """
        self.prolog.asserta(clause)

    def remove_clause(self, clause):
        """
        rimuove la clausola che si unifica con quella in input
        :param clause: clausola da rimuovere
        """
        self.prolog.retract(clause)

if __name__ == '__main__':
    kb = KnowledgeBase()
    t = kb.boolean_query_kb("device(outlet1, room1, on, 0.07, 220, 8.5)")
    print(t)

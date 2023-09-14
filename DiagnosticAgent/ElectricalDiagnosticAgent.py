import random

from KnowledgeBase import KnowledgeBase

DEFAULT_DEVICE = "light_corridoio_11_4_0"

# Per randomizzare i dati dai sensori utilizzo una variabile globale per restituire ogni 5 un valore diverso
COUNT = 0
COUNT_2 = 0


class ElectricalDiagnosticAgent:
    """
    Modella un agente diagnostico sullo stato el le anomalie di un impianto elettrico di un edificio
    """
    def __init__(self, kb: KnowledgeBase):
        self.kb = kb
        self.get_sensors_data()
        # Simuliamo il malfunzionamento di qualche dispositivo
        self.kb.remove_clause('device(light_corridoio_11_4_0,_,220,_)')
        self.kb.add_clause('device(light_corridoio_11_4_0,0,220,10001)')
        self.kb.remove_clause('switch(switch_corridoio_11_4_0,_)')
        self.kb.add_clause('switch(switch_corridoio_11_4_0,0.7)')
        self.kb.remove_clause('device(heater_ascensore_20_4_0,_,220,_)')
        self.kb.add_clause('device(heater_ascensore_20_4_0,25,220,1000)')


    def get_sensors_data(self):
        for light in self.kb.query_kb("is_light(X)"):
            current = self.get_light_current()
            hours = random.choice([1000, 6000, 10001])
            self.kb.add_clause(f"device({light['X']},{current},{220},{hours})")
            switches = self.kb.query_kb(f"controlled_by({light['X']},Y)")
            self.kb.add_clause(f"switch({switches[0]['Y']},{current})")
        for device in self.kb.query_kb("is_heater(X)"):
            device_current = self.get_device_current()
            hours = random.choice([1000, 6000, 10001])
            self.kb.add_clause(f"device({device['X']},{device_current},{220},{hours})")

    def get_light_current(self):
        global COUNT
        COUNT += 1
        if COUNT % 5 == 0:
            return 0
        return 0.7

    def get_device_current(self):
        global COUNT_2
        COUNT_2 += 1
        if COUNT_2 % 5 == 0:
            return 15
        return 0

    def run(self):
        """
        Implementa la logica principale dell'agente
        """
        while True:
            self.print_menu()
            choice = input("Inserisci il numero dell'operazione da svolgere:")
            if choice == '1':
                print("Scelto la 1...")
                print("Controllo dell'impianto...")
                faulty_devices = self.check_devices()
                while True:
                    choice = input("Vuoi vedere quali dispositivi non funzionano ? (y/n)\n")
                    if choice.lower() == 'y':
                        self.print_faulty_devices(faulty_devices)
                        break
                    if choice.lower() == 'n':
                        break
                while True:
                    choice = input("Vuoi vedere le possibili soluzioni per i dispositivi non funzionanti ? (y/n)\n")
                    if choice.lower() == 'y':
                        for device in faulty_devices:
                            self.diagnose(device)
                            input("Premi invio per continuare...")
                        break
                    if choice.lower() == 'n':
                        break
                continue
            elif choice == '2':
                print("Scelto la 2...")
                device = self.get_input_device()
                if self.is_correct_device(device):
                    self.diagnose(device)
                continue
            elif choice == 'q':
                break

    def print_menu(self):
        print("------------------------------------------------------------------")
        print("SAAC: Stato dell'impianto elettrico")
        print("------------------------------------------------------------------")
        print("Benvenuto :")
        print("Scegli una delle possibili operazioni (scrivi \"q\" per uscire):")
        print("\n")
        print("1) Verifica lo stato dell'impianto elettrico")
        print("2) Diagnosi di un dispositivo")
        print("\n")

    def check_devices(self):
        """
        Individua se ci sono device che non funzionano correttamente
        :return: lista de nomi dei device che non funzionano
        """
        faulty_devices = self.kb.query_kb('unic_faulty_devices(List)')  # Trova i dispositivi guasti
        if len(faulty_devices) == 0:
            print("Stato dell'impianto elettrico normale.")
            self.check_magnetothermal()
            return faulty_devices
        else:
            list_faulty_devices = faulty_devices[0]['List']
            for device in list_faulty_devices:
                if "ascensore" in device:
                    # fa scattare il magnetotermico per lo stesso scensore per tutti i piani
                    temp = device.replace('heater_', '').replace('_0', '_1')
                    self.kb.boolean_query_kb(f"active_magnetothermal({temp})")
            print(f"Riscontrate {(len(list_faulty_devices))} anomalie nell'impianto ellettrico.")
            self.check_magnetothermal()
            return list_faulty_devices

    def print_faulty_devices(self, faulty_devices):
        """
        stampa i device che non funzionano
        """
        for f_device in faulty_devices:  # Per ogni dispositivo guasto...
            print(
                f"Il dispositivo '{f_device}' è guasto." + (" Probabile sovraccarico." if "heater" in f_device else ""))

    def diagnose(self, device):
        """
        Esegue una diagnosi per individuare il tipo di malfunzionamento del device in input
        :param device: nome del device di cui eseguire la diagnostica
        """
        diagnoses = self.kb.query_kb(f'diagnosis({device}, Problem)')
        if len(diagnoses) == 0:
            print(f"Il {device} funziona correttamente.")
        for diagnose in diagnoses:  # Trova il problema...
            problem = diagnose['Problem']
            print(f"Il problema con {device} è {problem}.")
            self.propose_solution(device, problem)  # Proponi una soluzione
            # self.trace_diagnosis(device, problem)

    def propose_solution(self, device, problem):
        """
        Propone ua possibile soluzione al problema diagnosticato sul device
        :param device: nome del device affetto dal problema
        :param problem: problema che affligge il device
        :return:
        """
        if problem == "broken_light":
            print(
                f"La soluzione per {device} è di sostituire la lampadina.")
        elif problem == 'replace_light':
            print(
                f"La durata di vita di {device} sta per esaurirsi, è consigliata la sostituzione.")
        elif problem == 'overload':
            print(
                f"Si è riscontrato un sovraccarico dovuto a {device}, la corrente è stata rimossa, scollegare dalla presa il dispositivo.")
        else:
            print(
                f"Non sono sicuro di quale sia la soluzione per {device}. Potrebbe essere necessario consultare un elettricista.")

    def get_input_device(self):
        choice = input("Inserire nome dispositivo di cui eseguire la diagnostica: ")
        if choice == "":
            return DEFAULT_DEVICE
        return choice

    def is_correct_device(self, node_name):
        if not self.kb.boolean_query_kb(f"device({node_name},_,_,_)"):
            print(f"Il Dispositivo {node_name} non esiste")
            return False
        return True

    def check_magnetothermal(self):
        rooms_mag_on = self.kb.query_kb("magnetothermal_on(Room)")
        if len(rooms_mag_on) > 0:
            for mag in rooms_mag_on:
                mag_room = mag['Room']
                print(f"Magnetotermico nella stanza '{mag_room}' scattato")

    def check_magnetothermal_in_room(self, room):
        rooms_mag_on = self.kb.boolean_query_kb(f"magnetothermal_on({room})")
        if rooms_mag_on:
            print(f"Magnetotermico nella stanza '{room}' scattato")
        return rooms_mag_on

    # def trace_diagnosis(self, device, problem):
    #     self.kb.query_kb(f"set_prolog_flag(color_term,false), leash(-all), protocol(\"trace_output.txt\"), trace, diagnosis({device}, {problem}), nodebug, noprotocol.")

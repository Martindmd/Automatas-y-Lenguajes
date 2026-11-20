"""
    Equipo docente de Autómatas y Lenguajes Curso 2025-26
    Última modificación: 18 de septiembre de 2025
"""

from collections import deque
from graphviz import Digraph

# Import para to_minimized
from queue import Queue
"""
    Podéis implementar cualquier función auxiliar que consideréis necesaria
"""


def _get_all_transitions(automaton):
    automaton_all_transitions = []
    for state_ini in automaton.transitions:
        for symbol in automaton.transitions[state_ini]:
            for end_state in automaton.transitions[state_ini][symbol]:
                automaton_all_transitions.append(
                    (state_ini, symbol, end_state))
    return automaton_all_transitions


def is_deterministic(automaton):
    """Check whether an automaton is deterministic."""
    checked = set()

    for start_state, symbol, end_state in _get_all_transitions(automaton):
        if symbol is None:
            return False
        if (start_state, symbol) in checked:
            return False
        checked.add((start_state, symbol))

    return True


class FiniteAutomaton:

    def __init__(self, initial_state, states, symbols, transitions, final_states):
        self.initial_state = initial_state
        self.states = states
        self.symbols = symbols
        self.transitions = transitions
            # = {
            #   state1: {Symbolo: [stante_next1, state_next_2...], ...},
            #   state2: {Symbolo: [stante_next1, state_next_2...], ...},
            #   ...
            #}
            # Como puede ser no determinista, hay que dejar la posibilidad de poner mas de
            # un estado por simbolo...
            # symbolo puede ser vacia o lambda, Ya que en
            #  utils.py en el read, se puden crear transiciones sin simbolo...
            # Ya que se inicializa un automata con todo vacio y luego es que se le dan los valores
            


        self.final_states = final_states

        pass

    def add_transition(self, start_state, symbol, end_state):

        # Revisar si symbol, start_state y end_state existen de verdad
        # Crearlos en caso de que no existan
        self.transitions.setdefault(start_state, {})
        self.transitions[start_state].setdefault(symbol, [])


        self.transitions[start_state][symbol].append(end_state)

        pass

    def accepts(self, cadena):

        current_states = [self.initial_state]
        next_states = []


        # Obtener todos los nodos posibles que se consigan desde initialstate Si tienen 
        # transition lambda o transition sin ningun simbolo

        for estado in current_states:
            for destino in self.transitions.get(estado, {}).get(None, []):
                if destino not in current_states:
                    current_states.append(destino)





        for symbol in cadena:

            # Checkeo para SALIR
            if not current_states:
                return False



            # Revisar ssi el Simbolo es aceptable
            if symbol in self.symbols:                

                for estado in self.transitions:
                    if estado in current_states:
                        next_states.extend(self.transitions.get(estado, {}).get(symbol, []))


            # Para el segundo simbolo(s): revisar si algunos de los estados conseguidos anteriormente
            # aceptan nuevos simbolos sin ninguna transcicion (lambda), y obtener nuevos estados para cada uno

            for estado in next_states:
                for destino in self.transitions.get(estado, {}).get(None, []):
                    if destino not in next_states:
                        next_states.append(destino)

            
            current_states = next_states
            next_states = []
        


        for state in current_states:
            if state in self.final_states:
                return True

        return False #
    
    def to_deterministic(self):
        # Obtener todos los nodos posibles que se consigan desde initialstate Si tienen 
        # transition lambda o transition sin ningun simbolo
        initial_states = [self.initial_state]
        #for estado in initial_states:
        i = 0
        while i < len(initial_states):
            estado = initial_states[i]
            for destino in self.transitions.get(estado, {}).get(None, []):
                if destino not in initial_states:
                    initial_states.append(destino)
            i+=1


        initial_states = tuple(sorted(initial_states)) #sorted?
        queue = deque([initial_states])
        visited = set([initial_states])


        # Ej del video: Q  = q1, q2, q3
        #               Q' = q1->{q1,q2}|None || [q1, q2] -> simismo|{q3}|| {q3}->{q2}|{q3} || {q2}->{q1,q2}|{q3}
        # States = {
                    #           q1: {0: [q1, q2], 1: None}
                    # NEW= [q1,q2]: {0: [q1, q2], [q3]}
                    #           q3: {0: [q2], 1: [q3]},
                    #           q2: {0: [q2], 1: [q3]},
                    #   ...
                    #}
        
        #states = [str(y[1]) for x in tabla for y in x[1] if y[1] not in states and y[1] != None]
        new_transitions = {}    
        new_final_states = set()

        while queue:
            current_states = queue.popleft()
            
            # Comprobamos si este conjunto de estados contiene algún estado final original
            # Si es asi, este nuevo estado también es final.
            if any(state in self.final_states for state in current_states):
                new_final_states.add(current_states)


            new_transitions[current_states] = {}

            for symbol in self.symbols:
                next_states_list = []
                
                for state in current_states:
                    destinations = self.transitions.get(state, {}).get(symbol, [])
                    for dest in destinations:
                        if dest not in next_states_list:
                            next_states_list.append(dest)

                # Obtener todos los nodos posibles que se consigan Si tienen 
                # transition lambda o transition sin ningun simbolo
                i = 0
                while i < len(next_states_list):
                    estado = next_states_list[i]
                    for destino in self.transitions.get(estado, {}).get(None, []):
                        if destino not in next_states_list:
                            next_states_list.append(destino)
                    i += 1

                next_states_tuple = tuple(sorted(next_states_list))

                if next_states_tuple not in visited:
                    visited.add(next_states_tuple)
                    queue.append(next_states_tuple)
                    
                new_transitions[current_states][symbol] = [next_states_tuple]


        # Para la creacion del Automata, convertir estados a strings

        final_transitions_dict = {}
        for start_set, transitions in new_transitions.items():
            start_str = "{" + ",".join(sorted(start_set)) + "}"
            final_transitions_dict[start_str] = {}
            for symbol, dest_list in transitions.items():
                final_transitions_dict[start_str][symbol] = ["{" + ",".join(sorted(dest_set)) + "}" for dest_set in dest_list]


        final_states_list = ["{" + ",".join(sorted(s)) + "}" for s in visited]
        final_final_states = ["{" + ",".join(sorted(s)) + "}" for s in new_final_states]

        initial_states_str = "{" + ",".join(sorted(initial_states)) + "}"


        return FiniteAutomaton(initial_states_str, final_states_list, self.symbols, final_transitions_dict, final_final_states)
        #pass

    def to_minimized(self):
        if not is_deterministic(self):
            print("ERROR: ha de tratarse de un automata determinista")
            return None
        # hacer BFS de los estados del automata desde el inicial
        q = Queue()
        q.put(self.initial_state)
        new_states = []
        while not q.empty():
            node = q.get()
            if node in new_states:
                continue
            # Conseguir nodos "hijo" y añadimos a cola
            print("NODE: "+ str(node))
            for child in list(self.transitions[node].values()):
                q.put(child[0])
            new_states.append(node)

        # Algoritmo para minimización en sí comienza aquí
        earlier_dict = {}
        perm_dict = {}
        clase = 1
        change = 1
        #Instanciar valores de clase para la primera iteración (0 para no finales, 1 para sí)
        for state in new_states:
            if state in self.final_states:
                earlier_dict[state] = 1
            else:
                earlier_dict[state] = 0
        # loop de iteraciones hasta que no haya cambio entre la anterior y la actual
        while change == 1:
            #Iteraciones individuales del algoritmo
            temp_dict = {}
            for state in new_states:
                if state not in temp_dict:
                    if state not in perm_dict:
                        temp_dict[state] = earlier_dict[state]
                    else:
                        temp_dict[state] = perm_dict[state]
                for sub_state in new_states:
                    if state == sub_state:
                        continue
                    # Lógica para comprobar que el valor de clase de todos los hijos del estado coinciden con los hijos del subestado
                    truth_value = True
                    for symbol in list(self.transitions[state].keys()):
                        if earlier_dict[self.transitions[state][symbol][0]] != earlier_dict[self.transitions[sub_state][symbol][0]]:
                            truth_value = False
                    if sub_state not in temp_dict and earlier_dict[sub_state] == temp_dict[state] and truth_value:
                        temp_dict[sub_state] = temp_dict[state]
                    else:
                        temp_dict[sub_state],perm_dict[sub_state] = clase, clase
                        clase += 1
            if earlier_dict == temp_dict:
                change = 0
            earlier_dict = temp_dict

        final_states = self.final_states
        transitions = self.transitions
        for keys in earlier_dict.keys():
            for sub_keys in earlier_dict.keys():
                if keys == sub_keys:
                    continue
                elif earlier_dict[keys] == earlier_dict[sub_keys]:
                    if sub_keys in final_states:
                        final_states.pop(sub_keys)
                        final_states.append(keys)
                    if sub_keys in transitions:
                        transitions.pop(sub_keys)
                    earlier_dict.pop(sub_keys)
        #Asignar valores correctos a los parámetros usados para crear el Autómata minimizado
        initial_state = self.initial_state
        states = list(earlier_dict.keys())
        symbols = self.symbols

        return FiniteAutomaton(initial_state, states, symbols, transitions, final_states)
        pass

    def draw(self, path="./images/", filename="automata.png", view=False):
        dot = Digraph(comment="Automata", format="png")
        dot.attr(rankdir="LR")

        # Nodo invisible para punto inicial
        dot.node("", shape="none")

        # Almacenar estados
        for state in self.states:
            if state in self.final_states:
                dot.node(state, shape="doublecircle")
            else:
                dot.node(state, shape="circle")

        # Flecha al estado inicial
        dot.edge("", self.initial_state)

        # Almacenar transiciones
        for state_ini in self.transitions:
            for symbol in self.transitions[state_ini]:
                for state_fin in self.transitions[state_ini][symbol]:
                    dot.edge(state_ini, state_fin,
                             symbol if symbol is not None else "λ")

        dot.render(path+filename, view=view)

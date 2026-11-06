"""
    Equipo docente de Autómatas y Lenguajes Curso 2025-26
    Última modificación: 18 de septiembre de 2025
"""

from automaton import FiniteAutomaton

def _re_to_rpn(re_string):
    """
    Convert re to reverse polish notation (RPN).

    Does not check that the input re is syntactically correct.

    Args:
        re_string: Regular expression in infix notation. Type: str

    Returns:
        Regular expression in reverse polish notation. Type: str

    """
    stack = [] # List of strings
    rpn_string = ""
    for x in re_string:
        if x == "+":
            while len(stack) > 0 and stack[-1] != "(":
                rpn_string += stack.pop()
            stack.append(x)
        elif x == ".":
            while len(stack) > 0 and stack[-1] == ".":
                rpn_string += stack.pop()
            stack.append(x)
        elif x == "(":
            stack.append(x)
        elif x == ")":
            while stack[-1] != "(":
                rpn_string += stack.pop()
            stack.pop()
        else:
            rpn_string += x

    while len(stack) > 0:
        rpn_string += stack.pop()

    return rpn_string



class REParser():
    """Class for processing regular expressions in Kleene's syntax."""
    
    def __init__(self) -> None:
        self.state_counter = 0

    def _create_automaton_empty(self):
        """
        Create an automaton that accepts the empty language.

        Returns:
            Automaton that accepts the empty language. Type: FiniteAutomaton

        """
        #---------------------------------------------------------------------
        # TO DO: Implement this method...
        #raise NotImplementedError("This method must be implemented.")        
        #---------------------------------------------------------------------

        emptyState = f"{self.state_counter}" # None  ""
        self.state_counter += 1
        return FiniteAutomaton(emptyState, states=[emptyState], symbols=(), transitions={}, final_states=[])


        

    def _create_automaton_lambda(self):
        """
        Create an automaton that accepts the empty string.

        Returns:
            Automaton that accepts the empty string. Type: FiniteAutomaton

        """
        #---------------------------------------------------------------------
        # TO DO: Implement this method...
        #raise NotImplementedError("This method must be implemented.")        
        #---------------------------------------------------------------------

        #lambdaState = ""
        lambdaState = f"{self.state_counter}" 
        self.state_counter += 1
        return FiniteAutomaton(lambdaState, states=[lambdaState], symbols=(), transitions={}, final_states=[lambdaState])



    def _create_automaton_symbol(self, symbol):
        """
        Create an automaton that accepts one symbol.

        Args:
            symbol: Symbol that the automaton should accept. Type: str

        Returns:
            Automaton that accepts a symbol. Type: FiniteAutomaton

        """
        #---------------------------------------------------------------------
        # TO DO: Implement this method...
        #raise NotImplementedError("This method must be implemented.")        
        #---------------------------------------------------------------------

        symbolState = f"{self.state_counter}" # Como necesitamos dos simbolos, usamos este valor para asegurarnos de que sean distintos
        self.state_counter+=1
        symbolState2 = f"{self.state_counter}"
        self.state_counter += 1

        return FiniteAutomaton(symbolState, states=[symbolState, symbolState2], symbols=(symbol,), 
                               transitions={symbolState: {symbol: [symbolState2]}}, final_states=[symbolState2])



    def _create_automaton_star(self, automaton):
        """
        Create an automaton that accepts the Kleene star of another.

        Args:
            automaton: Automaton whose Kleene star must be computed. Type: FiniteAutomaton

        Returns:
            Automaton that accepts the Kleene star. Type: FiniteAutomaton

        """
        #---------------------------------------------------------------------
        # TO DO: Implement this method...
        # raise NotImplementedError("This method must be implemented.")  
        #---------------------------------------------------------------------

        new_initial = str(self.state_counter)
        self.state_counter += 1

        # Para una estrella, solo hace falta que el ultimo nodo vuelva al inicial si se repite el simbolo
        #automat = automaton.copy()
        # COPIAR VALORES

        # obtener nuevos estados para los viejos para que no choquen
        created_states = {}
        for i, s in enumerate(automaton.states):
            created_states[s] = str(self.state_counter + i)

        self.state_counter += len(automaton.states)
        new_states = [new_initial] + list(created_states.values())
        new_symbols = automaton.symbols

        # El nuevo inicio es fina. Los finales viejos también se mantienen.
        new_final_states = [new_initial] + [created_states[f] for f in automaton.final_states]
        new_transitions = {}
        
         # Copiar transiciones originales 
        for state, trans in automaton.transitions.items():
            new_state = created_states[state]
            new_transitions[new_state] = {}
            for symbol, dests in trans.items():
                new_transitions[new_state][symbol] = [created_states[dest] for dest in dests]



        # For every final state: conectar final con viejo/inicial?
        #FiniteAutomaton.add_transition(automat, automaton.final_states, automaton.symbols[0], automaton.initial_state)

        # nuevo inicial al viejo inicial
        new_transitions[new_initial] = {
            None: [created_states[automaton.initial_state]]
        }

        # cada viejo final al viejo inicial 
        for f in automaton.final_states:
            new_f = created_states[f]
            if new_f not in new_transitions:
                new_transitions[new_f] = {}
            if None not in new_transitions[new_f]:
                new_transitions[new_f][None] = []
            new_transitions[new_f][None].append(created_states[automaton.initial_state])

        


        return FiniteAutomaton(new_initial, new_states, new_symbols, new_transitions, new_final_states)


    def _create_automaton_union(self, automaton1, automaton2):
        """
        Create an automaton that accepts the union of two automata.

        Args:
            automaton1: First automaton of the union. Type: FiniteAutomaton.
            automaton2: Second automaton of the union. Type: FiniteAutomaton.

        Returns:
            Automaton that accepts the union. Type: FiniteAutomaton.

        """
        #---------------------------------------------------------------------
        # TO DO: Implement this method...
        # raise NotImplementedError("This method must be implemented.")  
        #---------------------------------------------------------------------

        new_initial = str(self.state_counter)
        self.state_counter += 1


        # producto cartesiano de los estados
        #new_states = [(x, y) for x in automaton1.states for y in automaton2.states]
        map_aut1 = {}
        for i, s in enumerate(automaton1.states):
            map_aut1[s] = str(self.state_counter + i)
        map_aut2 = {}
        for i, s in enumerate(automaton2.states):
            map_aut2[s] = str(self.state_counter + i)

        new_states = [new_initial] + list(map_aut1.values()) + list(map_aut2.values())

        #new_symbols = automaton1.symbols | automaton2.symbols
        new_symbols = tuple(set(automaton1.symbols) | set(automaton2.symbols)) 


        #new_final_states = [map1[f] for f in automaton1.final_states] + [map2[f] for f in automaton2.final_states]
        new_final_states = set()
        for (p, q) in new_states:
            if p in automaton1.final_states or q in automaton2.final_states:
                new_final_states.add((p, q))

        
        new_initial_states = (automaton1.initial_state, automaton2.initial_state)

        new_transitions = {}
        for (p, q) in new_states:
            for simbol in new_symbols:
                au1_next = automaton1.transitions.get(p, {}).get(simbol, [])
                au2_next = automaton2.transitions.get(q, {}).get(simbol, [])
                
                # Solo creamos la transicion si ambos estados destino existen
                if au1_next is not None and au2_next is not None:
                    new_transitions[((p, q), simbol)] = (au1_next, au2_next)



        return FiniteAutomaton(new_initial_states, states=new_states, symbols=new_symbols, 
                        transitions=new_transitions, final_states=new_final_states)



    def _create_automaton_concat(self, automaton1, automaton2):
        """
        Create an automaton that accepts the concatenation of two automata.

        Args:
            automaton1: First automaton of the concatenation. Type: FiniteAutomaton.
            automaton2: Second automaton of the concatenation. Type: FiniteAutomaton.

        Returns:
            Automaton that accepts the concatenation. Type: FiniteAutomaton.

        """
        #---------------------------------------------------------------------
        # TO DO: Implement this method...
        raise NotImplementedError("This method must be implemented.")     
        #---------------------------------------------------------------------


    def create_automaton(
        self,
        re_string,
    ):
        """
        Create an automaton from a regex.

        Args:
            re_string: String with the regular expression in Kleene notation. Type: str

        Returns:
            Automaton equivalent to the regex. Type: FiniteAutomaton

        """
        if not re_string:
            return self._create_automaton_empty()
        
        rpn_string = _re_to_rpn(re_string)

        stack = [] # list of FiniteAutomatons

        self.state_counter = 0
        for x in rpn_string:
            if x == "*":
                aut = stack.pop()
                stack.append(self._create_automaton_star(aut))
            elif x == "+":
                aut2 = stack.pop()
                aut1 = stack.pop()
                stack.append(self._create_automaton_union(aut1, aut2))
            elif x == ".":
                aut2 = stack.pop()
                aut1 = stack.pop()
                stack.append(self._create_automaton_concat(aut1, aut2))
            elif x == "λ":
                stack.append(self._create_automaton_lambda())
            else:
                stack.append(self._create_automaton_symbol(x))

        return stack.pop()

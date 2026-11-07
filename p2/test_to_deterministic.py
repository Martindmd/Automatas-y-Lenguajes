"""Test evaluation of automatas."""
import unittest
from abc import ABC

from automaton import FiniteAutomaton
from utils import AutomataFormat, deterministic_automata_isomorphism


class TestTransform(ABC, unittest.TestCase):
    """Base class for string acceptance tests."""

    def _check_transform(self, automaton, expected):
        """Test that the transformed automaton is as the expected one."""

        automaton.draw(filename="automaton", view=False)

        transformed = automaton.to_deterministic()

        transformed.draw(filename="transformed", view=False)
        expected.draw(filename="expected", view=False)

        equiv_map = deterministic_automata_isomorphism(expected, transformed)

        self.assertTrue(equiv_map is not None)

    def test_case1(self):
        """Test Case 1."""
        automaton_str = """
        Automaton:
        Symbols: 01
        
        q0
        qf final
        
        ini q0 -0-> qf
        qf -1-> qf
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
        Symbols: 01
        
        q0
        qf final
        empty
        
        ini q0 -0-> qf
        q0 -1-> empty
        qf -0-> empty
        qf -1-> qf
        empty -0-> empty
        empty -1-> empty
        
        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

    # Dos Tests adicionales  para el Ejercicio 2

    def test_case2(self):
            """Test Case 2."""
            automaton_str = """
            Automaton:
            Symbols: 01
            
            q0
            q1
            qf final
            
            ini q0 -0-> qf
            ini q0 -1-> q1
            q1 -1-> qf
            q1 -1-> q0
            q1 -0-> qf
            qf -1-> qf
            """
    
            automaton = AutomataFormat.read(automaton_str)
    
            expected_str = """
            Automaton:
            Symbols: 01
            
            q0
            q1
            qf final
            empty
            q0_qf final
            q1_qf final
            
            ini q0 -0-> qf
            q0 -1-> q1
            qf -0-> empty
            qf -1-> qf
            q1 -0-> qf
            q1 -1-> q0_qf
            empty -0-> empty
            empty -1-> empty
            q0_qf -0-> qf
            q0_qf -1-> q1_qf
            q1_qf -0-> qf
            q1_qf -1-> q0_qf
            """
    
            expected = AutomataFormat.read(expected_str)
    
            self._check_transform(automaton, expected)

    
    



if __name__ == '__main__':
    unittest.main()

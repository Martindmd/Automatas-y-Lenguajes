"""Test evaluation of automatas."""
import unittest
from abc import ABC, abstractmethod
from typing import Optional, Type

from automaton import FiniteAutomaton
from utils import AutomataFormat


class TestEvaluatorBase(ABC, unittest.TestCase):
    """Base class for string acceptance tests."""

    @abstractmethod
    def _create_automata(self):
        pass

    def setUp(self):
        """Set up the tests."""
        self.automaton = self._create_automata()

    def _check_accept_body(self, string, should_accept = True):
        accepted = self.automaton.accepts(string)
        self.assertEqual(accepted, should_accept)

    def _check_accept(self, string, should_accept = True, exception = None):

        with self.subTest(string=string):
            if exception is None:
                self._check_accept_body(string, should_accept)
            else:
                with self.assertRaises(exception):
                    self._check_accept_body(string, should_accept)


class TestEvaluatorFixed(TestEvaluatorBase):
    """Test for a fixed string."""

    def _create_automata(self):

        description = """
        Automaton:
            Symbols: Helo

            Empty
            H
            He
            Hel
            Hell
            Hello final

            ini Empty -H-> H
            H -e-> He
            He -l-> Hel
            Hel -l-> Hell
            Hell -o-> Hello
        """

        return AutomataFormat.read(description)

    def test_fixed(self):
        """Test for a fixed string."""
        self._check_accept("Hello", should_accept=True)
        self._check_accept("Helloo", should_accept=False)
        self._check_accept("Hell", should_accept=False)
        self._check_accept("llH", should_accept=False)
        self._check_accept("", should_accept=False)
        self._check_accept("Hella", should_accept=False)
        self._check_accept("aHello", should_accept=False)
        self._check_accept("Helloa", should_accept=False)


class TestEvaluatorLambdas(TestEvaluatorBase):
    """Test for a fixed string."""

    def _create_automata(self):

        description = """
        Automaton:
            Symbols: 

            1
            2
            3
            4 final

            ini 1 --> 2
            2 --> 3
            3 --> 4
        """

        return AutomataFormat.read(description)

    def test_lambda(self):
        """Test for a fixed string."""
        self._check_accept("", should_accept=True)
        self._check_accept("a", should_accept=False)


class TestEvaluatorNumber(TestEvaluatorBase):
    """Test for a fixed string."""

    def _create_automata(self):

        description = """
        Automaton:
            Symbols: 01.-

            initial
            sign
            int final
            dot
            decimal final

            ini initial ---> sign
            initial --> sign
            sign -0-> int
            sign -1-> int
            int -0-> int
            int -1-> int
            int -.-> dot
            dot -0-> decimal
            dot -1-> decimal
            decimal -0-> decimal
            decimal -1-> decimal
        """

        return AutomataFormat.read(description)

    def test_number(self) -> None:
        """Test for a fixed string."""
        self._check_accept("0", should_accept=True)
        self._check_accept("0.0", should_accept=True)
        self._check_accept("0.1", should_accept=True)
        self._check_accept("1.0", should_accept=True)
        self._check_accept("-0", should_accept=True)
        self._check_accept("-0.0", should_accept=True)
        self._check_accept("-0.1", should_accept=True)
        self._check_accept("-1.0", should_accept=True)
        self._check_accept("-101.010", should_accept=True)
        self._check_accept("0.", should_accept=False)
        self._check_accept(".0", should_accept=False)
        self._check_accept("0.0.0", should_accept=False)
        self._check_accept("0-0.0", should_accept=False)


    # Dos Tests adicionales  para el Ejercicio 1

    
class TestEvaluatorFixedAditional(TestEvaluatorBase):
    """Test for a fixed string. EXTRA"""

    def _create_automata(self):

        description = """
        Automaton:
            Symbols: World

            Empty
            W
            Wo
            Wor
            Worl
            World final

            ini Empty -W-> W
            W -o-> Wo
            Wo -r-> Wor
            Wor -l-> Worl
            Worl -d-> World
        """

        return AutomataFormat.read(description)

    def test_fixed(self):
        """Test for a fixed string."""
        self._check_accept("World", should_accept=True)
        self._check_accept("Woorld", should_accept=False)
        self._check_accept("Wrld", should_accept=False)
        self._check_accept("Wor", should_accept=False)
        self._check_accept("rld", should_accept=False)
        self._check_accept("", should_accept=False)


class TestEvaluatorNumberAditional(TestEvaluatorBase):
    """Test for a fixed string NOW with a symbol a to repressent letters only at the end."""

    def _create_automata(self):
        description = """
        Automaton:
            Symbols: 01.-a

            initial
            sign
            int final
            dot
            decimal final
            letter final

            ini initial ---> sign
            initial --> sign
            sign -0-> int
            sign -1-> int
            int -0-> int
            int -1-> int
            int -a-> letter
            int -.-> dot
            dot -0-> decimal
            dot -1-> decimal
            decimal -0-> decimal
            decimal -1-> decimal
            decimal -a-> letter
        """
        return AutomataFormat.read(description)

    def test_number_with_letter(self):
        self._check_accept("0", should_accept=True)
        self._check_accept("-1.0", should_accept=True)
        self._check_accept("0a", should_accept=True)
        self._check_accept("-1a", should_accept=True)
        self._check_accept("-101.010a", should_accept=True)
        self._check_accept("a", should_accept=False)
        self._check_accept("a0", should_accept=False)
        self._check_accept("0aa", should_accept=False)
        self._check_accept("0.a", should_accept=False)
        self._check_accept("0.a1", should_accept=False)
        self._check_accept("-a", should_accept=False)


if __name__ == '__main__':
    unittest.main()

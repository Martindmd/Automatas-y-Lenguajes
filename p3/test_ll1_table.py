"""Ejercicio 4: comprobaciones de tabla independientes de analyze."""
import unittest
from src.utils import GrammarFormat


class TestLL1Table(unittest.TestCase):
    def test_cells_and_empty_production(self):
        grammar = GrammarFormat.read('S -> aS\nS ->')
        table = grammar.get_ll1_table()
        self.assertIsNotNone(table)
        self.assertEqual(table.cells, {'S': {'a': 'aS', '$': ''}})

    def test_missing_cell_is_none(self):
        grammar = GrammarFormat.read('S -> aA\nA -> b')
        table = grammar.get_ll1_table()
        self.assertIsNotNone(table)
        self.assertEqual(table.cells['S']['a'], 'aA')
        self.assertIsNone(table.cells['S']['b'])
        self.assertIsNone(table.cells['S']['$'])
        self.assertEqual(table.cells['A']['b'], 'b')

    def test_first_first_conflict(self):
        grammar = GrammarFormat.read('S -> aA\nS -> aB\nA -> b\nB -> c')
        self.assertIsNone(grammar.get_ll1_table())

    def test_first_follow_conflict(self):
        grammar = GrammarFormat.read('S -> Aa\nA -> a\nA ->')
        self.assertIsNone(grammar.get_ll1_table())


if __name__ == '__main__':
    unittest.main()

"""Casos límite y convenciones del enunciado, ejercicios 1–3."""
import unittest
from src.grammar import Grammar, LL1Table, ParseTree, SyntaxError
from src.utils import GrammarFormat


class TestAnalyzeContract(unittest.TestCase):
    def setUp(self):
        self.table = LL1Table({'S'}, {'a', '$'})
        self.table.add_cell('S', 'a', 'aS')
        self.table.add_cell('S', '$', '')

    def test_empty_word_tree(self):
        self.assertEqual(self.table.analyze('$', 'S'), ParseTree('S', [ParseTree('')]))

    def test_nonempty_tree(self):
        expected = ParseTree('S', [ParseTree('a'), ParseTree('S', [ParseTree('')])])
        self.assertEqual(self.table.analyze('a$', 'S'), expected)

    def test_end_marker_and_unknown_symbols(self):
        for word in ['', 'a', '$$', 'a$$', '$a', 'a$a', '?$']:
            with self.subTest(word=word), self.assertRaises(SyntaxError):
                self.table.analyze(word, 'S')

    def test_invalid_start(self):
        with self.assertRaises(ValueError):
            self.table.analyze('a$', 'X')


class TestFirstFollowContract(unittest.TestCase):
    def test_first_checks_entire_argument(self):
        grammar = Grammar({'a'}, {'S'}, {'S': ['a']}, 'S')
        for word in ['?', 'a?', 'S?', '$']:
            with self.subTest(word=word), self.assertRaises(ValueError):
                grammar.compute_first(word)
        self.assertEqual(grammar.compute_first(''), {''})

    def test_nullable_chain(self):
        grammar = GrammarFormat.read('S -> AB\nA -> a\nA ->\nB -> b\nB ->')
        self.assertEqual(grammar.compute_first('S'), {'a', 'b', ''})
        self.assertEqual(grammar.compute_follow('A'), {'b', '$'})
        self.assertEqual(grammar.compute_follow('B'), {'$'})

    def test_repeated_nonterminal(self):
        grammar = GrammarFormat.read('S -> AaA\nA -> b\nA ->')
        self.assertEqual(grammar.compute_follow('A'), {'a', '$'})

    def test_cycle(self):
        grammar = GrammarFormat.read('S -> A\nA -> B\nB -> A\nB -> b')
        for symbol in ['S', 'A', 'B']:
            with self.subTest(symbol=symbol):
                self.assertEqual(grammar.compute_first(symbol), {'b'})
                self.assertEqual(grammar.compute_follow(symbol), {'$'})

    def test_invalid_follow_argument(self):
        grammar = GrammarFormat.read('S -> a')
        for symbol in ['a', '', 'SS', '?']:
            with self.subTest(symbol=symbol), self.assertRaises(ValueError):
                grammar.compute_follow(symbol)


if __name__ == '__main__':
    unittest.main()

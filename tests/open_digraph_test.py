""" from modules.open_digraph import *
import unittest
import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)


class NodeTest(unittest.TestCase):
    def setUp(self):
        self.n0 = node(0, 'i', {}, {1: 1})

    def test_get_id(self):
        self.assertEqual(self.n0.get_id(), 0)

    def test_get_label(self):
        self.assertEqual(self.n0.get_label(), 'a')

    def test_init_node(self):
        self.assertEqual(self.n0.id, 0)
        self.assertEqual(self.n0.label, 'i')
        self.assertEqual(self.n0.parents, {})
        self.assertEqual(self.n0.children, {1: 1})
        self.assertIsInstance(self.n0, node)


class OpenDigraphTest(unittest.TestCase):
    def setUp(self):
        self.n0 = node(0, 'a', {3: 1, 4: 1}, {1: 1, 2: 1})
        self.n1 = node(1, 'b', {0: 1}, {2: 2, 5: 1})
        self.n2 = node(2, 'c', {0: 1, 1: 2}, {6: 1})
        self.i0 = node(3, 'i0', {}, {0: 1})
        self.i1 = node(4, 'i1', {}, {0: 1})
        self.o0 = node(5, 'o0', {1: 1}, {})
        self.o1 = node(6, 'o1', {2: 1}, {})
        self.d0 = open_digraph(
            [3, 4], [5, 6], [self.n0, self.n1, self.n2, self.i0, self.i1, self.o0, self.o1])

    def test_get_id(self):
        self.assertEqual(self.n0.get_id(), 0)

    def test_get_label(self):
        self.assertEqual(self.n0.get_label(), 'a')

    def test_init_open_digraph(self):
        self.assertEqual(self.d0.inputs, [3, 4])
        self.assertEqual(self.d0.outputs, [5, 6])
        self.assertEqual(
            self.d0.nodes, {0: self.n0, 1: self.n1, 2: self.n2, 3: self.i0, 4: self.i1, 5: self.o0, 6: self.o1})

    def test_copy(self):
        self.assertIsNot(self.d0.copy(), self.d0)


if __name__ == '__main__':  # the following code is called only when
    unittest.main()  # precisely this file is run """

import unittest
from modules.open_digraph import *
import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)  # allows us to fetch files from the project root


class InitTest(unittest.TestCase):
    def test_init_node(self):
        n0 = node(0, 'i', {}, {1: 1})
        self.assertEqual(n0.identif, 0)
        self.assertEqual(n0.label, 'i')
        self.assertEqual(n0.parents, {})
        self.assertEqual(n0.children, {1: 1})
        self.assertIsInstance(n0, node)

    def test_init_open_digraph(self):
        n0 = node(0, 'i', {}, {1: 1})
        u = open_digraph([0], [0], [n0])
        self.assertEqual(u.inputs, [0])
        self.assertEqual(u.outputs, [0])
        self.assertEqual(u.nodes, {0: n0})


class NodeTest(unittest.TestCase):
    def setUp(self):
        self.n0 = node(0, 'a', [], [1])

    def test_get_id(self):
        self.assertEqual(self.n0.identif, 0)

    def test_get_label(self):
        self.assertEqual(self.n0.label, 'a')

    def test_cpy(self):
        self.assertIsNot(self.n0.copy(), self.n0)


class OpenDigraphTest(unittest.TestCase):
    def setUp(self):
        self.n0 = node(0, 'a', {3: 1, 4: 1}, {1: 1, 2: 1, 7: 1})
        self.n1 = node(1, 'b', {0: 1}, {2: 2, 5: 1})
        self.n2 = node(2, 'c', {0: 1, 1: 2}, {6: 1})
        self.i0 = node(3, 'i0', {}, {0: 1})
        self.i1 = node(4, 'i1', {}, {0: 1})
        self.o0 = node(5, 'o0', {1: 1}, {})
        self.o1 = node(6, 'o1', {2: 1}, {})
        self.useless = node(7, 'u', {0: 1}, {})
        self.G = open_digraph([3, 4], [5, 6], [
                              self.n0, self.n1, self.n2, self.i0, self.i1, self.o0, self.o1, self.useless])
        self.T = open_digraph(
            [0, 1], [3, 4], [self.n0, self.n1, self.n2, self.i0, self.i1, self.o0, self.o1])
        self.G.remove_node_by_id(7)
        self.G.add_node()
        self.AT = self.G.copy()
        # self.AT.remove_node_by_id(0)

    def test_is_well_formed(self):
        self.assertTrue(self.G.is_well_formed())
        self.assertFalse(self.T.is_well_formed())
        self.assertTrue(self.AT.is_well_formed())

    def test_cpy(self):
        self.assertIsNot(self.G.copy(), self.G)


if __name__ == '__main__':
    unittest.main()

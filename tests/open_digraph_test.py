from modules.open_digraph import *
import unittest
import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)  # allows us to fetch files from the project root


class InitTest(unittest.TestCase):
    def test_init_node(self):
        n0 = node(0, 'i', {}, {1: 1})
        self.assertEqual(n0.get_id(), 0)
        self.assertEqual(n0.get_label(), 'i')
        self.assertEqual(n0.get_parents(), {})
        self.assertEqual(n0.get_children(), {1: 1})
        self.assertIsInstance(n0, node)

    def test_init_open_digraph(self):
        n0 = node(0, 'i', {}, {1: 1})
        u = open_digraph([0], [0], [n0])
        self.assertEqual(u.get_input_ids(), [0])
        self.assertEqual(u.get_outputs(), [0])
        self.assertEqual(u.get_nodes(), [n0])


class NodeTest(unittest.TestCase):
    def setUp(self):
        self.n0 = node(0, 'a', {}, {1: 1})

    def test_get_id(self):
        self.assertEqual(self.n0.get_id(), 0)

    def test_get_label(self):
        self.assertEqual(self.n0.get_label(), 'a')

    def test_cpy(self):
        self.assertIsNot(self.n0.copy(), self.n0)


class OpenDigraphTest(unittest.TestCase):
    def setUp(self):
        self.n0 = node(0, 'a', {3: 1, 4: 1}, {1: 1, 2: 1})
        self.n1 = node(1, 'b', {0: 1}, {2: 2, 5: 1})
        self.n2 = node(2, 'c', {0: 1, 1: 2}, {6: 1})
        self.i0 = node(3, 'i0', {}, {0: 1})
        self.i1 = node(4, 'i1', {}, {0: 1})
        self.o0 = node(5, 'o0', {1: 1}, {})
        self.o1 = node(6, 'o1', {2: 1}, {})
        self.useless = node(7, 'u', {2: 1}, {})
        self.G = open_digraph(
            [3, 4], [5, 6], [self.n0, self.n1, self.n2, self.i0, self.i1, self.o0, self.o1])
        self.T = open_digraph(
            [0, 1], [3, 4], [self.n0, self.n1, self.n2, self.i0, self.i1, self.o0, self.o1])

    def test_is_well_formed(self):
        self.assertTrue(self.G.is_well_formed())
        self.assertFalse(self.T.is_well_formed())

    def test_cpy(self):
        self.assertIsNot(self.G.copy(), self.G)

    def test_add_node(self):
        newId: int = self.G.add_node("d", {1: 1}, {2: 1})
        newNode: node = self.G.get_node_by_id(newId)
        self.assertTrue(newId in self.G.get_node_ids())
        self.assertTrue(newNode.get_children() == {2: 1})
        self.assertTrue(newNode.get_parents() == {1: 1})
        self.assertTrue(newId in self.G.get_node_by_id(1).get_children_ids())
        self.assertTrue(newId in self.G.get_node_by_id(2).get_parents_ids())

    def test_remove_node(self):
        self.G.remove_node_by_id(3)
        self.assertFalse(3 in self.G.get_node_ids())
        self.assertFalse(3 in self.G.get_node_by_id(0).get_parents_ids())

    def test_add_input(self):
        newId: int = self.G.add_input_node(3)
        self.assertTrue(newId in self.G.get_node_by_id(3).get_parents_ids())
        self.assertFalse(3 in self.G.get_input_ids())
        self.assertTrue(self.G.get_node_by_id(newId).get_children() == {3: 1})
        self.assertTrue(newId in self.G.get_input_ids())

    def test_add_output(self):
        newId: int = self.G.add_output_node(5)
        self.assertTrue(newId in self.G.get_node_by_id(5).get_children_ids())
        self.assertFalse(5 in self.G.get_output_ids())
        self.assertTrue(self.G.get_node_by_id(newId).get_parents() == {5: 1})
        self.assertTrue(newId in self.G.get_output_ids())


if __name__ == '__main__':
    unittest.main()

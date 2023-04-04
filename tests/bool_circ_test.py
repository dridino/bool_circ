from modules.open_digraph import open_digraph
from modules.node import node
from modules.bool_circ import bool_circ
import unittest
import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)  # allows us to fetch files from the project root


""" class InitTest(unittest.TestCase):
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
        self.assertEqual(u.get_output_ids(), [0])
        self.assertEqual(u.get_nodes(), [n0]) """


""" class NodeTest(unittest.TestCase):
    def setUp(self):
        self.n0 = node(0, 'a', {}, {1: 1})

    def test_get_id(self):
        self.assertEqual(self.n0.get_id(), 0)

    def test_get_label(self):
        self.assertEqual(self.n0.get_label(), 'a')

    def test_cpy(self):
        self.assertIsNot(self.n0.copy(), self.n0) """


class BoolCircTest(unittest.TestCase):
    def setUp(self):
        return None
        """ self.n0 = node(0, 'a', {3: 1, 4: 1}, {1: 1, 2: 1})
        self.n1 = node(1, 'b', {0: 1}, {2: 2, 5: 1})
        self.n2 = node(2, 'c', {0: 1, 1: 2}, {6: 1})
        self.i0 = node(3, 'i0', {}, {0: 1})
        self.i1 = node(4, 'i1', {}, {0: 1})
        self.o0 = node(5, 'o0', {1: 1}, {})
        self.o1 = node(6, 'o1', {2: 1}, {})
        self.useless = node(7, 'u', {2: 1}, {})
        node_l = [self.n0, self.n1, self.n2,
                  self.i0, self.i1, self.o0, self.o1]
        # Correct exemple graph G
        self.G = open_digraph(
            [3, 4], [5, 6], node_l)
        # Graphs for is_well_formed tests
        self.T1 = open_digraph(
            [0, 1], [3, 4], [n.copy() for n in node_l])
        self.T2 = open_digraph(
            [0], [1], [node(0, 'i0', {}, {2: 1}), node(1, 'o0', {2: 1}, {}), node(2, 'a', {0: 1}, {1: 1})])
        self.T3 = open_digraph(
            [0], [1], [node(0, 'i0', {}, {1: 1}), node(1, 'o0', {0: 1}, {})])
        self.GTD7 = open_digraph([0, 2], [7], [
            node(0, "0", {}, {3: 1}),
            node(1, "1", {}, {5: 1, 8: 1, 4: 1}),
            node(2, "2", {}, {4: 1}),
            node(3, "3", {0: 1}, {7: 1, 6: 1}),
            node(4, "4", {1: 1, 2: 1}, {6: 1}),
            node(5, "5", {3: 1, 1: 1}, {7: 1}),
            node(6, "6", {3: 1, 4: 1}, {8: 1, 9: 1}),
            node(7, "7", {3: 1, 5: 1}, {}),
            node(8, "8", {1: 1, 6: 1}, {}),
            node(9, "9", {6: 1}, {}),
        ])

        self.T4 = open_digraph(
            [0], [1], [node(0, 'i0', {}, {2: 1}), node(1, 'o0', {2: 1}, {3: 1}), node(2, 'a', {0: 1}, {1: 1}), node(3, 'o1', {1: 1}, {})])
        self.T5 = open_digraph(
            [0], [1], [node(0, 'i0', {}, {2: 2}), node(1, 'o0', {2: 1}, {}), node(2, 'a', {0: 2}, {1: 1})])
        self.T6 = open_digraph(
            [0], [1], [node(0, 'i0', {}, {2: 1}), node(1, 'o0', {2: 2}, {}), node(2, 'a', {0: 1}, {1: 2})])
        self.T7 = open_digraph(
            [0, 2], [1], [node(0, 'i0', {}, {2: 1}), node(1, 'o0', {2: 1}, {}), node(2, 'a', {0: 1}, {1: 1})])
        self.T8 = open_digraph(
            [0], [1, 2], [node(0, 'i0', {}, {2: 1}), node(1, 'o0', {2: 1}, {}), node(2, 'a', {0: 1}, {1: 1})])
        self.T9 = open_digraph(
            [0], [1], [node(0, 'i0', {}, {2: 1}), node(1, 'o0', {2: 1}, {}), node(2, 'a', {0: 1}, {1: 1})])
        self.T9.get_node_by_id(2).set_id(3)
        self.T10 = open_digraph(
            [0], [1], [node(0, 'i0', {}, {2: 1}), node(1, 'o0', {3: 1}, {}), node(2, 'a', {0: 1}, {3: 2}), node(3, 'b', {2: 1}, {1: 1})])
        self.T11 = open_digraph(
            [0], [1], [node(0, 'i0', {}, {2: 1}), node(1, 'o0', {3: 1}, {}), node(2, 'a', {0: 1}, {3: 1}), node(3, 'b', {2: 2}, {1: 1})])
        self.T12 = open_digraph(
            [0], [1], [node(0, 'i0', {}, {2: 1}), node(1, 'o0', {3: 1}, {}), node(2, 'a', {0: 1}, {}), node(3, 'b', {2: 1}, {1: 1})])
        self.T13 = open_digraph(
            [0], [1], [node(0, 'i0', {}, {2: 1}), node(1, 'o0', {3: 1}, {}), node(2, 'a', {0: 1}, {3: 1}), node(3, 'b', {}, {1: 1})]) """

    def test_from_string(self):
        tmp: tuple[bool_circ, list] = bool_circ.empty(
        ).from_string("((x0)&((x1)&(x2)))|((x1)&(~(x2)))", "((x0)&(~(x1)))|(x2)")
        print(tmp[1])
        tmp[0].display(
            verbose=True, name="bool_circ.png")

    def test_random_bool_circ(self):
        bool_circ.random_bool_circ(20, inputs=5, outputs=6).display(
            verbose=True, name="random_bool_circ.png")

    def test_adder(self):
        bool_circ.adder(1).display(verbose=True)


if __name__ == '__main__':
    unittest.main()

from modules.open_digraph import open_digraph
from modules.node import node
from random import choice


class bool_circ(open_digraph):
    def __init__(self, g: open_digraph) -> None:
        """
        Create a `bool_circ` with the corresponding parameters.

        Parameters
        ----------
        g: `open_digraph`
            The `open_digraph` we want to create a `bool_circ` from

        Return
        ----------
        A `bool_circ` created from `g`.

        Label correspondance
        ----------
        - '&' -> AND
        - '|' -> OR
        - '~' -> NOT
        - ''  -> COPY
        """
        super().__init__(g.get_input_ids(), g.get_output_ids(), g.get_nodes())
        assert self.is_well_formed(), "The graph you provided isn't a valid bool circuit."

    @classmethod
    def empty(cls):
        """
        Create an empty `bool_circ`.
        """
        return cls(open_digraph.empty())

    @classmethod
    def random_bool_circ(cls, n: int, inputs: int = 1, outputs: int = 1):
        """
        Create a random bool_circ with `n` nodes.

        Parameters
        ----------
        n : int
            The number of nodes.

        inputs : int
            The number of inputs (superior or equal to 1)

        outputs : int
            The number of outputs (superior or equal to 1)
        """
        g: open_digraph = open_digraph.random(
            n, 1, form="dag", inputs=inputs, outputs=outputs)

        tmp: list[node] = list(g.nodes.values()).copy()
        for no in tmp:
            if no.get_parents_ids() == []:
                g.add_input_node(no.get_id())
            if no.get_children_ids() == []:
                g.add_output_node(no.get_id())

        tmp: list[node] = list(g.nodes.values()).copy()
        for u in tmp:
            # deg+
            deg1: int = u.indegree()
            # deg-
            deg2: int = u.outdegree()
            if u.get_id() in g.inputs:
                u.set_label(f"i{g.inputs.index(u.get_id())}")
            elif u.get_id() in g.outputs:
                u.set_label(f"o{g.outputs.index(u.get_id())}")
            elif deg1 == 1:
                if deg2 == 1:
                    u.set_label("~")
            else:
                if deg2 == 1:
                    u.set_label(choice(["|", "&"]))
                else:
                    uop: int = g.add_node(
                        choice(["|", "&"]), u.get_parents().copy())
                    ucp: int = g.add_node(
                        "", {uop: 1}, u.get_children().copy())
                    g.remove_node_by_id(u.get_id())

        return bool_circ(g)

    def adder_builder(self, n: int) -> tuple[open_digraph, list[int], list[int], int, int, list[int]]:
        """
        Build the adder block.

        Parameters
        ----------
        n : int
            The rank of the adder

        Return
        ----------
            - `bool_circ` : the resulting adder block
            - `list[int]` : the list of node ids corresponding to the first input (a)
            - `list[int]` : the list of node ids corresponding to the second input (b)
            - `int` : the id of the carry input (c)
            - `int` : the id of the carry output (c')
            - `list[int]` : the list of node ids corresponding to the output (r)
        """
        if n == 0:
            return bool_circ(open_digraph(
                inputs=[0, 1, 2],
                outputs=[12, 13],
                nodes=[
                    node(0, "i0", {}, {3: 1}),
                    node(1, "i1", {}, {4: 1}),
                    node(2, "i2", {}, {7: 1}),
                    node(3, "", {0: 1}, {5: 1, 8: 1}),
                    node(4, "", {1: 1}, {5: 1, 8: 1}),
                    node(5, "^", {3: 1, 4: 1}, {6: 1}),
                    node(6, "", {5: 1}, {9: 1, 10: 1}),
                    node(7, "", {2: 1}, {9: 1, 10: 1}),
                    node(8, "&", {3: 1, 4: 1}, {11: 1}),
                    node(9, "&", {6: 1, 7: 1}, {11: 1}),
                    node(10, "^", {6: 1, 7: 1}, {13: 1}),
                    node(11, "|", {8: 1, 9: 1}, {12: 1}),
                    node(12, "o0", {11: 1}, {}),
                    node(13, "o1", {10: 1}, {}),
                ]
            )), [0], [1], 2, 12, [13]
        else:
            prev1, i_a1, i_b1, i_c1, o_c1, o_r1 = self.adder_builder(n-1)

            prev2 = prev1.copy()
            i_a2 = i_a1.copy()
            i_b2 = i_b1.copy()
            i_c2 = i_c1
            o_c2 = o_c1
            o_r2 = o_r1.copy()

            shift = prev1.iparallel(prev2)
            i_a1 = [e+shift for e in i_a1]
            i_b1 = [e+shift for e in i_b1]
            o_r1 = [e+shift for e in o_r1]
            i_c1 += shift
            o_c1 += shift

            child_c = prev1.get_node_by_id(i_c2).get_children_ids()[0]
            parent_c = prev1.get_node_by_id(o_c1).get_parents_ids()[0]

            prev1.remove_node_by_id(i_c2)
            prev1.remove_node_by_id(o_c1)

            prev1.add_edge(parent_c, child_c)

            return prev1, i_a1 + i_a2, i_b1 + i_b2, i_c1, o_c2, o_r1 + o_r2

    @classmethod
    def adder(cls, n: int):
        """
        Return a `bool_circ` computing the sum of two registry, with an input carry.

        Parameters
        ----------
        n : int
            The size of the registries.
        """
        assert n >= 0, "n must be positive"
        adder = cls.empty()
        adder, i_a, i_b, i_c, o_c, o_r = adder.adder_builder(n)

        for i, node_id in enumerate(i_a):
            node = adder.get_node_by_id(node_id)
            node.label = f"a{i}"

        for i, node_id in enumerate(i_b):
            node = adder.get_node_by_id(node_id)
            node.label = f"b{i}"

        for i, node_id in enumerate(o_r):
            node = adder.get_node_by_id(node_id)
            node.label = f"r{i}"

        adder.get_node_by_id(i_c).label = 'c'
        adder.get_node_by_id(o_c).label = "c'"

        return adder

    @classmethod
    def half_adder(cls, n: int):
        """
        Return a `bool_circ` computing the sum of two registry, without input carry.

        Parameters
        ----------
        n : int
            The size of the registries.
        """
        half_adder: bool_circ = cls.adder(n)

        for i_id in half_adder.inputs:
            if cls.get_node_by_id(i_id).get_label() == "c":  # type: ignore
                child = cls.get_node_by_id(i_id).get_children_ids()[  # type: ignore
                    0]
                half_adder.remove_node_by_id(i_id)
                new_id: int = half_adder.add_node(label="0")
                half_adder.add_edge(new_id, child)

    def from_string(self, *v: str):
        """
        Take n infix representations of the desired bool_circ in argument and return a bool_circ whose outputs match each string representation.

        Parameters
        ----------
        v : tuple[str, str, ...]
            The infix representations of the desired bool_circ

        Return
        ----------
        Return a bool_circ whose outputs match each string representation
        """
        if len(v) == 0:
            return self.empty(), []

        l: list[dict[str, list[int]]] = [{} for _ in range(len(v))]
        g_list: list[bool_circ] = [bool_circ(open_digraph(
            [], [1], [node(0, "0", {}, {1: 1}), node(1, "1", {0: 1}, {})])) for _ in range(len(v))]
        for i, s in (enumerate(v)):
            g: bool_circ = g_list[i]
            g.get_node_by_id(0).set_label("")
            g.get_node_by_id(1).set_label("")
            current_node: int = 0
            s2: str = ""
            for c in s:
                if c == '(':
                    g.get_node_by_id(current_node).set_label(
                        g.get_node_by_id(current_node).label + s2)
                    tmp_id: int = g.add_node(children={current_node: 1})
                    g.get_node_by_id(current_node).add_parent_id(tmp_id)
                    current_node = tmp_id
                    s2 = ""
                elif c == ')':
                    if s2 not in ["&", "|", "~", ""]:
                        if s2 not in l[i].keys():
                            l[i][s2] = [current_node]
                        else:
                            l[i][s2] += [current_node]
                    g.get_node_by_id(current_node).set_label(
                        g.get_node_by_id(current_node).label + s2)
                    current_node = g.get_node_by_id(
                        current_node).get_children_ids()[0]
                    s2 = ""
                else:
                    s2 += c

        final_graph: bool_circ = g_list[0]
        l2: dict[str, list[int]] = l[0]
        for i in range(1, len(g_list)):
            l2 = {k: [vv + (final_graph.max_id() - g_list[i].min_id() + 1)
                      for vv in va] for k, va in l2.items()}
            for k, va in l[i].items():
                if k in l2.keys():
                    l2[k] += va
                else:
                    l2[k] = va
            final_graph.iparallel(g_list[i])

        res: list[str] = []
        while len(l2) != 0:
            lab: str = list(l2.keys())[0]
            if lab not in res:
                res += [lab]
            if len(l2[lab]) == 1:
                l2.pop(lab)
            else:
                idx1: int = l2[lab].pop()
                idx2: int = l2[lab].pop()
                idx3 = final_graph.merge_nodes(idx1, idx2)
                l2[lab] += [idx3]
                if l2[lab] == []:
                    l2.pop(lab)

        return final_graph, res

    def copy(self):
        """
        Return a new instance of `bool_circ` with the same parameters.
        """
        return bool_circ(super().copy())

    def is_cyclic(self) -> bool:
        """
        Return True whether this `bool_circ` is cyclic or not.

        Return
        ----------
        Return True whether this `bool_circ` is cyclic or not.
        """
        if self.nodes == {}:
            return False
        # we select every leaf
        leaves: list[int] = [
            k for k, n in self.nodes.items() if n.get_children() == {}]
        if leaves == []:
            return True
        else:
            g: bool_circ = self.copy()
            g.remove_node_by_id(leaves[0])
            return g.is_cyclic()

    def is_well_formed(self) -> bool:
        """
        Return True whether a `bool_circ` is well formed or not.
        A `bool_circ` is well formed if :
            - Every copy node has exactly an `indegree` of 1
            - Every '&' or '|' node has exactly an `outdegree` of 1
            - Every '~' node has exactly an `indegree` and an `outdegree` of 1

        Return
        ----------
        True wether a `bool_circ` is well formed or not.
        """
        if not super().is_well_formed():
            return False
        for n in self.nodes.values():
            if n.get_label() == '' and n.indegree() != 1:
                return False
            if (n.get_label() == '&' or n.get_label() == '|') and n.outdegree() != 1:
                return False
            if n.get_label() == '~' and n.indegree() != 1 and n.outdegree() != 1:
                return False
        return True

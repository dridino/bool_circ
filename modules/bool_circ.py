from modules.open_digraph import open_digraph
from modules.node import node


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

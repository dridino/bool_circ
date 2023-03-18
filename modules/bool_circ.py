from modules.open_digraph import open_digraph


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

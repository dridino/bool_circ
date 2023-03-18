class open_digraph_compositions_mx:

    def min_id(self) -> int:
        """
        Return the minimal `id` of the nodes in this `open_digraph`. Return -1 if there's no node in this `open_digraph`.

        Return
        ----------
        Return the minimal `id` of the nodes in this `open_digraph`. Return -1 if there's no node in this `open_digraph`.        
        """
        return min(self.get_node_ids(), default=-1)

    def max_id(self) -> int:
        """
        Return the maximal `id` of the nodes in this `open_digraph`. Return -1 if there's no node in this `open_digraph`.

        Return
        ----------
        Return the maximal `id` of the nodes in this `open_digraph`. Return -1 if there's no node in this `open_digraph`.        
        """
        return max(self.get_node_ids(), default=-1)

    def shift_indices(self, n: int) -> None:
        """
        Add `n` to every node's `id` in this `open_digraph`. `n` may be negative.

        Parameters
        ----------
        n : `int`
            The integer we'll add to every indice (may be negative).
        """
        d: dict[int, node] = {}
        for no in self.nodes.values():
            no.set_id(no.get_id() + n)
            no.set_parents({k+n: v for k, v in no.get_parents().items()})
            no.set_children({k+n: v for k, v in no.get_children().items()})
            d[no.get_id()] = no
        self.nodes = d
        self.inputs = [i+n for i in self.inputs]
        self.outputs = [o+n for o in self.outputs]

    def iparallel(self, g) -> None:
        """
        Add `g` to the current graph. (modify the current graph but not `g`)

        Parameters
        ----------
        g : `open_digraph`
            The `open_digraph` we want to add to the current one.
        """
        if g.nodes == {}:
            return None
        self.shift_indices(self.max_id() - g.min_id() + 1)
        for k, v in g.nodes.items():
            self.nodes[k] = v
        self.inputs += g.inputs
        self.outputs += g.outputs

    def parallel(self, g):
        """
        Merge `g` and the current `open_digraph` and return a newly created `open_digraph`.

        Parameters
        ----------
        g : `open_digraph`
            The `open_digraph` we want to add with the current one.

        Return
        ----------
        Return a new `open_digraph` corresponding to the concatenation of both `open_digraph`s.
        """
        res = self.copy()
        res.iparallel(g)
        return res

    def icompose(self, f) -> None:
        """
        Make the sequencial composition of `self` and `f`.

        Parameters
        ----------
        f : `open_digraph`
            The `open_digraph` we want to add before `self`

        Return
        ----------
        Make the sequencial composition of `self` and `f`.
        """
        if len(self.inputs) != len(f.outputs):
            raise ValueError(
                "The specified `open_digraph` don't match with the current inputs.")

        tmp = f.copy()
        self.shift_indices(self.max_id() - tmp.min_id() + 1)

        for i, out in enumerate(f.outputs):
            tmp.nodes[out].add_child_id(self.inputs[i])

        for k, v in tmp.nodes.items():
            self.nodes[k] = v
        self.set_input_ids(tmp.inputs)

    def compose(self, f):
        """
        Make the sequencial composition of `self` and `f` without modifying any of them.

        Parameters
        ----------
        f : `open_digraph`
            The `open_digraph` we want to add before `self`

        Return
        ----------
        Return a new `open_doigraph` corresponding to the sequencial composition of `self` and `f`.
        """
        cp = self.copy()
        cp.icompose(f)
        return cp

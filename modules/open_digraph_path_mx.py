class open_digraph_path_mx:

    def mapInputToOutput(self, i: int, outputs: list[int]):
        if self.nodes[i].get_children_ids() == []:
            return i

        return [self.mapInputToOutput(c, outputs) for c in self.nodes[i].get_children_ids()]

    def aux(self, l: list[int], first: bool):
        # at first, cpt = 0
        ll: set[int] = set()
        d: list[set[int]] = []
        """for i in l:
            n: node = self.nodes[i]
            d[i] = cpt
            if n.get_children_ids() == []:
                cpt += 1
            else:
                tmp, cpt = self.aux(n.get_children_ids(), cpt)
                for k, v in tmp.items():
                    d[k] = v
        return d, cpt"""
        for i in l:
            current: node = self.nodes[i]
            ll.add(i)
            if current.get_children_ids() != []:
                for elem in self.aux(current.get_children_ids(), False)[0]:
                    ll.add(elem)
            if first:
                d += [set(ll)]
                ll = set()
        return ll, d

    def connected_components(self) -> tuple[int, dict[int, int]]:
        """
        Return the number of connected components and a `dict` which associate at each
        node id in the graph an int corresponding to which "subgraph" it belongs to.

        Return
        ----------
        Return the number of connected components and a `dict` which associate at each
        node id in the graph an int corresponding to which "subgraph" it belongs to.
        """
        d: dict[int, int] = {}
        cpt: int = 0
        # à chaque input on associe les outputs possible
        res: list[set[int]] = self.aux(self.inputs, True)[1]
        for e in res[0]:
            d[e] = cpt
        for e in res[1:]:
            if len(e.intersection(d.keys())) != 0:
                for e2 in e:
                    d[e2] = cpt
            else:
                cpt += 1
                for e2 in e:
                    d[e2] = cpt
        return cpt+1, d

    def components_list(self) -> list:
        """
        Return a `list` containing every independants `open_digraph` this graph is made of.

        Return
        ----------
        Return a `list` containing every independants `open_digraph` this graph is made of.
        """
        res: tuple[int, dict[int, int]] = self.connected_components()
        splitted: list[set[int]] = [
            set([n_id for n_id, v in res[1].items() if v == i]) for i in range(res[0])]
        l: list[self.__class__] = [self.__class__.empty()
                                   for _ in range(res[0])]
        for i in range(res[0]):
            l[i].nodes = {k: v for k, v in self.nodes.items()
                          if k in splitted[i]}
            l[i].inputs = [j for j in self.inputs if j in splitted[i]]
            l[i].outputs = [o for o in self.outputs if o in splitted[i]]
        return l

    def dijkstra(self, src: int, direction: int | None = None, tgt: int | None = None) -> tuple[dict[int, int], dict[int, int]]:
        """
        Dijkstra algorithm applied to our class.

        Parameters
        ----------
        src : int
            The source node
        direction : int | None
            The direction we want to explore :
                - None : We explore both the parents and the children
                - -1 : We only explore the parents
                - 1 : We only explore the children
        tgt : int | None
            Make the execution faster by returning the result as soon as we're sure about the path from `src` to `tgt`

        Return
        ----------
        Return a pair of `dict[int, int]` corresponding to the distances and the previous node id of each node.
        """
        q: list[int] = [src]
        dist: dict[int, int] = {src: 0}
        prev: dict[int, int] = {}

        while q != []:
            u: int = min(q, key=lambda x: dist[x] if x in dist else 1)
            q.pop(q.index(u))
            neighbours: list[int] = self.nodes[u].get_children_ids() if direction == 1 else self.nodes[u].get_parents_ids(
            ) if direction == -1 else [*self.nodes[u].get_children_ids(), *self.nodes[u].get_parents_ids()]

            for v in neighbours:
                if v not in dist.keys():
                    q += [v]
                if v not in dist or dist[v] > dist[u] + 1:
                    dist[v] = dist[u]+1
                    prev[v] = u
                if v == tgt:
                    return dist, prev

        return dist, prev

    def shortest_path(self, u: int, v: int) -> list[int]:
        """
        Find the shortest path from u to v.

        Parameters
        ----------
        u : int
            The src node's id.
        v : int
            The target node's id.

        Return
        ----------
        A list corresponding to the shortest path from `u` to `v`.
        """
        p: list[int] = [v]
        m, res = self.dijkstra(u, 1, v)
        current = v
        while current != u:
            current = res[current]
            p += [current]
        p.reverse()
        return p

    def common_ancestor_dist(self, u: int, v: int) -> dict[int, tuple[int, int]]:
        """
        Return a `dict` mapping each common ancestor to a tuple (dist to `u`, dist to `v`)

        Parameters
        ----------
        u : int
            The first node's id.
        v : int
            The second node's id.

        Return
        ----------
        Return a `dict` mapping each common ancestor to a tuple (dist to `u`, dist to `v`)
        """
        d: dict[int, tuple[int, int]] = {}
        ances_u: dict[int, int] = self.dijkstra(u, -1)[0]
        ances_v: dict[int, int] = self.dijkstra(v, -1)[0]
        for k, v in ances_u.items():
            if k in ances_v.keys():
                d[k] = (v, ances_v[k])

        return d

    def topo_sort(self) -> list[set[int]]:
        """
        Return the different layers of that graph using topologic sort.

        Return
        ----------
        Return the different layers of that graph using topologic sort.
        """
        l: list[set[int]] = []
        nodes: dict[int, node] = self.nodes.copy()
        while nodes != {}:
            s: set[int] = set()
            for identif, n in nodes.items():
                if len(set(n.get_parents_ids()).difference(set([elem for t in l for elem in t]))) == 0:
                    s.add(identif)

            if len(s) == 0:
                raise AttributeError("The specified graph is cyclic.")
            l += [s]
            for e in s:
                nodes.pop(e)
        return l

    def node_depth(self, node_id: int) -> int:
        """
        Compute the depth in the graph of the node with `node_id` as id.
        Returns -1 if there is no node with that specific id in this graph.
        The value vary between 1 and n, n being the depth of the graph.

        Parameters
        ----------
        node_id : int
            The id of the node we want to know the depth.

        Return
        ----------
        Return the depth in the graph of the node with `node_id` as id.
        """
        tmp: list[set[int]] = self.topo_sort()
        for i, t in enumerate(tmp):
            if node_id in t:
                return i+1

        return -1

    def depth(self) -> int:
        """
        Compute the depth of this graph.
        Returns -1 if this graph is empty.
        Returns 1 if there is only one node in this graph.

        Return
        ----------
        Return the depth of the graph.
        """
        s: int = len(self.topo_sort())
        return s if s != 0 else -1

    def longuest_path(self, u: int, v: int) -> tuple[list[int], int]:
        """
        Return a pair containing the path from `u` to `v` and its length.

        Parameters
        ----------
        u : int
            The first node's id.
        v : int
            The second node's id.

        Return
        ----------
        Return a pair containing the path from `u` to `v` and its length.
        """
        topo: list[set[int]] = self.topo_sort()
        node_u: node = self.nodes[u]
        node_v: node = self.nodes[v]
        k: int = [i for i, v in enumerate(topo) if u in v][0]
        dist: dict[int, int] = {u: 0}
        prev: dict[int, int] = {}

        while v not in topo[k]:
            for w in topo[k]:
                node_w: node = self.nodes[w]
                if len(set(node_w.get_parents_ids()).intersection(set(dist.keys()))) != 0:
                    i: int = max([i for i in set(node_w.get_parents_ids()).intersection(
                        set(dist.keys()))], key=lambda x: dist[x])
                    dist[w] = dist[i] + 1
                    prev[w] = i
            k += 1

        return list(dist.keys()) + [v], len(dist.keys())

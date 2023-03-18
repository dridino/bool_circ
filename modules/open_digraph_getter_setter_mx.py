from modules.node import node


class open_digraph_getter_setter_mx:

    def get_input_ids(self) -> list[int]:
        """
        Return
        ----------
        A list containing every input id of the graph.
        """
        return self.inputs

    def get_output_ids(self) -> list[int]:
        """
        Return
        ----------
        A list containing every output id of the graph.
        """
        return self.outputs

    def get_id_node_map(self) -> dict[int, node]:
        """
        Return
        ----------
        A map containing every `{ id : node }` of the graph.
        """
        return self.nodes

    def get_nodes(self) -> list[node]:
        """
        Return
        ----------
        A list containing every node of the graph.
        """
        return list(self.nodes.values())

    def get_node_ids(self) -> list[int]:
        """
        Return
        ----------
        A list containing every id of the graph.
        """
        return list(self.nodes.keys())

    def get_node_by_id(self, identif: int) -> node:
        """
        Return the node in the graph whose `id` is equal to `identif`.

        Parameters
        ----------
        identif : int
            The id of the desired node.

        Return
        ----------
        The node in the graph whose `id` is equal to `identif`
        """
        return self.nodes[identif]

    def __getitem__(self, identif: int) -> node:
        """
        Return the node in the graph whose `id` is equal to `identif`.

        Parameters
        ----------
        identif : int
            The id of the desired node.

        Return
        ----------
        The node in the graph whose `id` is equal to `identif`
        """
        return self.get_node_by_id(identif)

    def get_nodes_by_ids(self, ids: list[int]) -> list[node]:
        """
        Return a list of nodes whose `id`s are in `ids`.

        Parameters
        ----------
        ids : list[int]
            The ids of the desired nodes.

        Return
        ----------
        A list of nodes whose `id`s are in `ids`
        """
        return [self.get_node_by_id(identif) for identif in ids]

    def set_input_ids(self, identifs: list[int]) -> None:
        """
        Set the input ids to identifs.

        Parameters
        ----------
        identifs : list[int]
            The new ids for the input nodes.
        """
        self.inputs = identifs

    def set_output_ids(self, identifs: list[int]) -> None:
        """
        Set the output ids to identifs.

        Parameters
        ----------
        identifs : list[int]
            The new ids for the output nodes.
        """
        self.outputs = identifs

    def add_input_id(self, identif: int) -> None:
        """
        Add `identif` to the input ids list.

        Parameters
        ----------
        identif : int
            The new id for the input nodes.
        """
        if identif not in self.inputs:
            self.inputs += [identif]

    def add_output_id(self, identif: int) -> None:
        """
        Add `identif` to the output ids list.

        Parameters
        ----------
        identif : int
            The new id for the output nodes.
        """
        if identif not in self.outputs:
            self.outputs += [identif]

    def new_id(self) -> int:
        """
        Return
        ----------
        A new unused id.
        """
        return max(list(self.nodes.keys())) + 1

    def add_edge(self, src: int, tgt: int) -> None:
        """
        Add an edge from src to tgt.

        Parameters
        ----------
        src : int
            The source id.

        tgt : int
            The target id.
        """
        self.nodes[src].add_child_id(tgt)
        self.nodes[tgt].add_parent_id(src)

    def add_edges(self, edges: list[tuple[int, int]]) -> None:
        """
        Add all the edges from edges, which is a list as `[(src, tgt), (src, tgt), ...]`.

        Parameters
        ----------
        edges : list[tuple[int, int]]
            The list of edges such as `[(src, tgt), (src, tgt), ...]`.
        """
        for src, tgt in edges:
            self.add_edge(src, tgt)

    def add_node(self, label: str = '', parents: dict[int, int] | None = None, children: dict[int, int] | None = None) -> int:
        """
        Add a node with `label` as label, `parents` as parents and `children` as children. Return the `id` of this newly created node.

        Parameters
        ----------
        label : str
            The node's `label`, default to `''`.

        parents : dict[int, int] | None
            The node's `parents`, default to `None`.

        children : dict[int, int] | None
            The node's `children`, default to `None`.

        Return
        ----------
        The `id` of the newly created node.
        """
        identif: int = self.new_id()
        n: node = node(identif, label, {} if parents ==
                       None else parents, {} if children == None else children)
        self.nodes[identif] = n
        if parents != None:
            for k, v in parents.items():
                for _ in range(v):
                    self.nodes[k].add_child_id(identif)
        if children != None:
            for k, v in children.items():
                for _ in range(v):
                    self.nodes[k].add_parent_id(identif)
        return identif

    def remove_edge(self, src: int, tgt: int) -> None:
        """
        Remove an edge from src to tgt.

        Parameters
        ----------
        src : int
            The source id.

        tgt : int
            The target id.
        """
        self.get_node_by_id(src).remove_child_once(tgt)
        self.get_node_by_id(tgt).remove_parent_once(src)

    def remove_parallel_edges(self, src: int, tgt: int) -> None:
        """
        Remove all edges from src to tgt.

        Parameters
        ----------
        src : int
            The source id.

        tgt : int
            The target id.
        """
        self.get_node_by_id(src).remove_child_id(tgt)
        self.get_node_by_id(tgt).remove_parent_id(src)

    def remove_node_by_id(self, identif: int) -> None:
        """
        Remove the node with `identif` as id.

        Parameters
        ----------
        identif : int
            The node's we want to remove id.
        """
        if identif in self.get_node_ids():
            if identif in self.get_input_ids():
                self.inputs.remove(identif)
            elif identif in self.get_output_ids():
                self.outputs.remove(identif)
            n = self.nodes.pop(identif)
            for c in n.children:
                self.nodes[c].remove_parent_id(identif)
            for p in n.parents:
                self.nodes[p].remove_child_id(identif)
        else:
            raise ValueError("This id doesn't exist in the graph.")

    def remove_edges(self, l: list[tuple[int, int]]) -> None:
        """
        Remove all edges from l.

        Parameters
        ----------
        l : list[tuple[int, int]]
            The list of edges such as `[(src, tgt), (src, tgt), ...]`.
        """
        for src, tgt in l:
            self.remove_edge(src, tgt)

    def remove_several_parallel_edges(self, l: list[tuple[int, int]]) -> None:
        """
        Remove all edges between sources and targets from l.

        Parameters
        ----------
        l : list[tuple[int, int]]
            The list of edges such as `[(src, tgt), (src, tgt), ...]`.
        """
        for src, tgt in l:
            self.remove_parallel_edges(src, tgt)

    def remove_nodes_by_id(self, l: list[int]) -> None:
        """
        Remove all nodes whose ids are in l.

        Parameters
        ----------
        l : list[int]
            The list of ids we want to remove.
        """
        for identif in l:
            self.remove_node_by_id(identif)

    def add_input_node(self, identif: int) -> int:
        """
        Create an input node, child of a node with `identif` as id and a label of "". `parents` is set to `{}` and `children` is set to `{identif: 1}`.
        Raise an `AttributeError` if there's no node in the graph with `identif` as `id`.

        Parameters
        ----------
        identif : int
            The id of the child of the newly created input node.

        Return
        ----------
        The id of the newly created input node.
        """
        if identif in self.nodes.keys():
            if identif in self.inputs:
                self.inputs.remove(identif)
            newId: int = self.add_node(children={identif: 1})
            self.add_input_id(newId)
            return newId
        else:
            raise AttributeError("The specified ID isn't in the graph.")

    def add_output_node(self, identif: int) -> int:
        """
        Create an output node, child of a node with `identif` as id and a label of "". `parents` is set to `{identif: 1}` and `children` is set to `{}`.

        Parameters
        ----------
        identif : int
            The id of the parent of the newly created output node.

        Return
        ----------
        The id of the newly created output node.
        """
        if identif in self.nodes.keys():
            if identif in self.outputs:
                self.outputs.remove(identif)
            newId: int = self.add_node(parents={identif: 1})
            self.add_output_id(newId)
            return newId
        else:
            raise AttributeError("The specified ID isn't in the graph.")

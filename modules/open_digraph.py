class node:
    def __init__(self, identity: int, label: str, parents: dict[int, int], children: dict[int, int]):
        '''
        identity: int; its unique identifin the graph
        label: string;
        parents: int->int dict; maps a parent node's identifto its multiplicity
        children: int->int dict; maps a child node's identifto its multiplicity
        '''
        self.identif: int = identity
        self.label: str = label
        self.parents: dict[int, int] = parents
        self.children: dict[int, int] = children

    def __str__(self) -> str:
        """Return a string representation of this node."""
        return f"identif: {self.identif} | label : {self.label}"

    def __repr__(self) -> str:
        """Return the representation of the node object."""
        return f"identif: {self.identif} | label : {self.label} | parents : {self.parents} | children : {self.parents}"

    def copy(self):
        return node(self.identif, self.label, self.parents.copy(), self.children.copy())

    def get_id(self) -> int:
        """Return the `id` of this node."""
        return self.identif

    def get_label(self) -> str:
        """Return the `label` of this node."""
        return self.label

    def get_children(self) -> dict[int, int]:
        """Return the `children` of the current node."""
        return self.children

    def get_parents(self) -> dict[int, int]:
        """Return the `parents` of the current node."""
        return self.parents

    def get_parents_ids(self) -> list[int]:
        """Return the list of all its parents' `id`s."""
        return list(self.parents.keys())

    def get_children_ids(self) -> list[int]:
        """Return the list of all its children's `id`s."""
        return list(self.children.keys())

    def get_child_multiplicity(self, identif: int) -> int:
        """
        Return the multiplicty of the child node with `identif` as `id`. Return -1 there's no such node.

        Parameters
        ----------
        identif : int
            The node's id
        """
        res: int | None = self.children.get(identif)
        return res if res != None else -1

    def get_parent_multiplicity(self, identif: int) -> int:
        """
        Return the multiplicty of the parent node with `identif` as `id`. Return -1 if there's no such node.

        Parameters
        ----------
        identif : int
            The node's id
        """
        res: int | None = self.parents.get(identif)
        return res if res != None else -1

    def set_id(self, identif: int) -> None:
        """
        Set this node's id to `identif`.

        Parameters
        ----------
        identif: int
            The new id
        """
        self.identif = identif

    def set_label(self, lab: str) -> None:
        """
        Set this node's label to `lab`.

        Parameters
        ----------
        lab: str
            The new label
        """
        self.label = lab

    def set_parent_ids(self, ids: list[int]) -> None:
        """
        Set this nodes parent ids to `ids`.

        Parameters
        ----------
        ids: list[int]
            The new list of parents ids.
        """
        for i in range(min(len(self.parents), len(ids))):
            k: int = list(self.parents.keys())[i]
            self.parents[ids[i]] = self.parents[k]
            self.parents.pop(k)

    def set_children_ids(self, ids: list[int]) -> None:
        """
        Set this nodes parent ids to `ids`.

        Parameters
        ----------
        ids: list[int]
            The new list of children ids.
        """
        for i in range(min(len(self.children), len(ids))):
            k: int = list(self.children.keys())[i]
            self.children[ids[i]] = self.children[k]
            self.parents.pop(k)

    def add_child_id(self, identif: int) -> None:
        """
        Add `identif` to the children ids list.

        Parameters
        ----------
        identif: int
            The id to add to the children ids list.
        """
        if identif in self.children.keys():
            self.children[identif] += 1
        else:
            self.children[identif] = 1

    def add_parent_id(self, identif: int) -> None:
        """
        Add `identif` to the parents ids list.

        Parameters
        ----------
        identif: int
            The id to add to the parents ids list.
        """
        if identif in self.parents.keys():
            self.parents[identif] += 1
        else:
            self.parents[identif] = 1

    def remove_parent_once(self, identif: int) -> None:
        """
        Remove once the parent node with `identif` as `id`, if there.

        Parameters
        ----------
        identif: int
            The id of the parent node that should be removed once.
        """
        if identif in self.get_parents_ids():
            self.parents[identif] -= 1
            if self.parents[identif] <= 0:
                self.parents.pop(identif)

    def remove_child_once(self, identif: int) -> None:
        """
        Remove once the child node with `identif` as `id`, if there.

        Parameters
        ----------
        identif: int
            The id of the child node that should be removed once.
        """
        if identif in self.get_children_ids():
            self.children[identif] -= 1
            if self.children[identif] <= 0:
                self.children.pop(identif)

    def remove_parent_id(self, identif: int) -> None:
        """
        Totally remove the parent node with `identif` as `id`, if there.

        Parameters
        ----------
        identif: int
            The id of the parent node that should be totally removed.
        """
        for _ in range(self.parents[identif]):
            self.remove_parent_once(identif)

    def remove_child_id(self, identif: int) -> None:
        """
        Totally remove once the child node with `identif` as `id`, if there.

        Parameters
        ----------
        identif: int
            The id of the child node that should be totally removed.
        """
        for _ in range(self.children[identif]):
            self.remove_child_once(identif)


class open_digraph:  # for opened directed graph
    def __init__(self, inputs: list[int], outputs: list[int], nodes: list[node]):
        '''
        inputs: int list; the ids of the input nodes
        outputs: int list; the ids of the output nodes
        nodes: node iter;
        '''
        self.inputs: list[int] = inputs
        self.outputs: list[int] = outputs
        self.nodes: dict[int, node] = {node.get_id(): node for node in nodes}

    def __str__(self) -> str:
        """Return the string representation of that node."""
        s: str = f"inputs : {self.inputs} | outputs : {self.outputs}\n"
        for _, v in self.nodes.items():
            s += str(v) + "\n"
        return s

    def __repr__(self) -> str:
        """Return a string that represents this node as an object."""
        s: str = f"inputs : {self.inputs} | outputs : {self.outputs}\n"
        for _, v in self.nodes.items():
            s += repr(v)
        return s

    @classmethod
    def empty(cls):
        """Return an empty open_digraph."""
        return cls([], [], [])

    def copy(self):
        """Copy the current open_digraph."""
        return open_digraph([e for e in self.inputs], [e for e in self.outputs], [e for e in list(self.nodes.values())])

    def get_outputs(self) -> list[int]:
        """Return the outputs of the current digraph."""
        return self.outputs

    def get_input_ids(self) -> list[int]:
        """Return a list containing every input id of the graph."""
        return self.inputs

    def get_output_ids(self) -> list[int]:
        """Return a list containing every output id of the graph."""
        return self.outputs

    def get_id_node_map(self) -> dict[int, node]:
        """Return a map containing every `{ id : node }` of the graph."""
        return self.nodes

    def get_nodes(self) -> list[node]:
        """Return a list containing every node of the graph."""
        return list(self.nodes.values())

    def get_node_ids(self) -> list[int]:
        """Return a list containing every id of the graph."""
        return list(self.nodes.keys())

    def get_node_by_id(self, identif: int) -> node:
        """
        Return a node with `identif` as `id`.

        Parameters
        ----------
        identif : int
            The id of the desired node.
        """
        return self.nodes[identif]

    def __getitem__(self, identif: int) -> node:
        """
        Return a node with `identif` as `id`.

        Parameters
        ----------
        identif : int
            The id of the desired node.
        """
        return self.get_node_by_id(identif)

    def get_nodes_by_ids(self, ids: list[int]) -> list[node]:
        """
        Return a list of nodes whose `id`s are in `ids`.

        Parameters
        ----------
        ids : list[int]
            The ids of the desired nodes.
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
        """Return an unused id."""
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

    def add_node(self, label: str = '', parents: dict[int, int] | None = None, children: dict[int, int] | None = None):
        """
        Add a node with `label` as label, `parents` as parents and `children` as children.

        Parameters
        ----------
        label : str
            The node's `label`.

        parents : dict[int, int] | None
            The node's `parents`.

        children : dict[int, int] | None
            The node's `children`.
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
        u: node = self.get_node_by_id(identif)
        for i in u.get_children_ids():
            self.remove_parallel_edges(identif, i)
        for j in u.get_parents_ids():
            self.remove_parallel_edges(j, identif)
        self.nodes.pop(identif)

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

    def is_well_formed(self) -> bool:
        """
        Return true if the graph is well formed.
        """
        node_ids: list[int] = self.get_node_ids()
        # check des inputs
        for i in self.get_input_ids():
            n: node = self.get_node_by_id(i)
            if (i not in node_ids) or (n.get_parents_ids() != []) or (len(n.get_children_ids()) != 1) or (n.get_child_multiplicity(n.get_children_ids()[0]) != 1):
                return False

        # check des outputs
        for o in self.get_output_ids():
            n: node = self.get_node_by_id(o)
            if (o not in node_ids) or (n.get_children_ids() != []) or (len(n.get_parents_ids()) != 1) or (n.get_parent_multiplicity(n.get_parents_ids()[0]) != 1):
                return False

        # clé de node pointe vers un noeud d'id la clé
        for k, v in self.nodes.items():
            if k != v.get_id():
                return False

        # check vice-versa parent-enfant
        for i, n in self.nodes.items():
            for j, m in n.get_children().items():
                if (i not in self.get_node_by_id(j).get_parents_ids()) or (m != self.get_node_by_id(j).get_parent_multiplicity(i)):
                    return False

        return True

    def assert_is_well_formed(self) -> None:
        """Assert if the graph is well formed."""
        assert self.is_well_formed(), "Le graphe n'est pas bien formé"

    def add_input_node(self, identif: int) -> int:
        """
        Create an input node, child of a node with `identif` as id and a label of "". `parents` is set to `{}` and `children` is set to `{identif: 1}`.

        Parameters
        ----------
        identif : int
            The id of the child of the newly created input node.
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
        """
        if identif in self.nodes.keys():
            if identif in self.outputs:
                self.outputs.remove(identif)
            newId: int = self.add_node(parents={identif: 1})
            self.add_output_id(newId)
            return newId
        else:
            raise AttributeError("The specified ID isn't in the graph.")

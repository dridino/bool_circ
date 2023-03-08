import random as random
import os as os


class node:
    def __init__(self, identity: int, label: str, parents: dict[int, int], children: dict[int, int]):
        """
        Parameters
        ----------
        identity : int
            The node's unique id.

        label : str
            The node's label.

        parents : dict[int, int]
            Maps a parent node's id to its multiplicity.

        children : dict[int, int]
            Maps a child node's id to its multiplicity.

        Return
        ----------
        A new node with the corresponding parameters.
        """
        self.identif: int = identity
        self.label: str = label
        self.parents: dict[int, int] = parents
        self.children: dict[int, int] = children

    def __str__(self) -> str:
        """
        Return
        ----------
        A string representation of this node.
        """
        return f"identif: {self.identif} | label : {self.label}"

    def __repr__(self) -> str:
        """
        Return
        ----------
        The string representation of the node object.
        """
        return f"identif : {self.identif} | label : {self.label} | parents : {self.parents} | children : {self.children}"

    def __eq__(self, other) -> bool:
        """Return `True` if both nodes are equal."""
        return self.identif == other.identif and self.label == other.get_label() and self.children == other.children and self.parents == other.parents

    def copy(self):
        """
        Return
        ----------
        A copy of this node.
        """
        return node(self.identif, self.label, self.parents.copy(), self.children.copy())

    def get_id(self) -> int:
        """
        Return
        ----------
        The `id` of this node.
        """
        return self.identif

    def get_label(self) -> str:
        """
        Return
        ----------
        The `label` of this node.
        """
        return self.label

    def get_children(self) -> dict[int, int]:
        """
        Return
        ----------
        The `children` of the current node.
        """
        return self.children

    def get_parents(self) -> dict[int, int]:
        """
        Return
        ----------
        The `parents` of the current node.
        """
        return self.parents

    def get_parents_ids(self) -> list[int]:
        """
        Return
        ----------
        The list of all its parents' `id`s.
        """
        return list(self.parents.keys())

    def get_children_ids(self) -> list[int]:
        """
        Return
        ----------
        The list of all its children's `id`s.
        """
        return list(self.children.keys())

    def get_child_multiplicity(self, identif: int) -> int:
        """
        Return the multiplicty of the child node with `identif` as `id`. Return -1 there's no such node.

        Parameters
        ----------
        identif : int
            The node's id

        Return
        ----------
        int:
            The multiplicty of the child with `identif` as `id`.
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

        Return
        ----------
        int:
            The multiplicity of the parent with `identif` as `id`
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
        tmp: list[int] = list(self.parents.keys())
        for i in range(min(len(self.parents), len(ids))):
            k: int = tmp[i]
            self.parents[ids[i]] = self.parents[k]
            self.parents.pop(k)

    def set_parents(self, new_parents: dict[int, int]) -> None:
        """
        Set this node's parents to `new_parents`.

        Parameters
        ----------
        new_parents : dict[int, int]
            The map of `{node_id : multiplicity}` that represents the new parents of this node.
        """
        self.parents = new_parents

    def set_children(self, new_children: dict[int, int]) -> None:
        """
        Set this node's children to `new_children`.

        Parameters
        ----------
        new_children : dict[int, int]
            The map of `{node_id : multiplicity}` that represents the new children of this node.
        """
        self.children = new_children

    def set_children_ids(self, ids: list[int]) -> None:
        """
        Set this nodes parent ids to `ids`.

        Parameters
        ----------
        ids: list[int]
            The new list of children ids.
        """
        tmp: list[int] = list(self.children.keys()).copy()
        for i in range(min(len(self.children), len(ids))):
            k: int = tmp[i]
            self.children[ids[i]] = self.children[k]
            self.children.pop(k)

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
        Totally remove the child node with `identif` as `id`, if there.

        Parameters
        ----------
        identif: int
            The id of the child node that should be totally removed.
        """
        for _ in range(self.children[identif]):
            self.remove_child_once(identif)

    def indegree(self) -> int:
        """
        Return the number of node pointing to this node.

        Return
        ----------
        Return the number of node pointing to this node.
        """
        return sum([v for v in self.parents.values()])

    def outdegree(self) -> int:
        """
        Return the number of node this node is pointing to.

        Return
        ----------
        Return the number of node this node is pointing to.
        """
        return sum([v for v in self.children.values()])

    def degree(self) -> int:
        """
        Return the number of node this node is pointing to + the number of node pointing to this node. (i.e. indegree() + outdegree())

        Return
        ----------
        Return the number of node this node is pointing to + the number of node pointing to this node.
        """
        return self.indegree() + self.outdegree()


class open_digraph:  # for opened directed graph
    def __init__(self, inputs: list[int], outputs: list[int], nodes: list[node]) -> None:
        """
        Create an open_digraph with the corresponding parameters.

        Parameters
        ----------
        inputs: list[int]
            The ids of the input nodes

        outputs: list[int]
            The ids of the output nodes

        nodes: list[node]
            The nodes of the graph

        Return
        ----------
        A new graph with `inputs` as inputs, `outputs` as outputs and `nodes` as nodes.
        """
        self.inputs: list[int] = inputs
        self.outputs: list[int] = outputs
        self.nodes: dict[int, node] = {node.get_id(): node for node in nodes}

    def __str__(self) -> str:
        """
        Return
        ----------
        The string representation of that node.
        """
        s: str = f"inputs : {self.inputs} | outputs : {self.outputs}\n"
        for _, v in self.nodes.items():
            s += str(v) + "\n"
        return s

    def __repr__(self) -> str:
        """
        Return
        ----------
        A string that represents this node as an object.
        """
        s: str = f"inputs : {self.inputs} | outputs : {self.outputs}\n"
        for _, v in self.nodes.items():
            s += repr(v) + "\n"
        return s

    def __eq__(self, other) -> bool:
        """Returns `True` if both graph are equal."""
        return self.nodes == other.nodes and self.inputs == other.inputs and self.outputs == other.outputs

    @classmethod
    def empty(cls):
        """
        Return
        ----------
        An empty open_digraph, where inputs, outputs and nodes are all set to `[]`.
        """
        return cls([], [], [])

    @classmethod
    def random(cls, n: int, bound: int, inputs: int = 0, outputs: int = 0, form: str = "free"):
        """
        Return a graph matching all given conditions.
        All graphs will have `n` nodes, with maximum `bound` multiplicity,
        `inputs` inputs and `outputs` outputs.

        Possibilities
        ----------

        Flags (to add after the graph name. eg : `"free null_diag"`) :
            - `"null_diag"` : force the graph to have no node pointing directly to itself. (useless for `"dag"`)

        Options :
            - `"free"`: default
                Return a graph from a totally random matrix.

            - `"symetric"`:
                Return a graph where if multiplicit from `i` to `j` is m, then multiplicity from `j` to `i` is also m.

            - `"oriented"`:
                Return an oriented graph.

            - `"dag"`:
                Return an acyclic oriented graph.

        Parameters
        ----------
        n: int
            The number of nodes.

        bound: int
            The maximum multiplicity (included)

        inputs: int
            The number of desired inputs. Default to 0.

        outputs: int
            The number of desired outputs. Default to 0.

        form: str
            A string representing the type of graph we want.

        Return
        ----------
        A graph matching all the criterias, if possible, otherwise returns an empty graph.
        """
        if inputs > n:
            print("\033[91m[ ! ] The number of inputs requested is greater than the number of nodes, such a graph is impossible to create. Try with a lower inputs value.\033[0m")
            return cls.empty()
        elif outputs > n:
            print("\033[91m[ ! ] The number of outputs requested is greater than the number of nodes, such a graph is impossible to create. Try with a lower outputs value.\033[0m")
            return cls.empty()
        elif inputs + outputs > n:
            print("\033[91m[ ! ] The sum of inputs and outputs requested is greater than the number of nodes, such a graph is impossible to create. Try with lower inputs or outputs values.\033[0m")
            return cls.empty()
        elif "free" in form:
            return matrix.free(n, bound, "null_diag" in form).to_graph(inputs, outputs)
        elif "symetric" in form:
            return matrix.symetric(n, bound, "null_diag" in form).to_graph(inputs, outputs)
        elif "oriented" in form:
            return matrix.oriented(n, bound, "null_diag" in form).to_graph(inputs, outputs)
        elif "dag" in form:
            return matrix.loop_free(n, bound).to_graph(inputs, outputs)
        else:
            print("\033[91m[ ! ] The combinaison you asked for is not available, refer to the doc to see what type of graph you can create.\033[0m")
            return cls.empty()

    @classmethod
    def identity(cls, n: int):
        """
        Return the identity `open_digraph` for sequential composition, with `n` inputs and `n` outputs.

        Parameters:
        ----------
        n : int
            The number of nodes this `open_digraph` should contain.

        Return
        ----------
        An `open_digraph` whose inputs are only connected to the corresponding outputs
        """
        g = cls.empty()
        g.set_input_ids([i for i in range(n)])
        g.set_output_ids([i for i in range(n, 2*n)])
        # inputs
        g.nodes = {i: node(i, f"i{i}", {}, {i+n: 1}) for i in range(n)}
        # outputs
        g.nodes = {i: node(i, f"o{i}", {i-n: 1}, {}) for i in range(n, 2*n)}
        return g

    def split_line(self, s: str) -> tuple[str, str, str]:
        """
        Given a string like `"id [label=..., type=...]"` returns `(id, label, type)`.

        Parameters
        ----------
        s : str
            The string we want to parse

        Return
        ----------
        Returns `(id, label, type)`.
        """
        l: list[str] = ["", "", ""]
        idx: int = 0
        i: int = 0
        while i < len(s) - 1:
            c: str = s[i]
            if c == "\"":
                temp: int = 1
                res: str = ""
                while s[i+temp] != "\"":
                    res += s[i+temp]
                    temp += 1
                l[idx] = res
                idx += 1
                while s[i+temp] != "=":
                    temp += 1
                temp += 1
                res = ""
                while s[i+temp] != "]":
                    res += s[i+temp]
                    temp += 1
                l[idx] = res
                i += temp
                return tuple(l)
            elif c != " ":
                l[idx] += c
            elif idx == 0:
                idx += 1
                i += 6
            i += 1
        return tuple(l)

    @classmethod
    def from_dot_file(cls, path: str):
        """
        Read a graph saved in a `.dot` file specified by `path`.

        Parameters
        ----------
        path : str
            The location of the `.dot` file that contains the graph.

        Return
        ----------
        Returns an `open_digraph` corresponding to this `.dot` representation.
        """
        inputs: list[int] = []
        outputs: list[int] = []
        nodes: dict[int, node] = {}
        with open(path, "r") as f:
            lines: list[str] = f.readlines()
            for i, l in enumerate(lines):
                if i != 0 and i != len(lines) - 1:
                    if "->" not in l:
                        name, label, t = cls.split_line(cls, l)
                        nodes[int(name)] = node(int(name), label, {}, {})
                        if t == "1":
                            inputs += [int(name)]
                        elif t == "2":
                            outputs += [int(name)]
                    else:
                        temp: list[str] = l[:-2].split("->")
                        nodes[int(temp[0])].add_child_id(int(temp[1]))
                        nodes[int(temp[1])].add_parent_id(int(temp[0]))
        return open_digraph(inputs, outputs, list(nodes.values()))

    def save_as_dot_file(self, path: str, verbose: bool = False) -> None:
        """
        Save the current graph to `path`.

        The field `type` of each node will be :
            - 0 if it's a classic node
            - 1 if it's an input node
            - 2 if it's an output node

        Parameters
        ----------
        path : str
            The path where the file will be saved.

        verbose : bool
            If set to `True`, the id will be displayed below the label, otherwise only the label will be displayed.
        """
        content: list[str] = []
        nodeList: list[str] = []

        for identif, n in self.nodes.items():
            t: int = 1 if identif in self.inputs else 2 if identif in self.outputs else 0
            nodeList += [rf'{identif} [label="{n.get_label()}\nid : {n.get_id()}", type={t}];' + "\n"] if verbose else [
                f"{identif} [label=\"{n.get_label()}\", type={t}];\n"]
            content += [f"{identif}->{c};\n"*m for c,
                        m in n.get_children().items()]

        with open(path, "w") as f:
            f.writelines(["digraph G {\n"] + nodeList + content + ["}"])

    def display(self, verbose: bool = False, name: str = "graph.png") -> None:
        """Display that current graph.

        Parameters
        ----------
        verbose : bool
            If set to `True`, the id will be displayed below the label, otherwise only the label will be displayed.
        """
        self.save_as_dot_file(f"temp/{name}.dot", verbose)
        print(f"Saving the graph at \"outputs/{name}\"...")
        os.system(f'dot.exe -Tpng -o "outputs/{name}" "temp/{name}.dot')

    def mapIntToId(self) -> dict[int, int]:
        """
        Map to each node id a unique integer i such as 0 <= i < n, where n represents the number of nodes in the graph.

        Return
        ----------
        dict[int, int] :
            A dictionnary where the keys are the id of the nodes and the values are a unique integer between 0 and n, where n represents the number of nodes in the graph.
        """
        return {k: i for i, k in enumerate(self.nodes.keys())}

    def adjacencyMatrix(self) -> list[list[int]]:
        """
        Returns the adjacency matrix associated to the graph.

        Return
        ----------
        A `list[list[int]]` representing the adjacency matrix of that graph.
        """
        s: int = len(self.nodes)
        mat: list[list[int]] = [[0 for _ in range(s)] for _ in range(s)]
        m: dict[int, int] = self.mapIntToId()
        for k, n in self.nodes.items():
            for c, mul in n.get_children().items():
                mat[m[k]][m[c]] = mul
        return mat

    def copy(self):
        """
        Copy the current open_digraph.

        Return
        ----------
        A new instance of open_digraph with the same parameters as this one.
        """
        return open_digraph([i for i in self.inputs], [o for o in self.outputs], [n.copy() for n in list(self.nodes.values())])

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

    def is_well_formed(self) -> bool:
        """
        A graph is well formed if :
            - each input and output node is in the graph (is in the nodes `dict`)
            - each input node has only one child, with a multiplicity of 1 and has no parent
            - each output node has only one parent, with a multiplicity of 1 and has no child
            - each key in `nodes` point to a node whose `id` is that specific key
            - if `j` have `i` as child with a multiplicity of `m`, then `i` as `j` as parent with a multiplicity of `m`, and vice-versa

        Return
        ----------
        Return `True` if the graph is well formed, `False` otherwise.
        """
        node_ids: list[int] = self.get_node_ids()
        # inputs check
        for i in self.get_input_ids():
            n: node = self.get_node_by_id(i)
            if (i not in node_ids) or (n.get_parents_ids() != []) or (len(n.get_children_ids()) != 1) or (n.get_child_multiplicity(n.get_children_ids()[0]) != 1):
                return False

        # outputs check
        for o in self.get_output_ids():
            n: node = self.get_node_by_id(o)
            if (o not in node_ids) or (n.get_children_ids() != []) or (len(n.get_parents_ids()) != 1) or (n.get_parent_multiplicity(n.get_parents_ids()[0]) != 1):
                return False

        # node's key point to a node whose id is that specific key check
        for k, v in self.nodes.items():
            if k != v.get_id():
                return False

        # vice-versa check
        for i, n in self.nodes.items():
            for j, m in n.get_children().items():
                if (i not in self.get_node_by_id(j).get_parents_ids()) or (m != self.get_node_by_id(j).get_parent_multiplicity(i)):
                    return False
            for j, m in n.get_parents().items():
                if (i not in self.get_node_by_id(j).get_children_ids()) or (m != self.get_node_by_id(j).get_child_multiplicity(i)):
                    return False

        return True

    def assert_is_well_formed(self) -> None:
        """
        Assert if the graph is well formed.

        See also `open_digraph.is_well_formed`
        """
        assert self.is_well_formed(), "The graph isn't well formed."

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
        l: list[open_digraph] = [open_digraph.empty() for _ in range(res[0])]
        for i in range(res[0]):
            l[i].nodes = {k: v for k, v in self.nodes.items()
                          if k in splitted[i]}
            l[i].inputs = [j for j in self.inputs if j in splitted[i]]
            l[i].outputs = [o for o in self.outputs if o in splitted[i]]
        return l


class matrix:
    def __init__(self, mat: list[list[int]]) -> None:
        """
        Create a matrix (`list[list[int]]`) from `mat`. Used as an interface for all the `classmethod`s.

        Parameters
        ----------

        mat: list[list[int]]
            A square double list of integers.
        """
        self.matrix = mat

    @classmethod
    def free(cls, n: int, bound: int, null_diag: bool = True, number_generator=(lambda: random.betavariate(1, 5))):
        """
        Return a `n*n` matrix whose elements are integers randomly (using `number_generator`) chosen between 0 and `bound` (included).

        Parameters
        ----------
        n: int
              The size of the matrix.

        bound: int
              The maximum value that the elements of the matrix can take (included).

        null_diag: bool
              If set to `True`, the diagonal will contain only 0, otherwise it will contain random integers like every other element. Default to True.

        number_generator: function
            Set the function used to generate random numbers. Default to `random.betavariate(1, 5)`.

        Return
        ----------
        A matrix (list[list[int]]) containing `n*n` integers randomly chosen between 0 and `bound` (included).
        """
        res: list[list[int]] = [
            [int(number_generator() * n) for _ in range(n)] for _ in range(n)]
        if null_diag:
            for i in range(n):
                res[i][i] = 0
        return cls(res)

    @classmethod
    def symetric(cls, n: int, bound: int, null_diag: bool = True, number_generator=(lambda: random.betavariate(1, 5))):
        """
        Return a `n*n` symetric matrix whose elements are integers randomly chosen between 0 and `bound` (included).

        Parameters
        ----------
        n: int
              The size of the matrix.

        bound: int
              The maximum value that the elements of the matrix can take (included).

        null_diag: bool
              If set to `True`, the diagonal will contain only 0, otherwise it will contain random integers like every other element.

        number_generator: function
            Set the function used to generate random numbers. Default to `random.betavariate(1, 5)`.

        Return
        ----------
        A symetric matrix (list[list[int]]) containing `n*n` integers randomly chosen between 0 and `bound` (included).
        """
        res: list[list[int]] = cls.free(
            n, bound, null_diag, number_generator).matrix
        for i in range(n):
            for j in range(i):
                res[j][i] = res[i][j]
        return cls(res)

    @classmethod
    def oriented(cls, n: int, bound: int, null_diag: bool = True, number_generator=(lambda: random.betavariate(1, 5))):
        """
        Return a `n*n` matrix of an oriented graph whose elements are integers randomly chosen between 0 and `bound` (included).

        Parameters
        ----------
        n: int
            The size of the matrix.

        bound: int
            The maximum value that the elements of the matrix can take (included).

        null_diag: bool
            If set to `True`, the diagonal will contain only 0, otherwise it will contain random integers like every other element.

        number_generator: function
            Set the function used to generate random numbers. Default to `random.betavariate(1, 5)`.

        Return
        ----------
        A matrix (list[list[int]]) of an oriented graph containing `n*n` integers randomly chosen between 0 and `bound` (included).
        """
        res: list[list[int]] = cls.free(
            n, bound, null_diag, number_generator).matrix
        for i in range(n):
            for j in range(i):
                # to add randomness, otherwise it would always be a triangular matrix
                if random.randint(0, 1):
                    if res[i][j] != 0:
                        res[j][i] = 0
                else:
                    if res[j][i] != 0:
                        res[i][j] = 0
        return cls(res)

    @classmethod
    def loop_free(cls, n: int, bound: int, number_generator=(lambda: random.betavariate(1, 5))):
        """
        Return a `n*n` triangular matrix of an oriented acyclic graph whose elements are integers randomly chosen between 0 and `bound` (included).

        Parameters
        ----------
        n: int
            The size of the matrix.

        bound: int
            The maximum value that the elements of the matrix can take (included).

        number_generator: function
            Set the function used to generate random numbers. Default to `random.betavariate(1, 5)`.

        Return
        ----------
        A triangular matrix (list[list[int]]) of an oriented acyclic graph containing `n*n` integers randomly chosen between 0 and `bound` (included).
        """
        res: list[list[int]] = cls.free(
            n, bound, number_generator=number_generator).matrix
        for i in range(n):
            for j in range(i+1):
                res[i][j] = 0
        return cls(res)

    def to_graph(self, inputs: int = 0, outputs: int = 0) -> open_digraph:
        """
        Return the open_digraph corresponding to this matrix.

        Return
        ----------
        The open_digraph corresponding to this matrix.
        """
        n: int = len(self.matrix)
        G: open_digraph = open_digraph(
            [] if inputs == 0 else [e[i] for i in range(
                inputs) for e in [random.sample([i for i in range(n)], n)]],
            [] if outputs == 0 else [e[i] for i in range(
                outputs) for e in [random.sample([i for i in range(n)], n)]],
            [node(i, f"{i}", {}, {}) for i in range(n)])
        for i in range(n):
            for j in range(n):
                G.add_edges([(i, j) for _ in range(self.matrix[i][j])])

        return G


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

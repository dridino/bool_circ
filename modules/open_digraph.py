import random as random
import os as os

from modules.utils import split_line
from modules.node import node
from modules.open_digraph_getter_setter_mx import open_digraph_getter_setter_mx
from modules.open_digraph_compositions_mx import open_digraph_compositions_mx
from modules.open_digraph_path_mx import open_digraph_path_mx


# for opened directed graph
class open_digraph(open_digraph_getter_setter_mx, open_digraph_compositions_mx, open_digraph_path_mx):
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
                        name, label, t = split_line(l)
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

    def copy(self):
        """
        Copy the current open_digraph.

        Return
        ----------
        A new instance of open_digraph with the same parameters as this one.
        """
        return open_digraph([i for i in self.inputs], [o for o in self.outputs], [n.copy() for n in list(self.nodes.values())])

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
        print(f"Saving the graph at \"outputs/{name}\"...\n")
        os.system(f'dot.exe -Tpng -o "outputs/{name}" "temp/{name}.dot"')
        os.system(f'"{os.path.abspath(f"./outputs/{name}")}')

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


class matrix(object):
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

    def to_graph(self, inputs: int = 0, outputs: int = 0):
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

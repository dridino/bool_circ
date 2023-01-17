class node:
    def __init__(self, identity, label, parents, children):
        '''
        identity: int; its unique identifin the graph
        label: string;
        parents: int->int dict; maps a parent node's identifto its multiplicity
        children: int->int dict; maps a child node's identifto its multiplicity
        '''
        self.identif = identity
        self.label = label
        self.parents = parents
        self.children = children

    def __str__(self):
        """string"""
        return f"identif: {self.id} | label : {self.label}"

    def __repr__(self):
        return f"identif: {self.id} | label : {self.label} | parents : {self.parents} | children : {self.parents}"

    def get_id(self):
        return self.id

    def get_label(self):
        return self.label

    def get_parents_id(self):
        return self.parents.keys()

    def get_children_id(self):
        return self.children.keys()

    def set_id(self, identif):
        self.identif = id

    def set_label(self, lab):
        self.label = lab

    def set_parent_ids(self, ids):
        """suppose que les clés sont dans l'ordre"""
        for i in range(min(len(self.parents), len(ids))):
            k = self.parents.keys()[i]
            self.parents[ids[i]] = self.parents[k]
            del(self.parents[k])

    def set_children_ids(self, ids):
        """suppose que les clés sont dans l'ordre"""
        for i in range(min(len(self.children), len(ids))):
            k = self.children.keys()[i]
            self.children[ids[i]] = self.children[k]
            del(self.children[k])

    def add_child_id(self, identif):
        if identif in self.children.keys():
            self.children[id] += 1
        else:
            self.children[id] = 1

    def add_parent_id(self, identif):
        if identif in self.parents.keys():
            self.parents[id] += 1
        else:
            self.parents[id] = 1


class open_digraph:  # for opened directed graph
    def __init__(self, inputs, outputs, nodes):
        '''
        inputs: int list; the ids of the input nodes
        outputs: int list; the ids of the output nodes
        nodes: node iter;
        '''
        self.inputs = inputs
        self.outputs = outputs
        # self.nodes: <int,node> dict
        self.nodes = {node.id: node for node in nodes}

    def __str__(self):
        s = f"inputs : {self.inputs} | outputs : {self.outputs}\n"
        for _, v in self.nodes.items():
            s += str(v) + "\n"
        return s

    def __repr__(self):
        s = f"inputs : {self.inputs} | outputs : {self.outputs}\n"
        for _, v in self.nodes.items():
            s += repr(v)
        return s

    @classmethod
    def empty(cls):
        return cls([], [], [])

    def copy(self):
        return open_digraph(self.inputs, self.outputs, self.nodes.values())

    def get_input_ids(self):
        return self.inputs

    def get_output_ids(self):
        return self.outputs

    def get_id_node_map(self):
        return self.nodes

    def get_nodes(self):
        return self.nodes.values()

    def get_node_ids(self):
        return self.nodes.keys()

    def get_node_by_id(self, identif):
        return self.nodes[id]

    def __getitem__(self, identif):
        return self.get_node_by_id(identif)

    def get_nodes_by_ids(self, ids):
        return [self.get_node_by_id(identif) for identif in ids]

    def set_input_ids(self, identifs):
        self.inputs = identifs

    def set_output_ids(self, identifs):
        self.outputs = identifs

    def add_input_id(self, identif):
        if identif not in self.inputs:
            self.inputs += [identif]

    def add_output_id(self, identif):
        if identif not in self.outputs:
            self.outputs += [identif]

    def new_id(self):
        return max(self.nodes.values()) + 1

    def add_edge(self, src, tgt):
        self.nodes[src].add_child_id(tgt)
        self.nodes[tgt].add_parent_id(src)

    def add_edges(self, edges):
        for src, tgt in edges:
            self.add_edge(src, tgt)

    def add_node(self, label='', parents=None, children=None):
        identif = self.new_id()
        n = node(identif, label, {} if parents ==
                 None else parents, {} if children == None else children)
        self.nodes[identif] = n
        if parents != None:
            for k, v in parents:
                for _ in range(v):
                    self.nodes[k].add_child_id(identif)
        if children != None:
            for k, v in children:
                for _ in range(v):
                    self.nodes[k].add_parent_id(identif)
        return identif

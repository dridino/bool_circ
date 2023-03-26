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
        if identif in self.parents:
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
        if identif in self.children:
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

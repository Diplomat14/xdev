import xdev.core.logger

class tree_type(object):

    def __init__(self, logger):
        assert isinstance(logger, xdev.core.logger.logger), "Logger is of wrong type"
        self.__logger = logger
        self.__roots = []

    def add_root_node(self,rootnode):
        assert isinstance(rootnode, tree_node_type), "Tree node is of wrong type"
        if rootnode not in self.__roots:
            self.__roots.append(rootnode)

    def remove_root_node(self,rootnode):
        assert isinstance(rootnode, tree_node_type), "Tree node is of wrong type"
        if rootnode in self.__roots:
            self.__roots.remove(rootnode)

    # Treats root node of provided subtree as one of root nddes for this tree
    def addRootSubtree(self,subtree):
        assert isinstance(subtree, tree_type), "Tree is of wrong type"
        other_roots = subtree.roots
        for other_root in other_roots:
            self.add_root_node(other_root)

    def __addSubtree(self,parentnode,subtree):
        assert isinstance(parentnode, tree_node_type), "Tree node is of wrong type"
        assert isinstance(subtree, tree_type), "Tree is of wrong type"
        other_roots = subtree.roots
        for other_root in other_roots:
            if not parentnode.has_direct_child(other_root):
                parentnode.add_child(other_root)

    @property
    def roots(self):
        return self.__roots

    # Searches data in a tree
    # @deep Bool If deep search has to be done
    def contains_data(self, data):
        return True if self.find_node_by_data(data) != None else False

    def find_node_by_data(self,data):
        for tree_node in self.roots:
            search_result = tree_node.find_data(data, True)
            if search_result != None:
                return search_result
        return None


class tree_node_type(object):

    def __init__(self, data):
        self.__data = data
        self.__parent = None
        self.__children = []

    def __set_parent(self,parent):
        assert isinstance(parent, tree_node_type), "Tree node is of wrong type"
        self.__parent = parent

    def add_children(self,children):
        for ch in children:
            self.add_child(ch)

    def add_child(self,childnode):
        assert isinstance(childnode, tree_node_type), "Tree node is of wrong type"
        self.__children.append(childnode)
        childnode.__set_parent(self)

    def has_direct_child(self, childnode):
        return True if childnode in self.__children else False

    def has_children(self):
        return True if len(self.__children)>0 else False

    @property
    def data(self):
        return self.__data

    @property
    def parent(self):
        return self.__parent

    @property
    def children(self):
        return self.__children

    # Searches data in a tree and returns corresponding tree node
    # @deep Bool If deep search has to be done
    def find_data(self,data,deep):
        if self.data == data:
            return self
        elif deep == True:
            for ch in self.children:
                search_result = ch.find_data(data,True)
                if search_result != None:
                    return search_result
        else:
            return None
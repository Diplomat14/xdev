from xdev.types.complex.tree import tree_type
from xdev.types.complex.tree import tree_node_type
from xdev.types.complex.graph import graph_type
from xdev.types.complex.graph import graph_node_type
from xdev.core.logger import logger

class graph_to_tree_converter(object):

    def __init__(self,l, data_to_string_converter, value_by_field):
        self.__logger = logger.from_parent('G2T',l)
        self.__data_to_string = data_to_string_converter
        self.__value_by_field = value_by_field

    def convert(self, datagraph, starting_nodes, graph_root_for_not_processed_data, rules, sort_rules):
        assert isinstance(datagraph, graph_type), "Datagraph is of wrong type"
        assert isinstance(rules, conversionrules), "rules is of wrong type"

        l = self.__logger

        l.msg("Converting grah to tree")
        resulting_tree = tree_type(l)
        if sort_rules:
            self.sort_graph_nodes(starting_nodes, sort_rules)
        for snode in starting_nodes:
            assert isinstance(snode, graph_node_type), "Node is of wrong type"
            l.msg("Processing node %s" % (self.__data_to_string(snode.data)))
            # Build down provided starting nodes treating them as root nodes for generated tree
            snode_tree = self.build_down(snode, datagraph, rules, sort_rules)
            resulting_tree.addRootSubtree(snode_tree)

        # Adding nodes that are unconnected with starting one to a separate tree root node
        # Separate root node might already be part of complex, so searching for it
        root_for_not_processed = resulting_tree.find_node_by_data(graph_root_for_not_processed_data)
        if root_for_not_processed == None:
            root_for_not_processed = tree_node_type(graph_root_for_not_processed_data)
            resulting_tree.add_root_node(root_for_not_processed)
        self.processnotprocessed_simpleflat(datagraph, resulting_tree, root_for_not_processed)

        l.msg("Grah to tree convertion finished")
        return resulting_tree


    # Starting from parentnode walks through complex building tree according to provided rules
    def build_down(self, parent_graph_node, graph, rules, sort_rules):
        l = self.__logger

        assert isinstance(parent_graph_node, graph_node_type), "Node is of wrong type"
        assert isinstance(graph, graph_type), "Graph is of wrong type"
        l.msg("Building subtree for root node %s" % self.__data_to_string(parent_graph_node.data))

        # Resulting tree
        tree = tree_type(l)

        parent_tree_node = tree_node_type(parent_graph_node.data)
        tree.add_root_node(parent_tree_node)

        # Walking a complex to form a tree level by level with a non recursive algorithm
        # Warning: Currently non cycle-safe (if nodes are linked in a "cycle" A-B-C-A - algorithm will loop infinetely
        current_nodes_level_map = {}
        current_nodes_level_map[parent_tree_node] = parent_graph_node
        while len(current_nodes_level_map) > 0:
            next_nodes_level_map = {}
            for current_tree_node, current_graph_node in current_nodes_level_map.items():
                l.msg("Searching for children for node %s" % self.__data_to_string(current_graph_node.data))
                current_graph_node_children = self.getchildrenbyrules(current_graph_node,rules)
                if sort_rules:
                    self.sort_graph_nodes(current_graph_node_children, sort_rules)
                current_graph_node_new_children_map = self.convert_graph2tree_nodes( current_graph_node_children )
                current_tree_node.add_children( current_graph_node_new_children_map.keys() )
                next_nodes_level_map.update(current_graph_node_new_children_map)
            current_nodes_level_map = next_nodes_level_map

        return tree


    def convert_graph2tree_nodes (self, graph_nodes):
        tree_nodes_map = {}
        for n in graph_nodes:
            assert isinstance(n, graph_node_type), "Node is of wrong type"
            # Inversing sotrage, as complex node can appear several times in the same tree, but tree node shall be always new
            tree_nodes_map[tree_node_type(n.data)] = n
        return tree_nodes_map


    def getchildrenbyrules(self, currentnode, rules):
        assert isinstance(currentnode, graph_node_type), "Node is of wrong type"
        assert isinstance(rules, conversionrules), "Rules are of wrong type"
        l = self.__logger

        children = []
        for rule in rules.list:
            if rule.type == 'link':
                outward_direction = True # TODO: Now supporting only outward
                link_children = currentnode.get_linked_nodes(rule.name,outward_direction)
                # Appending children without overwriting to keep order
                for ch in link_children:
                    if ch not in children:
                        children.append(ch)
            else:
                pass # TODO: Implement other rule types - like Epic task

        return children

    def sort_graph_nodes(self, nodes, sort_rules):
        assert isinstance(nodes, list), "Node is of wrong type"
        l = self.__logger
        for field, sort_type in sort_rules.items():
            nodes.sort(
                key=lambda node: self.__value_by_field(node.data, field),
                reverse=True if sort_type == 'desc' else False)

    # Adds complex nodes that didn't get to the tree yet to a newly created tree node in a flat structure
    def processnotprocessed_simpleflat(self, graph, tree, notprocessed_root_tree_node):
        assert isinstance(graph, graph_type), "Graph is of wrong type"
        assert isinstance(tree, tree_type), "Tree are of wrong type"

        sub_tree = tree_type(self.__logger)

        for graphnode in graph.nodes:
            if not tree.contains_data( graphnode.data ):
                notprocessed_root_tree_node.add_child(tree_node_type(graphnode.data))





class conversionrules(object):

    def __init__(self):
        self.__rules = []

    def add_link_rule(self,name):
        self.__rules.append( rule('link',name) )

    @property
    def list(self):
        return self.__rules


class rule(object):

    def __init__(self, type,name):
        self.__type = type
        self.__name = name

    @property
    def type(self):
        return self.__type

    @property
    def name(self):
        return self.__name
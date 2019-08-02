import xdev.core.logger

class graph_type(object):

    def __init__(self, parent_logger):
        assert isinstance(parent_logger, xdev.core.logger.logger), "Type of node is wrong"
        self.__nodes = [] # plain list of nodes
        self.__links = {} # links[(from,to,link)] = True
        self.__logger = xdev.core.logger.logger.from_parent("GR",parent_logger)

        self.__last_added_node = None
        self.__pre_last_added_node = None


    @property
    def logger(self):
        return self.__logger

    def add_node(self,newnode):
        assert isinstance(newnode, graph_node_type), "Type of node is wrong"
        if newnode not in self.__nodes:
            self.__nodes.append(newnode)
            newnode.set_graph(self)
            self.__pre_last_added_node = self.__last_added_node
            self.__last_added_node = newnode
        else:
            self.__logger.msg("Node already exists")

    @property
    def last_added_node(self):
        return self.__last_added_node

    @property
    def pre_last_added_node(self):
        return self.__pre_last_added_node

    @property
    def nodes(self):
        return self.__nodes

    @property
    def outlinks(self):
        return self.__links

    @property
    def inlinks(self):
        return self.__links

    def add_link(self,from_node,to_node,new_link):
        assert isinstance(from_node, graph_node_type), "Type of from node is wrong"
        assert isinstance(to_node, graph_node_type), "Type of to node is wrong"
        assert isinstance(new_link, graph_link_type), "Type of link is wrong"

        if from_node not in self.__nodes:
            self.__logger.warning("From node not found trying to add link")
        elif to_node not in self.__nodes:
            self.__logger.warning("To node not found trying to add link")
        else:
            if not self.has_link(from_node,to_node,new_link):
                # Warning: Currently it is possible to add the same link (by meaning) twice
                self.__links[(from_node,to_node,new_link)] = True
            else:
                self.__logger.msg("Link already exists")

    # Returns links and linked nodes where focus_node is on either one or another end (depdencing on outward)
    # @outward Bool if only outward connections have to be searched (True), inward (False)
    def get_links_for_node(self,focus_node,link_name = None, outward = True):
        assert outward == True or outward == False, "link direction shall be specified"
        links = {}
        if outward == True:
            for trip in self.__links.keys():
                (from_node,to_node,link) = trip
                if from_node == focus_node and link_name == link.name:
                    links[to_node] = link
        elif outward == False:
            for trip in self.__links.keys():
                (from_node, to_node, link) = trip
                if to_node == focus_node and link_name == link.name:
                    links[from_node] = link
        return  links

    def has_link(self,from_node,to_node,new_link):
        assert isinstance(from_node, graph_node_type), "Type of from node is wrong"
        assert isinstance(to_node, graph_node_type), "Type of to node is wrong"
        assert isinstance(new_link, graph_link_type), "Type of link is wrong"

        return (from_node,to_node,new_link) in self.__links.keys()


class graph_node_type(object):

    def __init__(self, data, logger):
        assert isinstance(logger, xdev.core.logger.logger), "Type of link has to be of string type"
        self.__data = data
        self.__graph = None
        self.__logger = logger

    @property
    def data(self):
        return self.__data

    # Provides reference to a complex that node currently is in and starts using its logger
    def set_graph(self,graph):
        assert isinstance(graph, graph_type), "Type of complex is wrong"
        self.__graph = graph
        self.__logger = graph.logger

    # Returns linked nodes
    # @outward Bool if only outward connections have to be searched (True), inward (False)
    def get_linked_nodes(self,link_name,outward = True):
        if self.__graph != None:
            links = self.__graph.get_links_for_node(self,link_name,outward)
            return links.keys()
        else:
            self.__logger.warning("Cannot find linked notes as complex for node is not set")
            return None


class graph_link_type(object):

    def __init__(self,name,link_extra_data = None):
        assert isinstance(name, str), "Type of link has to be of string type"
        self.__type = type
        self.__name = name
        self.__extra_data = link_extra_data

    @property
    def name(self):
        return self.__name

    @property
    def extra_data(self):
        return self.__extra_data
from dataTypes import *

SEPARATOR = ' '


class Parser:

    def openFile(self, file_name):
        network = Network()

        with open(file_name) as file:
            number_of_links = int(file.readline())

            for _ in range(number_of_links):
                link_array = file.readline().strip().split(SEPARATOR)
                network.links.append(Link(link_array))

            file.readline()
            file.readline()

            number_of_demands = int(file.readline())

            file.readline()

            for demand_id in range(number_of_demands):
                demand_node_info = file.readline().strip().split(SEPARATOR)
                number_of_demand_paths = int(file.readline())

                demand = Demand(demand_node_info, demand_id + 1)

                for _ in range(number_of_demand_paths):
                    demand_path_info = file.readline().strip().split(SEPARATOR)
                    demand_path = DemandPath(demand_path_info)
                    demand.demand_paths.append(demand_path)

                file.readline()
                network.demands.append(demand)

        return network

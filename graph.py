class Graph:
    def __init__(self, links, demands):
        self._links= links
        self._demands = demands

    def is_path_correct(self, path):
        for i in range(len(path) - 1):
            next_vertices = []
            for link in self._links:
                if link[0].text == path[i]:
                    next_vertices.append(link[1].text)
                elif link[1].text == path[i]:
                    next_vertices.append(link[0].text)

            if path[i+1] not in next_vertices:
                return False

        return True


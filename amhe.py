import xml.etree.ElementTree as ET
from graph import Graph


def load_data(graph_path, demands_path):
    links = load_xml(graph_path)
    demands = load_txt(demands_path)
    return Graph(links, demands)

def load_xml(graph_path):
    graph = ET.parse(graph_path)
    return graph.getroot()[0][0]

def load_txt(demands_path):
    with open(demands_path) as f:
        content = f.readlines()
        content = [x.strip() for x in content]

        return dict((v.split(',')) for v in content)


g = load_data("D:\Tomek\PW-informatyka\Magisterka\SEM2\AMHE\projekt\przykladowe_dane\gen_50_d_2.xml", "D:\Tomek\PW-informatyka\Magisterka\SEM2\AMHE\projekt\przykladowe_dane\gen_50_d_2_0_4_1.txt")
for link in g._links:
    print(link[0].text, link[1].text)

print(g.is_path_correct(['N1', 'N2', 'N3']))
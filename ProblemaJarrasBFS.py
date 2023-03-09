
from collections import deque
import matplotlib.pyplot as plt
import networkx as nx

def build_graph():
    graph = {}
    for i in range(5):
        for j in range(4):
            node = (i, j)
            neighbors = set()
            if i < 4:
                neighbors.add((4, j))
            if i > 0:
                neighbors.add((0, j))
            if j < 3:
                neighbors.add((i, 3))
            if j > 0:
                neighbors.add((i, 0))
            if i+j <= 4:
                neighbors.add((i+j, 0))
            else:
                neighbors.add((4, i+j-4))
            if i+j <= 3:
                neighbors.add((0, i+j))
            else:
                neighbors.add((i+j-3, 3))
            graph[node] = neighbors
    return graph

def bfs(graph, start, goal):
    queue = deque([(start, [start])])
    visited = set([start])
    while queue:
        node, path = queue.popleft()
        if node == goal:
            return path
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return None

# Construir el grafo
graph = build_graph()

# Convertir el grafo en dirigido
digraph = {}
for node, neighbors in graph.items():
    for neighbor in neighbors:
        if node not in digraph:
            digraph[node] = set()
        digraph[node].add(neighbor)

# Encontrar el camino más corto
start = (0, 0)
goal = (2, 0)
path = bfs(digraph, start, goal)
print("Camino más corto:", path)

# Crear un grafo de NetworkX
G = nx.DiGraph()
for node, neighbors in digraph.items():
    G.add_node(node)
    for neighbor in neighbors:
        G.add_edge(node, neighbor)

# Generar el layout utilizando el algoritmo "spring_layout"
pos = nx.spring_layout(G)

# Graficar el grafo y el camino más corto
fig, ax = plt.subplots(figsize=(8, 8))

# Dibujar los nodos
# Dibujar los nodos
for node in digraph:
    x, y = pos[node]
    # Si el nodo es el nodo inicial o final, cambiar el color del borde y relleno
    if node == start or node == goal:
        ax.scatter(x, y, s=500, color='yellow', edgecolors='white', linewidths=2, zorder=4)
    else:
        ax.scatter(x, y, s=500, color='lightblue', edgecolors='gray', linewidths=1, zorder=2)
    # Si el nodo es el nodo inicial o final, cambiar el color del texto a blanco
    if node == start or node == goal:
        ax.annotate(f'({node[0]}, {node[1]})', (x, y), fontsize=12, ha='center', va='center', color='black', zorder=5)
    else:
        ax.annotate(f'({node[0]}, {node[1]})', (x, y), fontsize=12, ha='center', va='center', zorder=3)

# Dibujar las aristas
for node, neighbors in digraph.items():
    for neighbor in neighbors:
        x1, y1 = pos[node]
        x2, y2 = pos[neighbor]
        dx = x2 - x1
        dy = y2 - y1
        ax.quiver(x1, y1, dx, dy, angles='xy', scale_units='xy', scale=1, width=0.0029, color='gray', zorder=1)
# Resaltar el camino más corto
for i in range(len(path)-1):
    node1 = path[i]
    node2 = path[i+1]
    x1, y1 = pos[node1]
    x2, y2 = pos[node2]
    dx = x2 - x1
    dy = y2 - y1
    ax.quiver(x1, y1, dx, dy, angles='xy', scale_units='xy', scale=1, width=0.01, color='red', zorder=3)
# Asignar distancias a cada nodo
distances = {}
for node in digraph:
    if node == start:
        distances[node] = 0
    else:
        distances[node] = float('inf')

# Aplicar el algoritmo de Dijkstra
visited = set()
queue = [(start, 0)]
while queue:
    node, dist = min(queue, key=lambda x: x[1])
    queue.remove((node, dist))
    visited.add(node)
    for neighbor in digraph[node]:
        if neighbor not in visited:
            alt = dist + 1
            if alt < distances[neighbor]:
                distances[neighbor] = alt
                queue.append((neighbor, alt))

# Dibujar las etiquetas de las distancias
for node in digraph:
    x, y = pos[node]
    if node in path:
        ax.text(x, y+0.1, f'{distances[node]}', fontsize=12, fontweight='bold', ha='center', va='bottom', color='white', bbox=dict(facecolor='blue', edgecolor='none', pad=0.3))


fig.suptitle('Grafo con camino más corto resaltado (BFS)', fontsize=16)

plt.show()


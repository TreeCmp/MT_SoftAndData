import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx

# Tworzymy graf
G = nx.Graph()

# Dodajemy główne wierzchołki
G.add_node('u')
G.add_node('v')

# Poddrzewa jako "wirtualne" węzły do rysowania krawędzi
G.add_node('A')
G.add_node('B')
G.add_node('C')
G.add_node('D')

# Łączymy wierzchołki
G.add_edge('u', 'v')
G.add_edge('v', 'A')
G.add_edge('u', 'B')
G.add_edge('v', 'C')
G.add_edge('u', 'D')

# Pozycje
pos = {
    'u': (1, 0),
    'v': (0, 0),
    'A': (-0.5, 0),
    'B': (1.5, 0),
    'C': (0, -0.5),
    'D': (1, -0.5)
}

# Rysujemy krawędzie
nx.draw_networkx_edges(G, pos)

# Rysujemy główne wierzchołki
nx.draw_networkx_nodes(G, pos, nodelist=['u', 'v'], node_color='black', node_size=100)

# Rysujemy poddrzewa jako trójkąty
ax = plt.gca()
x, y = pos['A']
triangle = mpatches.Polygon([
    (x, y),
    (x - 1, y + 0.3),
    (x - 1, y - 0.3)
], closed=True, fill=True, facecolor='white', edgecolor='black')
ax.add_patch(triangle)

x, y = pos['B']
triangle = mpatches.Polygon([
    (x, y),
    (x + 1, y + 0.3),
    (x + 1, y - 0.3)
], closed=True, fill=True, facecolor='white', edgecolor='black' )
ax.add_patch(triangle)

subtree_pos = ['C', 'D']
for node in subtree_pos:
    x, y = pos[node]
    triangle = mpatches.Polygon([
        (x, y),
        (x - 0.3, y - 1),
        (x + 0.3, y - 1)
    ], closed=True, fill=True, facecolor='white', edgecolor='black')
    ax.add_patch(triangle)

# Dodajemy etykiety dla u i v
for node in ['u', 'v']:
    x, y = pos[node]
    plt.text(x, y + 0.1, node, fontsize=12, ha='center')

# Dodajemy etykiety dla poddrzew
x, y = pos['A']
plt.text(x - 0.4, y, 'A', fontsize=10, ha='center')
x, y = pos['B']
plt.text(x + 0.4, y, 'B', fontsize=10, ha='center')
for node in ['C', 'D']:
    x, y = pos[node]
    plt.text(x, y - 0.4, node, fontsize=10, ha='center')

# Dodajemy strzałkę o dwóch grotach między C i D (nie stykającą się z trójkątami)
xC, yC = pos['C']
xD, yD = pos['D']

# Obliczamy przesunięcie by strzałka nie dochodziła do środka trójkątów
offset = 0.1
dx = xD - xC
dy = yD - yC
length = (dx**2 + dy**2)**0.5
ux = dx / length
uy = dy / length

# Punkt startu i końca strzałki (odsunięte od trójkątów)
start = (xC + offset * ux, yC + offset * uy)
end = (xD - offset * ux, yD - offset * uy)

# Rysujemy grubą szarą strzałkę z dwoma grotami
arrow = mpatches.FancyArrowPatch(
    start, end,
    arrowstyle='<->',
    color='black',
    mutation_scale=20,  # większe groty
    linewidth=5         # grubsza linia
)
ax.add_patch(arrow)

# Ustawiamy proporcje i limity osi
ax.set_aspect('equal')
ax.set_xlim(-2, 3)
ax.set_ylim(-2, 0.5)
plt.axis('off')
# plt.title("")

# Usuwamy marginesy
plt.tight_layout(pad=0)
plt.savefig('figdMTuNNI.png', bbox_inches='tight')
plt.show()

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx

# Tworzymy graf
G = nx.Graph()

# Dodajemy główne wierzchołki
G.add_node('n')
G.add_node('n_2')
G.add_node('v')
G.add_node('u')
G.add_node('w')


# Poddrzewa jako "wirtualne" węzły do rysowania krawędzi
G.add_node('v')
G.add_node('u')
G.add_node('w')

# Łączymy wierzchołki
G.add_edge('n', 'n_2')
G.add_edge('v', 'u')
G.add_edge('v', 'w')

# Pozycje
pos = {
    'n': (3, 1),
    'n_2': (3, 0),
    'v': (3, -2),
    'u': (1.8, -3),
    'w': (4.2, -3),
}

# Rysujemy poddrzewa jako trójkąty
ax = plt.gca()

def draw_triangle(pos, x_marg, y_marg, labels=None):
    x, y = pos  # rozpakowanie tuple (x, y)
    # współrzędne trójkąta
    top = (x, y)
    left = (x - x_marg, y - y_marg)
    right = (x + x_marg, y - y_marg)

    # rysowanie trójkąta
    triangle = mpatches.Polygon([top, left, right],
                                closed=True, fill=True,
                                facecolor='white', edgecolor='black')
    ax.add_patch(triangle)

    # jeżeli podano etykiety, dodajemy je
    if labels:
        if len(labels) >= 1:
            plt.text(left[0], left[1] - 0.3, labels[0], fontsize=12, ha='center')
        if len(labels) >= 2:
            plt.text(right[0], right[1] - 0.3, labels[1], fontsize=12, ha='center')

draw_triangle(pos['n_2'], 4, 5, labels=["1", "n-1"])
draw_triangle(pos['u'], 0.9, 2, labels=["a", "b"])
draw_triangle(pos['w'], 0.9, 2, labels=["b+1", "d"])

# Rysujemy krawędzie
nx.draw_networkx_edges(G, pos)

nodelist=['n','v','u','w']

# Rysujemy główne wierzchołki
nx.draw_networkx_nodes(G, pos, nodelist, node_color='black', node_size=100)

# Dodajemy etykiety dla u i v
for node in nodelist:
    x, y = pos[node]
    plt.text(x, y + 0.3, node, fontsize=12, ha='center')

# Usuwamy marginesy
plt.tight_layout(pad=0)

# współrzędne rogów największego trójkąta
x, y = pos['n_2']
left_corner = (x - 4, y - 7)
right_corner = (x + 4, y - 7)

plt.axis("off")

# Usuwamy marginesy
plt.tight_layout(pad=0)
plt.savefig('figDiam.png', bbox_inches='tight')
plt.show()

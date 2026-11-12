import networkx as nx
import matplotlib.pyplot as plt

# Tworzenie grafu
G = nx.Graph()
G.add_edges_from([
    ('x', 'a'),
    ('x', 'b'),
    ('x', 'y'),
    ('y', 'c'),
    ('z', 'd'),
    ('z', 'e'),
    ('y', 'z')
])

# Ręczne ustawienie współrzędnych
pos = {
    'a': (-2, 1),
    'b': (-2, -1),
    'x': (-1, 0),
    'c': (0, 1),
    'y': (0, 0),
    'z': (1, 0),
    'd': (2, 1),
    'e': (2, -1)
}

# Rysowanie wierzchołków i krawędzi bez etykiet
plt.figure(figsize=(8, 6))
nx.draw(
    G, pos=pos, with_labels=False, node_color='black', node_size=100
)

# Rysowanie etykiet obok wierzchołków (np. trochę na prawo i do góry)
offset_pos = {k: (v[0] + 0.1, v[1] + 0.05) for k, v in pos.items()}
labels_to_draw = {k: k for k in G.nodes if k not in ('x', 'y', 'z')}
nx.draw_networkx_labels(G, pos=offset_pos, labels=labels_to_draw,
                        font_color='black', font_size=12)

plt.text(-0.5, 0.2, r"$T_1$", fontsize=14, ha='center')
plt.title("Figure 1", fontsize=18)
plt.tight_layout()
plt.show()

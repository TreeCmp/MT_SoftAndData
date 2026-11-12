import matplotlib.pyplot as plt
import networkx as nx

# --- T 1 ---
G1 = nx.Graph()
G1.add_edges_from([
    ('x', 'a'),
    ('x', 'b'),
    ('x', 'y'),
    ('y', 'c'),
    ('z', 'd'),
    ('z', 'e'),
    ('y', 'z')
])
pos1 = {
    'a': (-2, 1),
    'b': (-2, -1),
    'x': (-1, 0),
    'c': (0, 1),
    'y': (0, 0),
    'z': (1, 0),
    'd': (2, 1),
    'e': (2, -1)
}

# --- T 2 ---
G2 = nx.Graph()
G2.add_edges_from([
    ('x', 'a'),
    ('x', 'b'),
    ('y', 'c'),
    ('y', 'd'),
    ('y', 'e'),
    ('x', 'y')
])
pos2 = {
    'a': (-2, 1),
    'b': (-2, -1),
    'x': (-1, 0),
    'y': (0, 0),
    'c': (1, 1),
    'd': (1, 0),
    'e': (1, -1)
}

# --- Tworzenie subplotów ---
fig, axs = plt.subplots(1, 2, figsize=(12, 6))

# Lewy subplot: G1
nx.draw(G1, pos=pos1, with_labels=False, node_color='black', node_size=100, ax=axs[0])
offset_pos1 = {k: (v[0] + 0.1, v[1] + 0.05) for k, v in pos1.items()}
labels1 = {k: k for k in G1.nodes if k not in ('x', 'y', 'z')}
nx.draw_networkx_labels(G1, pos=offset_pos1, labels=labels1, font_color='black', font_size=12, ax=axs[0])
axs[0].set_title(r"$T_1$", fontsize=18)
axs[0].axis('off')

# Prawy subplot: G2
nx.draw(G2, pos=pos2, with_labels=False, node_color='black', node_size=100, ax=axs[1])
offset_pos2 = {k: (v[0] + 0.1, v[1] + 0.05) for k, v in pos2.items()}
labels2 = {k: k for k in G2.nodes if k not in ('x', 'y')}
nx.draw_networkx_labels(G2, pos=offset_pos2, labels=labels2, font_color='black', font_size=12, ax=axs[1])
axs[1].set_title(r"$T_2$", fontsize=18)
axs[1].axis('off')

plt.tight_layout()
plt.show()

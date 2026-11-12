import matplotlib.pyplot as plt
import networkx as nx

# --- Graf 1 ---
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

T1_labels = {
    'a': 'a',
    'b': 'b',
    'c': 'c',
    'd': 'd',
    'e': 'e',
    'x': r'$u_1$',
    'y': r'$u_2$',
    'z': r'$u_3$'
}

# --- Graf 2 ---
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

T2_labels = {
    'a': 'a',
    'b': 'b',
    'c': 'c',
    'd': 'd',
    'e': 'e',
    'x': r'$v_1$',
    'y': r'$v_2$'
}

# --- Trzeci graf ---
G3 = nx.Graph()

edge_labels = {
    ('a', 'd'): 0,
    ('a', 'e'): 10,
    ('a', 'f'): 3,
    ('b', 'd'): 7,
    ('b', 'e'): 3,
    ('b', 'f'): 4,
    ('c', 'd'): 3,
    ('c', 'e'): 4,
    ('c', 'f'): 3
}
G3.add_edges_from(edge_labels)

lab = {
    'a': '$u_1$={{a,b,c},{a,b,d},{a,b,e}}',
    'b': '$u_2$={{a,c,d},{a,c,e},{b,c,d},{b,c,e}}',
    'c': '$u_3$={{a,d,e},{b,d,e},{c,d,e}}',
    'd': '$v_1$={{a,b,c},{a,b,d},{a,b,e}}',
    'e': '$v_2$={{a,c,d},{a,c,e},{a,d,e},\n{b,c,d},{b,c,e},{b,d,e},{c,d,e}}',
    'f': 'O=∅'
}

pos3 = {
    'a': (-1, 1),
    'b': (-1, 0),
    'c': (-1, -1),
    'd': (1, 1),
    'e': (1, 0),
    'f': (1, -1)
}

# --- Ustawienia subplotów ---
fig = plt.figure(figsize=(30, 6))

import matplotlib.gridspec as gridspec
# GridSpec do 2 rzędów: górny (2 kolumny), dolny (1 kolumna)
#gs = gridspec.GridSpec(2, 2, height_ratios=[3, 2])
# ax1 = fig.add_subplot(gs[0, 0])  # lewy górny
# ax2 = fig.add_subplot(gs[0, 1])  # prawy górny
# ax3 = fig.add_subplot(gs[1, :])  # dolny, zajmuje 2 kolumny

# GridSpec do 1 rzędu: i 4 kolumn
gs = gridspec.GridSpec(1, 4)


ax1 = fig.add_subplot(gs[0, 0])  # lewy
ax2 = fig.add_subplot(gs[0, 3])  # prawy
ax3 = fig.add_subplot(gs[0, 1:3])  # środkowy

# --- Rysowanie G1 ---
nx.draw(G1, pos=pos1, with_labels=False, node_color='black', node_size=100, ax=ax1)
offset_pos1 = {k: (v[0] + 0.1, v[1] + 0.05) for k, v in pos1.items()}
nx.draw_networkx_labels(G1, pos=offset_pos1, labels=T1_labels, font_color='black', font_size=26, ax=ax1)
ax1.set_title(r"$T_1$", fontsize=30)
ax1.axis('off')

# --- Rysowanie G2 ---
nx.draw(G2, pos=pos2, with_labels=False, node_color='black', node_size=100, ax=ax2)
offset_pos2 = {k: (v[0] + 0.1, v[1] + 0.05) for k, v in pos2.items()}
nx.draw_networkx_labels(G2, pos=offset_pos2, labels=T2_labels, font_color='black', font_size=26, ax=ax2)
ax2.set_title(r"$T_2$", fontsize=30)
ax2.axis('off')

# --- Rysowanie G3 ---
nx.draw_networkx_nodes(G3, pos=pos3, node_color='black', node_size=100, ax=ax3)

matching = [('a', 'd'), ('b', 'e'), ('c', 'f')]
normal_edges = [e for e in G3.edges() if e not in matching and (e[1], e[0]) not in matching]
nx.draw_networkx_edges(G3, pos=pos3, edgelist=normal_edges, width=1, edge_color='black', ax=ax3)
nx.draw_networkx_edges(G3, pos=pos3, edgelist=matching, width=3, edge_color='black', ax=ax3)

for (u, v), lbl in edge_labels.items():
    x0, y0 = pos3[u]
    x1, y1 = pos3[v]
    xm = (x0 + x1) / 2
    ym = (y0 + y1) / 2

    # przesunięcia etykiet krawędzi
    if (u, v) == ('a', 'e') or (v, u) == ('a', 'e'):
        dx, dy = -0.1, 0.11
    elif (u, v) == ('a', 'f') or (v, u) == ('a', 'f'):
        dx, dy = -0.11, 0.14
    elif (u, v) == ('b', 'd') or (v, u) == ('b', 'd'):
        dx, dy = 0.11, 0.11
    elif (u, v) == ('b', 'f') or (v, u) == ('b', 'f'):
        dx, dy = -0.11, 0.11
    elif (u, v) == ('c', 'd') or (v, u) == ('c', 'd'):
        dx, dy = 0.08, 0.14
    elif (u, v) == ('c', 'e') or (v, u) == ('c', 'e'):
        dx, dy = 0.11, 0.11
    else:
        dx, dy = -0.02, 0.05

    ax3.text(xm + dx, ym + dy, str(lbl),
             fontsize=26, color='black',
             bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.1'))

offset_pos3 = {
    k: (v[0] + 0.05 if v[0] < 0 else v[0] + 0.0, v[1] + 0.3)
    for k, v in pos3.items()
}
nx.draw_networkx_labels(G3, pos=offset_pos3, labels=lab,
                        font_color='black', font_size=26,
                        bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.2'),
                        ax=ax3)

ax3.set_xlim(-1.74, 1.68)
ax3.set_ylim(-1.2, 1.4)
ax3.axis('off')
plt.tight_layout()
plt.savefig('T1_T2_matching_hor.png', bbox_inches='tight')
plt.show()
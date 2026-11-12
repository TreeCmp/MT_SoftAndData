import matplotlib.pyplot as plt
import networkx as nx

# --- Graf GA ---
GA = nx.Graph()
GA.add_nodes_from(['1', '2', '3', '4', 'i', 'n-3', 'n-2', 'n-1', 'n',
                   '$a_2$', '$a_3$', '$a_4$', '$a_i$', '$a_{n-3}$', '$a_{n-2}$', '$a_{n-1}$'])
GA.add_edges_from([
    ('1', '$a_2$'), ('2', '$a_2$'), ('3', '$a_3$'), ('4', '$a_4$'), ('i', '$a_i$'),
    ('n-3', '$a_{n-3}$'), ('n-2', '$a_{n-2}$'), ('n-1', '$a_{n-1}$'), ('n', '$a_{n-1}$'),
    ('$a_2$', '$a_3$'), ('$a_3$', '$a_4$'), ('$a_4$', '$a_i$'), ('$a_i$', '$a_{n-3}$'),
    ('$a_{n-3}$', '$a_{n-2}$'), ('$a_{n-2}$', '$a_{n-1}$')
])
posA = {
    '1': (-4.5, 2), '2': (-4.5, 0), '3': (-3, 0), '4': (-2, 0), 'i': (0, 0),
    'n-3': (2, 0), 'n-2': (3, 0), 'n-1': (4.5, 0), 'n': (4.5, 2),
    '$a_2$': (-4, 1), '$a_3$': (-3, 1), '$a_4$': (-2, 1), '$a_i$': (0, 1),
    '$a_{n-3}$': (2, 1), '$a_{n-2}$': (3, 1), '$a_{n-1}$': (4, 1),
}

# --- Graf GB ---
GB = nx.Graph()
GB.add_nodes_from(['1', 'n', '2', '3', 'j', 'n-4', 'n-3', 'n-2', 'n-1',
                   '$b_1$', '$b_2$', '$b_3$', '$b_j$', '$b_{n-4}$', '$b_{n-3}$', '$b_{n-2}$'])
GB.add_edges_from([
    ('1', '$b_1$'), ('n', '$b_1$'), ('2', '$b_2$'), ('3', '$b_3$'), ('j', '$b_j$'),
    ('n-4', '$b_{n-4}$'), ('n-3', '$b_{n-3}$'), ('n-2', '$b_{n-2}$'), ('n-1', '$b_{n-2}$'),
    ('$b_1$', '$b_2$'), ('$b_2$', '$b_3$'), ('$b_3$', '$b_j$'), ('$b_j$', '$b_{n-4}$'),
    ('$b_{n-4}$', '$b_{n-3}$'), ('$b_{n-3}$', '$b_{n-2}$')
])
posB = {
    '1': (-4.5, -1), 'n': (-4.5, -3), '2': (-3, -3), '3': (-2, -3), 'j': (0, -3),
    'n-4': (2, -3), 'n-3': (3, -3), 'n-2': (4.5, -3), 'n-1': (4.5, -1),
    '$b_1$': (-4, -2), '$b_2$': (-3, -2), '$b_3$': (-2, -2), '$b_j$': (0, -2),
    '$b_{n-4}$': (2, -2), '$b_{n-3}$': (3, -2), '$b_{n-2}$': (4, -2),
}

# --- Rysowanie ---
plt.figure(figsize=(12, 8))

# Lista przerywanych krawędzi
dashed_edges = [
    ('$a_4$', '$a_i$'),
    ('$a_i$', '$a_{n-3}$'),
    ('$b_3$', '$b_j$'),
    ('$b_j$', '$Bb_{n-4}$')
]

# Rysujemy wierzchołki
nx.draw_networkx_nodes(GA, posA, node_color='black', node_size=100)

nx.draw_networkx_nodes(GB, posB, node_color='black', node_size=100)

# Krawędzie z GA bez przerywanych
nx.draw_networkx_edges(GA, posA, edgelist=[e for e in GA.edges if e not in dashed_edges and e[::-1] not in dashed_edges])

# Krawędzie z GB bez przerywanych
nx.draw_networkx_edges(GB, posB, edgelist=[e for e in GB.edges if e not in dashed_edges and e[::-1] not in dashed_edges])

# Rysujemy przerywane krawędzie osobno
for u, v in dashed_edges:
    if u in posA and v in posA:
        x = [posA[u][0], posA[v][0]]
        y = [posA[u][1], posA[v][1]]
    elif u in posB and v in posB:
        x = [posB[u][0], posB[v][0]]
        y = [posB[u][1], posB[v][1]]
    else:
        continue  # pomiń jeśli pozycje nie istnieją
    plt.plot(x, y, linestyle='--', color='black', linewidth=2)


# Przesunięcie etykiet
def draw_labels_shifted(G, pos, dx=0.2, dy=0.15):
    shifted_pos = {k: (x + dx, y + dy) for k, (x, y) in pos.items()}
    nx.draw_networkx_labels(G, shifted_pos, font_size=18)

draw_labels_shifted(GA, posA)
draw_labels_shifted(GB, posB)

# Dodajemy etykiety T1 i T2
plt.text(-5.2, 2.3, r"$T_1$", fontsize=22, fontweight='bold')  # etykieta dla górnego drzewa
plt.text(-5.2, -0.7, r"$T_2$", fontsize=22, fontweight='bold') # etykieta dla dolnego drzewa


# Finalne wykończenie
plt.axis('off')
plt.tight_layout()
plt.savefig('figAddLeafCater.png', bbox_inches='tight')
plt.show()



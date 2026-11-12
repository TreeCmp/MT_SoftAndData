import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx

# Tworzymy graf
G = nx.Graph()

# Dodajemy główne wierzchołki
G.add_node('u')
G.add_node('v')

# Poddrzewa jako "wirtualne" węzły do rysowania krawędzi
G.add_node('$A_1$')
G.add_node('$A_2$')
G.add_node('$A_a$')
G.add_node('$B_1$')
G.add_node('$B_2$')
G.add_node('$B_b$')

# Łączymy wierzchołki
G.add_edge('u', 'v')
G.add_edge('v', '$A_1$')
G.add_edge('v', '$A_2$')
G.add_edge('v', '$A_a$')
G.add_edge('u', '$B_1$')
G.add_edge('u', '$B_2$')
G.add_edge('u', '$B_b$')

# Pozycje
pos = {
    'u': (1, 0),
    'v': (0, 0),
    '$A_1$': (-1, 1),
    '$A_2$': (-1, 0),
    '$A_a$': (-1, -1.5),
    '$B_1$': (2, 1),
    '$B_2$': (2, 0),
    '$B_b$': (2, -1.5)
}

# Rysujemy krawędzie
nx.draw_networkx_edges(G, pos)

# Rysujemy główne wierzchołki
nx.draw_networkx_nodes(G, pos, nodelist=['u', 'v'], node_color='black', node_size=100)

# Rysujemy poddrzewa jako trójkąty
ax = plt.gca()

subtree_A_pos = ['$A_1$','$A_2$', '$A_a$']
for node in subtree_A_pos:
    x, y = pos[node]
    triangle = mpatches.Polygon([
        (x, y),
        (x - 1, y + 0.3),
        (x - 1, y - 0.3)
    ], closed=True, fill=True, facecolor='white', edgecolor='black')
    ax.add_patch(triangle)

subtree_B_pos = ['$B_1$','$B_2$', '$B_b$']
for node in subtree_B_pos:
    x, y = pos[node]
    triangle = mpatches.Polygon([
        (x, y),
        (x + 1, y + 0.3),
        (x + 1, y - 0.3)
    ], closed=True, fill=True, facecolor='white', edgecolor='black')
    ax.add_patch(triangle)


# Dodajemy etykiety dla u i v
for node in ['u', 'v']:
    x, y = pos[node]
    plt.text(x, y + 0.1, node, fontsize=12, ha='center')

# Dodajemy etykiety dla poddrzew
for node in subtree_A_pos:
    x, y = pos[node]
    plt.text(x - 0.6, y, node, fontsize=12, ha='center')
for node in subtree_B_pos:
    x, y = pos[node]
    plt.text(x + 0.4, y, node, fontsize=12, ha='center')

# Dodaj pionowe trzy kropki pomiędzy $A_2$ a $A_a$
x_A, y_A_top = pos['$A_2$']
_, y_A_bot = pos['$A_a$']
x_dots_A = x_A - 0.4  # żeby było na linii z etykietami A

ys_A = [y_A_top - 0.25 - i * (y_A_top - y_A_bot)/6 for i in [1, 2, 3]]
for y in ys_A:
    ax.text(x_dots_A, y, '•', fontsize=16, ha='center', va='center')

# Dodaj pionowe trzy kropki pomiędzy $B_2$ a $B_b$
x_B, y_B_top = pos['$B_2$']
_, y_B_bot = pos['$B_b$']
x_dots_B = x_B + 0.4  # żeby było na linii z etykietami B

ys_B = [y_B_top - 0.25 - i * (y_B_top - y_B_bot)/6 for i in [1, 2, 3]]
for y in ys_B:
    ax.text(x_dots_B, y, '•', fontsize=16, ha='center', va='center')

# Dodajemy strzałkę między C i D (nie stykającą się z trójkątami)
xC, yC = pos['v']
xD, yD = pos['u']

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
    arrowstyle='<-',
    color='black',
    mutation_scale=20,  # większe groty
    linewidth=5         # grubsza linia
)
ax.add_patch(arrow)

# Ustawiamy proporcje i limity osi
ax.set_aspect('equal')
# ax.set_xlim(-2, 3)
# ax.set_ylim(-2, 0.5)
plt.axis('off')
# plt.title("")

# Usuwamy marginesy
plt.tight_layout(pad=0)
plt.savefig('figdMTShrink.png', bbox_inches='tight')
plt.show()

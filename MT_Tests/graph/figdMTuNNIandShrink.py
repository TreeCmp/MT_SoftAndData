import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx

fig, ax = plt.subplots(figsize=(6, 8))

# ==============================
# GÓRNA CZĘŚĆ (pierwszy skrypt)
# ==============================
G1 = nx.Graph()
G1.add_nodes_from(['u', 'v', 'A', 'B', 'C', 'D'])
G1.add_edges_from([
    ('u', 'v'),
    ('v', 'A'),
    ('u', 'B'),
    ('v', 'C'),
    ('u', 'D')
])
pos1 = {
    'u': (1, 0),
    'v': (0, 0),
    'A': (-0.5, 0),
    'B': (1.5, 0),
    'C': (0, -0.5),
    'D': (1, -0.5)
}

nx.draw_networkx_edges(G1, pos1, ax=ax)
nx.draw_networkx_nodes(G1, pos1, nodelist=['u', 'v'], node_color='black', node_size=100, ax=ax)

# trójkąty A, B
x, y = pos1['A']
ax.add_patch(mpatches.Polygon([(x, y), (x - 1, y + 0.3), (x - 1, y - 0.3)], closed=True, fill=True, facecolor='white', edgecolor='black'))
x, y = pos1['B']
ax.add_patch(mpatches.Polygon([(x, y), (x + 1, y + 0.3), (x + 1, y - 0.3)], closed=True, fill=True, facecolor='white', edgecolor='black'))

# trójkąty C, D
for node in ['C', 'D']:
    x, y = pos1[node]
    ax.add_patch(mpatches.Polygon([(x, y), (x - 0.3, y - 1), (x + 0.3, y - 1)], closed=True, fill=True, facecolor='white', edgecolor='black'))

# etykiety
for node in ['u', 'v']:
    x, y = pos1[node]
    ax.text(x, y + 0.1, node, fontsize=12, ha='center')
x, y = pos1['A']
ax.text(x - 0.4, y, 'A', fontsize=10, ha='center')
x, y = pos1['B']
ax.text(x + 0.4, y, 'B', fontsize=10, ha='center')
for node in ['C', 'D']:
    x, y = pos1[node]
    ax.text(x, y - 0.4, node, fontsize=10, ha='center')

# strzałka C-D
xC, yC = pos1['C']
xD, yD = pos1['D']
offset = 0.1
dx = xD - xC
dy = yD - yC
length = (dx**2 + dy**2)**0.5
ux = dx / length
uy = dy / length
start = (xC + offset * ux, yC + offset * uy)
end = (xD - offset * ux, yD - offset * uy)
ax.add_patch(mpatches.FancyArrowPatch(start, end, arrowstyle='<->', color='black', mutation_scale=20, linewidth=5))

# etykieta (a)
ax.text(-1.8, 0.5, '(a)', fontsize=14, fontweight='bold')

# ==============================
# DOLNA CZĘŚĆ (drugi skrypt)
# ==============================
y_offset = -3.2  # przesunięcie w dół

G2 = nx.Graph()
G2.add_nodes_from(['u', 'v', '$A_1$', '$A_2$', '$A_a$', '$B_1$', '$B_2$', '$B_b$'])
G2.add_edges_from([
    ('u', 'v'),
    ('v', '$A_1$'),
    ('v', '$A_2$'),
    ('v', '$A_a$'),
    ('u', '$B_1$'),
    ('u', '$B_2$'),
    ('u', '$B_b$')
])
pos2_base = {
    'u': (1, 0),
    'v': (0, 0),
    '$A_1$': (-1, 1),
    '$A_2$': (-1, 0),
    '$A_a$': (-1, -1.5),
    '$B_1$': (2, 1),
    '$B_2$': (2, 0),
    '$B_b$': (2, -1.5)
}
pos2 = {node: (x, y + y_offset) for node, (x, y) in pos2_base.items()}

nx.draw_networkx_edges(G2, pos2, ax=ax)
nx.draw_networkx_nodes(G2, pos2, nodelist=['u', 'v'], node_color='black', node_size=100, ax=ax)

# trójkąty A
for node in ['$A_1$', '$A_2$', '$A_a$']:
    x, y = pos2[node]
    ax.add_patch(mpatches.Polygon([(x, y), (x - 1, y + 0.3), (x - 1, y - 0.3)], closed=True, fill=True, facecolor='white', edgecolor='black'))

# trójkąty B
for node in ['$B_1$', '$B_2$', '$B_b$']:
    x, y = pos2[node]
    ax.add_patch(mpatches.Polygon([(x, y), (x + 1, y + 0.3), (x + 1, y - 0.3)], closed=True, fill=True, facecolor='white', edgecolor='black'))

# etykiety u, v
for node in ['u', 'v']:
    x, y = pos2[node]
    ax.text(x, y + 0.1, node, fontsize=12, ha='center')

# etykiety A i B
for node in ['$A_1$', '$A_2$', '$A_a$']:
    x, y = pos2[node]
    ax.text(x - 0.6, y, node, fontsize=12, ha='center')
for node in ['$B_1$', '$B_2$', '$B_b$']:
    x, y = pos2[node]
    ax.text(x + 0.4, y, node, fontsize=12, ha='center')

# pionowe kropki
x_A, y_A_top = pos2['$A_2$']
_, y_A_bot = pos2['$A_a$']
x_dots_A = x_A - 0.4
ys_A = [y_A_top - 0.25 - i * (y_A_top - y_A_bot) / 6 for i in [1, 2, 3]]
for y in ys_A:
    ax.text(x_dots_A, y, '•', fontsize=16, ha='center', va='center')

x_B, y_B_top = pos2['$B_2$']
_, y_B_bot = pos2['$B_b$']
x_dots_B = x_B + 0.4
ys_B = [y_B_top - 0.25 - i * (y_B_top - y_B_bot) / 6 for i in [1, 2, 3]]
for y in ys_B:
    ax.text(x_dots_B, y, '•', fontsize=16, ha='center', va='center')

# strzałka u-v w dolnym rysunku
xC, yC = pos2['v']
xD, yD = pos2['u']
dx = xD - xC
dy = yD - yC
length = (dx**2 + dy**2)**0.5
ux = dx / length
uy = dy / length
start = (xC + offset * ux, yC + offset * uy)
end = (xD - offset * ux, yD - offset * uy)
ax.add_patch(mpatches.FancyArrowPatch(start, end, arrowstyle='<-', color='black', mutation_scale=20, linewidth=5))

# etykieta (b)
ax.text(-1.8, y_offset + 1.5, '(b)', fontsize=14, fontweight='bold')

# ==============================
# Wygląd
# ==============================
ax.set_aspect('equal')
ax.axis('off')
plt.tight_layout(pad=0.05)
plt.savefig('figdMTuNNIandShrink.png', bbox_inches='tight', pad_inches=0.02)
plt.show()

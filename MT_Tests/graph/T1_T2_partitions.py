import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.gridspec as gridspec

# Włączenie renderowania LaTeX w Matplotlib z pakietem ulem do przekreśleń
plt.rcParams.update({
    "text.usetex": True,
    "text.latex.preamble": r"""
        \usepackage[normalem]{ulem}   % dla \sout
        \usepackage{amsmath}          % dla \overset
        \usepackage{amssymb}          % dla \therefore
        \newcommand{\ccc}{{\ensuremath{\overset{\therefore}{c}}}}
    """
})

# --- Grafy ---
G1 = nx.Graph()
G1.add_edges_from([('x', 'a'), ('x', 'b'), ('x', 'y'), ('y', 'c'), ('z', 'd'), ('z', 'e'), ('y', 'z')])
pos1 = {'a': (-2, 1), 'b': (-2, -1), 'x': (-1, 0), 'c': (0, 1), 'y': (0, 0), 'z': (1, 0), 'd': (2, 1), 'e': (2, -1)}
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

G2 = nx.Graph()
G2.add_edges_from([('x', 'a'), ('x', 'b'), ('y', 'c'), ('y', 'd'), ('y', 'e'), ('x', 'y')])
pos2 = {'a': (-2, 1), 'b': (-2, -1), 'x': (-1, 0), 'y': (0, 0), 'c': (1, 1), 'd': (1, 0), 'e': (1, -1)}
T2_labels = {
    'a': 'a',
    'b': 'b',
    'c': 'c',
    'd': 'd',
    'e': 'e',
    'x': r'$v_1$',
    'y': r'$v_2$'
}

# --- Trees z przekreśleniem i większą odległością ---
trees_combined = (
    r"\parbox{30em}{"
    r"\centering "
    r"$\ccc(u_1)$=\{\{a,b,c\}, \{a,b,d\}, \{a,b,e\}\},\\"  
    r"$\ccc(u_2)$=\{\{a,c,d\}, \{a,c,e\}, \{b,c,d\}, \{b,c,e\}\},\\"  
    r"$\ccc(u_3)$=\{\sout{\{a,d,e\}}, \sout{\{b,d,e\}}, \sout{\{c,d,e\}}\}\\[2em]" 
    r"$\ccc(v_1)$=\{\{a,b,c\}, \{a,b,d\}, \{a,b,e\}\},\\"  
    r"$\ccc(v_2)$=\{\{a,c,d\}, \{a,c,e\}, \sout{\{a,d,e\}}, \{b,c,d\}, \{b,c,e\}, \sout{\{b,d,e\}}, \sout{\{c,d,e\}}\}"
    r"}"
)

# --- Subploty: 3 wiersze, 1 kolumna ---
fig = plt.figure(figsize=(10, 9))
gs = gridspec.GridSpec(3, 1, height_ratios=[1, 1, 1])

ax1 = fig.add_subplot(gs[0])  # Górny graf
ax_mid = fig.add_subplot(gs[1])  # Środkowy napis
ax2 = fig.add_subplot(gs[2])  # Dolny graf

# --- Górny graf ---
nx.draw(G1, pos=pos1, with_labels=False, node_color='black', node_size=100, ax=ax1)

# przesunięcie etykiet: a i b bardziej w lewo, reszta standardowo
pos_labels_G1 = {}
for k, v in pos1.items():
    if k in ['a', 'b']:
        pos_labels_G1[k] = (v[0]-0.1, v[1])
    elif k in ['c', 'd', 'e']:
        pos_labels_G1[k] = (v[0]+0.15, v[1])
    else:
        pos_labels_G1[k] = (v[0]+0.1, v[1]-0.25)

nx.draw_networkx_labels(G1, pos=pos_labels_G1, labels=T1_labels, font_color='black', font_size=26, ax=ax1)

# Tytuł T1 na dole grafu
ax1.text(0.5, 0.0, r"$T_1$", fontsize=30, ha='center', va='top', transform=ax1.transAxes)
ax1.axis('off')

# --- Środkowy napis ---
ax_mid.text(0.5, 0.5, trees_combined, fontsize=25, ha='center', va='center')
ax_mid.axis('off')

# --- Dolny graf ---
nx.draw(G2, pos=pos2, with_labels=False, node_color='black', node_size=100, ax=ax2)
pos_labels_G2 = {}
for k, v in pos2.items():
    if k in ['a', 'b']:
        pos_labels_G2[k] = (v[0]-0.08, v[1])
    elif k in ['c', 'd', 'e']:
        pos_labels_G2[k] = (v[0]+0.1, v[1])
    else:
        pos_labels_G2[k] = (v[0]+0.1, v[1]-0.25)

nx.draw_networkx_labels(G2, pos=pos_labels_G2, labels=T2_labels, font_color='black', font_size=26, ax=ax2)
ax2.set_title(r"$T_2$", fontsize=30)
ax2.axis('off')

fig.subplots_adjust(left=0.05, right=0.95, top=1, bottom=0, hspace=0.4)
plt.savefig('T1_T2_partitions.png', bbox_inches='tight')
plt.show()

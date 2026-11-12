import sys
import networkx as nx
from statistics import mean

def parse_newick(newick_str):
    """Parsuje drzewo Newick do grafu nieskierowanego."""
    import re
    G = nx.Graph()
    stack = []
    node_id = 0

    tokens = re.findall(r'[(),;]|[^\s(),;]+', newick_str)
    for token in tokens:
        if token == '(':
            stack.append([])
        elif token == ')':
            children = stack.pop()
            internal_node = f'node_{node_id}'
            node_id += 1
            for child in children:
                G.add_edge(internal_node, child)
            if stack:
                stack[-1].append(internal_node)
        elif token == ',':
            continue
        elif token == ';':
            continue
        else:
            if stack:
                stack[-1].append(token)
            G.add_node(token)
    return G

def find_leaves(G):
    return [n for n in G.nodes if G.degree(n) == 1]

def internal_nodes_for_rerooting(G):
    """Zwraca tylko wierzchołki o stopniu 3 (typowe wierzchołki wewnętrzne w drzewach binarnych)."""
    return [n for n in G.nodes if G.degree(n) == 3]

def internal_edges_for_rerooting(G):
    """Zwraca krawędzie między węzłami, które nie są liśćmi."""
    leaves = find_leaves(G)
    return [(u, v) for u, v in G.edges if u not in leaves and v not in leaves]

def sackin_index(G, root):
    lengths = nx.single_source_shortest_path_length(G, root)
    return sum(lengths[n] for n in find_leaves(G))

def reroot_on_node(G_orig, node):
    return G_orig.copy(), node

def reroot_on_edge(G_orig, u, v):
    G = G_orig.copy()
    G.remove_edge(u, v)
    new_root = f'root_{u}_{v}'
    G.add_node(new_root)
    G.add_edge(new_root, u)
    G.add_edge(new_root, v)
    return G, new_root

def suppress_degree_2_nodes(G):
    G = G.copy()
    nodes_to_check = list(G.nodes)
    for n in nodes_to_check:
        if G.degree(n) == 2 and n not in find_leaves(G):
            neighbors = list(G.neighbors(n))
            G.remove_node(n)
            G.add_edge(neighbors[0], neighbors[1])
    return G

import csv

def read_multiple_trees(filename):
    """
    Wczytuje wiele drzew Newick z pliku.
    Zakłada, że każde drzewo jest w osobnej linii lub oddzielone średnikiem i nową linią.
    """
    trees = []
    with open(filename) as f:
        content = f.read().strip()
    # Podziel na drzewa — zakładam, że każde kończy się średnikiem
    raw_trees = [t.strip() for t in content.split(';') if t.strip()]
    for t in raw_trees:
        trees.append(t + ';')  # Dodaj średnik z powrotem
    return trees

def process_tree(newick_str):
    G = parse_newick(newick_str)
    G = suppress_degree_2_nodes(G)

    node_sackins = []
    for node in internal_nodes_for_rerooting(G):
        rooted_G, root = reroot_on_node(G, node)
        node_sackins.append(sackin_index(rooted_G, root))

    edge_sackins = []
    for u, v in internal_edges_for_rerooting(G):
        rooted_G, root = reroot_on_edge(G, u, v)
        edge_sackins.append(sackin_index(rooted_G, root))

    def stats(lst):
        return (min(lst) if lst else None,
                max(lst) if lst else None,
                mean(lst) if lst else None)

    node_stats = stats(node_sackins)
    edge_stats = stats(edge_sackins)

    return node_stats, edge_stats

def compare_tree_pairs_flat(tree_stats, writer, latex_fieldname_map):
    def compute_ops(val1, val2):
        if val1 is None or val2 is None:
            return '', '', '', ''
        s = val1 + val2
        d = abs(val1 - val2)
        p = val1 * val2
        r = min(val1, val2) / max(val1, val2) if max(val1, val2) != 0 else ''
        return f"{s:.3f}", f"{d:.3f}", f"{p:.3f}", f"{r:.3f}"

    for i in range(0, len(tree_stats) - 1, 2):
        t1 = tree_stats[i]
        t2 = tree_stats[i + 1]
        row = {
            'tree1': i + 1,
            'tree2': i + 2
        }

        for stat in ['min_node', 'max_node', 'mean_node', 'min_edge', 'max_edge', 'mean_edge']:
            row[f"{stat}1"] = t1.get(stat, '')
            row[f"{stat}2"] = t2.get(stat, '')

            v1 = t1.get(stat)
            v2 = t2.get(stat)
            s, d, p, r = compute_ops(v1, v2)
            row[f"{stat}_sum"] = s
            row[f"{stat}_absdiff"] = d
            row[f"{stat}_prod"] = p
            row[f"{stat}_ratio"] = r

        # Zamień oryginalne klucze na LaTeX
        row_latex = {
            latex_fieldname_map.get(k, k): v for k, v in row.items()
        }
        writer.writerow(row_latex)

def main(input_file):
    trees = read_multiple_trees(input_file)

    base_stats = ['min_node', 'max_node', 'mean_node', 'min_edge', 'max_edge', 'mean_edge']
    ops = ['sum', 'absdiff', 'prod', 'ratio']

    # pierwsze 14 kolumn
    flat_fieldnames = (
            ['tree1', 'tree2'] +
            [f"{stat}{i}" for stat in base_stats for i in [1, 2]]
    )

    latex_fieldname_map = {}  # oryginalna_nazwa: latex_nazwa

    for stat in base_stats:
        x, y = stat.split('_')
        y_tex = 'vert' if y == 'node' else 'edge'
        for op in ops:
            original_name = f"{stat}_{op}"  # np. mean_node_sum
            latex_label = f"${{\\verb+{op}+}}(S(T)_{{{x}_{{{y_tex}}}}})$"
            latex_fieldname_map[original_name] = latex_label
            flat_fieldnames.append(latex_label)

    tree_stats = []

    for tree_str in trees:
        node_stats, edge_stats = process_tree(tree_str)

        tree_stat_entry = {}
        if node_stats[0] is not None:
            tree_stat_entry.update({
                'min_node': node_stats[0],
                'max_node': node_stats[1],
                'mean_node': node_stats[2]
            })

        if edge_stats[0] is not None:
            tree_stat_entry.update({
                'min_edge': edge_stats[0],
                'max_edge': edge_stats[1],
                'mean_edge': edge_stats[2]
            })

        tree_stats.append(tree_stat_entry)

    # Zapis wyników tylko dla par
    with open(input_file + ".csv", mode='w', newline='') as pairs_file:
        flat_writer = csv.DictWriter(pairs_file, fieldnames=flat_fieldnames)
        flat_writer.writeheader()
        compare_tree_pairs_flat(tree_stats, flat_writer, latex_fieldname_map)


# Jeśli uruchamiasz skrypt z linii poleceń:
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Use: python unrooted_sackin_index.py input_trees.newick")
    else:
        main(sys.argv[1])

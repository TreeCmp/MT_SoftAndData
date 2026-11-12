import pandas as pd
from scipy.stats import spearmanr, pearsonr

# Wczytaj dane
file_path = "gen_newicks/n200_e200000_u_b_trees"
df1 = pd.read_csv(file_path + ".newick.csv")
df2 = pd.read_csv(file_path + ".out", sep='\t', nrows=100000)

# Wybierz odpowiednie kolumny
df1_features = df1.iloc[:, 14:]  # 24 kolumny
df2_features = df2.iloc[:, 3:]   # zaczynając od RF(0.5)

# Podział kolumn df1 na dwie części
df1_part1 = df1_features.iloc[:, :12]
df1_part2 = df1_features.iloc[:, 12:]

# Funkcja generująca tabelę LaTeX
def generate_latex_table(corr_matrix, row_labels, col_labels, title):
    latex = f"\\begin{{table}}[h]\n\\centering\n\\caption{{{title}}}\n"
    latex += "\\begin{tabular}{l" + "c" * len(col_labels) + "}\n"
    latex += " & " + " & ".join(col_labels) + " \\\\\n"
    latex += "\\hline\n"
    for i, row in enumerate(corr_matrix):
        latex += row_labels[i] + " & " + " & ".join(f"{val:.3f}" for val in row) + " \\\\\n"
    latex += "\\end{tabular}\n\\end{table}\n\n"
    return latex

# Oblicz korelacje
def compute_correlation(df1_block, df2_block, method="pearson"):

    print(f"[DEBUG] Długość x: {len(df1_block)}")
    print(f"[DEBUG] Długość y: {len(df2_block)}")

    if len(df1_block) != len(df2_block):
        raise ValueError(f"x i y mają różne długości: {len(df1_block)} != {len(df2_block)}")

    matrix = []
    for col1 in df1_block.columns:
        row = []
        for col2 in df2_block.columns:
            x = df1_block[col1]
            y = df2_block[col2]
            if method == "pearson":
                corr, _ = pearsonr(x, y)
            else:
                corr, _ = spearmanr(x, y)
            row.append(corr)
        matrix.append(row)
    return matrix

# Korelacje
pearson_1 = compute_correlation(df1_part1, df2_features, method="pearson")
pearson_2 = compute_correlation(df1_part2, df2_features, method="pearson")
spearman_1 = compute_correlation(df1_part1, df2_features, method="spearman")
spearman_2 = compute_correlation(df1_part2, df2_features, method="spearman")

# Generuj LaTeX
latex_output = ""
latex_output += generate_latex_table(pearson_1, df1_part1.columns, df2_features.columns, "Pearson correlation coefficients of metrics with the Sackin index (vertex rooting)")
latex_output += generate_latex_table(pearson_2, df1_part2.columns, df2_features.columns, "Pearson correlation coefficients of metrics with the Sackin index (vertex rooting)")
latex_output += generate_latex_table(spearman_1, df1_part1.columns, df2_features.columns, "Spearman correlation coefficients of metrics with the Sackin index (edge rooting)")
latex_output += generate_latex_table(spearman_2, df1_part2.columns, df2_features.columns, "Spearman correlation coefficients of metrics with the Sackin index (edge rooting)")

# Zapisz do pliku
with open(file_path + "_corr_tab.tex", "w") as f:
    f.write(latex_output)

print(f"Zapisano 4 tabele LaTeX do pliku {file_path + "_corr_tab.tex"}")

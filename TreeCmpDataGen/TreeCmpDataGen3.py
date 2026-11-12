import pandas as pd
from scipy.stats import spearmanr, pearsonr
from itertools import combinations

def corr_color(value):
    # Zakładamy wartość od 0 do 1 (lub -1 do 1 jeśli chcesz uwzględnić ujemne)
    r = value  # czerwony od 0 do 1
    g = 1 - value  # zielony od 1 do 0
    b = 0  # brak niebieskiego
    return f"\\cellcolor[rgb]{{{r:.2f},{g:.2f},{b:.2f}}}{value:.4f}"

# Wczytaj dane z pliku (zmień ścieżkę, jeśli potrzeba)
dfy = pd.read_csv('gen_newicks/n200_y200000_u_b_trees.out', sep='\t', nrows=100001, low_memory=False)
dfe = pd.read_csv('gen_newicks/n200_e200000_u_b_trees.out', sep='\t', nrows=100001, low_memory=False)

# Wybierz kolumny od 4 wzwyż (pomijamy No, Tree1, Tree2)
data_y = dfy.iloc[:, 3:].copy()
data_e = dfe.iloc[:, 3:].copy()

# Spróbuj przekonwertować wszystkie kolumny na liczby zmiennoprzecinkowe
# błędne wartości zostaną zamienione na NaN
for col in data_y.columns:
    data_y[col] = pd.to_numeric(data_y[col], errors='coerce')
for col in data_e.columns:
    data_e[col] = pd.to_numeric(data_e[col], errors='coerce')

# Usuń wiersze, w których brakuje danych (NaN)
data_y = data_y.dropna()
data_e = data_e.dropna()

# Generowanie wszystkich 15 par kolumn
column_pairs_y = list(combinations(data_y.columns, 2))
column_pairs_e = list(combinations(data_e.columns, 2))

# Lista wyników do DataFrame'a
results = []

# Zakładamy, że obie listy par (column_pairs_y i column_pairs_e) mają te same pary
# Jeśli kolumny są identyczne (co jest prawdopodobne), możemy użyć jednej pętli
for (col1, col2) in column_pairs_y:
    spearman_y, _ = spearmanr(data_y[col1], data_y[col2])
    pearson_y, _ = pearsonr(data_y[col1], data_y[col2])

    spearman_e, _ = spearmanr(data_e[col1], data_e[col2])
    pearson_e, _ = pearsonr(data_e[col1], data_e[col2])

    results.append({
        'Compared distances': f"{col1}-{col2}",
        'Spearman_y': round(spearman_y, 4),
        'Pearson_y': round(pearson_y, 4),
        'Spearman_e': round(spearman_e, 4),
        'Pearson_e': round(pearson_e, 4)
    })

# Tworzymy DataFrame z wynikami
results_df = pd.DataFrame(results)

with open("korelacje.tex", "w", encoding="utf-8") as f:
    f.write("\\begin{table}[htbp]\n\\centering\n")
    f.write("\\caption{Pearson and Spearman rank correlation for 6 unrooted metrics}\n")
    f.write("\\label{tab:correlations}\n")
    f.write("\\begin{tabular}{lcccc}\n")
    f.write("\\toprule\n")
    f.write("\\multirow{2}{*}{Compared distances} & \\multicolumn{2}{c}{Yule} & \\multicolumn{2}{c}{Uniform} \\\\\n")
    f.write("& Spearman & Pearson & Spearman & Pearson \\\\\n")
    f.write("\\midrule\n")

    for row in results:
        f.write(
            f"{row['Compared distances']} & "
            f"{corr_color(row['Spearman_y'])} & {corr_color(row['Pearson_y'])} & "
            f"{corr_color(row['Spearman_e'])} & {corr_color(row['Pearson_e'])} \\\\\n"
        )

    f.write("\\bottomrule\n")
    f.write("\\end{tabular}\n\\end{table}\n")



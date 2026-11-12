#!/usr/bin/env python
import subprocess
import os

from utilities import read_cmd_line_args
gen_trees_path = "gen_newicks"
data_path = "data"
leaves_count, are_trees_yule, trees_count, distances, are_trees_binary, are_trees_rooted = read_cmd_line_args()

##############################################
# creating trees database files if not exist #
##############################################
if not os.path.exists(gen_trees_path):
    os.makedirs(gen_trees_path)

programs_folder = "bin"
input_trees_file_name = "/n" + str(leaves_count) + "_" + are_trees_yule + str(trees_count * 2) + "_" + are_trees_binary + "_" + are_trees_rooted + "_trees"
input_trees_file_extension = ".newick"
output_result_file_extension = ".out"
output_graphic_file_extension = ".png"
output_summary_csv_file_extension = ".csv"
output_summary_txt_file_extension = ".txt"
input_tree_path = gen_trees_path + input_trees_file_name + input_trees_file_extension
output_tree_path = gen_trees_path + input_trees_file_name + output_result_file_extension
output_graphic_path = gen_trees_path + input_trees_file_name + output_graphic_file_extension
output_summary_path = gen_trees_path + input_trees_file_name + output_summary_csv_file_extension
output_summary_txt_path = gen_trees_path + input_trees_file_name + output_summary_txt_file_extension

if not os.path.exists(input_tree_path):
    gen_trees_cmd = [programs_folder + "/PRTGen.exe", "-n", str(leaves_count), "-" + are_trees_yule, str(trees_count * 2), "-" + are_trees_binary, "-" + are_trees_rooted, "-f", input_tree_path]
    print("Executing:", ' '.join(gen_trees_cmd))
    subprocess.check_call(gen_trees_cmd)
else:
    print(f"Trees already generated in file: {input_tree_path}")

if not os.path.exists(data_path):
    os.makedirs(data_path)

if not os.path.exists(output_tree_path):
    comp_dis_cmd = ["java", "-jar", programs_folder + "/TreeCmp-2.0-b103.jar", "-w", str(2), "-d", *distances, "-I", "-i", input_tree_path, "-o", output_tree_path]
    print("Executing:", ' '.join(comp_dis_cmd))
    subprocess.check_call(comp_dis_cmd)
else:
    print(f"Results already generated in file: {output_tree_path}")

###################
# load data files #
###################

import pandas as pd
import matplotlib.pyplot as plt

# Wczytanie pliku txt z separatorem tabulacji
df = pd.read_csv(output_tree_path, sep="\t", nrows=trees_count + 1)

# Wybór kolumn
columns = [
    ("RF(0.5)", "RF (Robinson-Foulds)"),
    ("PathDiffernce", "Path Difference"),
    ("Quartet", "Quartet Distance"),
    ("UMAST", "Unrooted MAST"),
    ("MatchingSplit", "Matching Split"),
    ("MatchingTriplet", "Matching Triplet")
]

# Tworzenie siatki 2x3
fig, axes = plt.subplots(2, 3, figsize=(18, 8))  # większy rozmiar dla czytelności

# Rysowanie każdego histogramu
for ax, (col, x_label) in zip(axes.flatten(), columns):
    ax.hist(df[col], bins=trees_count, edgecolor='black')
    # ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel('Number of pairs of trees')
    ax.grid(True)


# Wybierz kolumny od czwartej do końca
selected_columns = df.iloc[:, 3:]


from scipy.stats import skew

import numpy as np

def safe_skew(series):
    clean = series.dropna()
    if clean.nunique() <= 1:
        return np.nan  # Brak wariancji, skośność nie ma sensu
    return skew(clean)

# Własna funkcja: 6 cyfr znaczących + zawsze zapis dziesiętny
def format_float(x):
    try:
        if pd.isna(x):
            return ""
        # Format z 6 cyframi znaczącymi, zawsze jako dziesiętna liczba
        return f"{float(f'{x:.8g}')}"
    except:
        return str(x)

# Ustawienie opcji pandas
pd.options.display.float_format = format_float

# Oblicz statystyki
summary = pd.DataFrame({
    'Average': selected_columns.mean(),
    'Standard Deviation': selected_columns.std(),
    'Skewness': selected_columns.apply(skew),
    'Skewness Safe': selected_columns.apply(safe_skew),
    'Min': selected_columns.min(),
    'Max': selected_columns.max(),
    'Count': selected_columns.count()
})
# Wyświetl wyniki
print(summary)
# summary.to_csv(output_summary_csv_path)
with open(output_summary_txt_path, "w") as f:
    f.write(summary.to_string())

# Automatyczne rozmieszczenie i wyświetlenie
plt.tight_layout()
plt.savefig(output_graphic_path)
# plt.show()
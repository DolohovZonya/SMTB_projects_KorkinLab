# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 20:28:12 2025

@author: User
"""

import os
import pandas as pd

proteins_papka = os.listdir("D:/Downloads/databases_repeats_db/databases/rul_structure_db")

proteins = []
for papka in proteins_papka:
    pr = os.listdir(f"D:/Downloads/databases_repeats_db/databases/rul_structure_db/{papka}")
    for i in pr:
        i = i.split(sep="_")[0]
        for k in range(len(i)):
            if i[k].isupper():
                i = i.replace(i[k],"")
        proteins.append(i)

df_prs = pd.DataFrame(proteins)
df_prs.to_csv("proteins_from_repeats_db.csv")

scope_list_207 = []
with open("dir.cla.scope.2.07-stable.csv", "r") as scope_207:
    sc_2 = scope_207.readlines()
    for line in sc_2:
        line = line.split(",")
        scope_list_207.append(line)
scope_207_df = pd.DataFrame(scope_list_207, columns = ['id','pdb_id','coords','group','chislo','cl','cf','sf','fa','dm','sp','px','dop_1','dop_2','dop_3'])


repeats_df = []
for pro in proteins:
    x = scope_207_df.loc[scope_207_df['pdb_id'] == pro]
    if x.empty:
        continue
    else:
        selected_columns = x[['pdb_id', 'coords', 'cl', 'cf', 'sf', 'fa']].values[0]
        repeats_df.append(selected_columns)
df_rep = pd.DataFrame(repeats_df, columns = ['pdb_id', 'coords', 'cl', 'cf', 'sf', 'fa'])
df_rep_no_dup = df_rep.drop_duplicates(subset=['pdb_id'])
df_rep_no_dup.to_csv("repeats_in_scope_2.07_no_dup.csv")

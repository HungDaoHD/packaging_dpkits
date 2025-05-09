





# import pandas as pd
# import numpy as np
# import prince
# import matplotlib.pyplot as plt
# from sklearn.preprocessing import StandardScaler
#
#
#
# # 1) Load your data — now only one metric, Performance
# df = pd.read_excel('sample_ca_dataset.xlsx', sheet_name='Data3')
#
# # df = df.query("~Brand.isin(['Hisense', 'TCL', 'LG'])")
# # df = df.query("Brand.isin(['Sony'])")
#
# df = df.drop(columns=['AGE'])
#
#
# # 2) Split categorical vs continuous
# attr_cols = [
#     'Best picture quality',
#     'Leader in TV technology',
#     'Stylish TV',
#     'Best sound quality',
#     'Durable TV',
#     'Is a brand I trust',
#     'Is great for playing video games on',
#     'Come to mind first when thinking about',
#     'Is great for entertainment',
#     'Provide excellent customer service',
#     'Liked by young people',
#     'Has user friendly interface',
#     'Support a wide variety of video content apps (eg. Netflix, Youtube)',
#     'Able to control by voice',
#     'IoT compability',
#     'Advantaged Google Assistant functions',
#     'Good for Movie',
#     'Good for watching sports',
#     'Studio mastering quality/professional quality',
# ]
#
# df['PUR2TV'] = df['PUR2TV'].astype(float)
# df['CONSTV'] = df['CONSTV'].astype(float)
#
# df = pd.get_dummies(
#     df,
#     columns=['Brand'],
# )
#
# df[attr_cols] = df[attr_cols].astype(bool)
#
# std_scaler = StandardScaler()
# pur2tv_std = std_scaler.fit_transform(df[['PUR2TV', 'CONSTV']])
# df[['PUR2TV', 'CONSTV']] = pur2tv_std
#
# df = df.drop(columns=['PUR2TV', 'CONSTV'])
#
#
# # 2) Fit FAMD
# famd = prince.PCA(
#     n_components=2,
#     n_iter=10,
#     random_state=42,
# ).fit(df)
#
# # 3) Extract category-level coords and rename
# col_pts = famd.column_coordinates_
# col_pts.columns = ['Dim1', 'Dim2']
#
# # 4) Pull out brands and attributes
# brand_pts = col_pts.loc[col_pts.index.str.startswith('Brand_')]
# attr_pts = col_pts.loc[attr_cols]
#
# # 5) Plot
# fig, ax = plt.subplots(figsize=(8, 6))
# # brands
# ax.scatter(brand_pts['Dim1'], brand_pts['Dim2'], marker='D', c='tab:blue', label='Brands')
# for lbl,(x,y) in brand_pts.iterrows():
#     ax.text(x,y,lbl.split('_',1)[1], fontweight='bold')
#
# # attributes
# ax.scatter(attr_pts['Dim1'], attr_pts['Dim2'], marker='o', c='tab:red', label='Attributes')
# for lbl,(x,y) in attr_pts.iterrows():
#     ax.text(x,y,lbl.rsplit('_',1)[0], color='tab:red')
#
# # # continuous = PUR2TV appears as its own “column” level
# # pur_pt = col_pts.loc['PUR2TV', ['Dim1','Dim2']]
# # ax.arrow(0,0, pur_pt.Dim1, pur_pt.Dim2, head_width=0.02, length_includes_head=True, color='gray')
# # ax.text(pur_pt.Dim1*1.1, pur_pt.Dim2*1.1, 'PUR2TV', color='gray')
# #
# # # continuous = CONSTV appears as its own “column” level
# # con_pt = col_pts.loc['CONSTV', ['Dim1','Dim2']]
# # ax.arrow(0,0, con_pt.Dim1, con_pt.Dim2, head_width=0.02, length_includes_head=True, color='gray')
# # ax.text(con_pt.Dim1*1.1, con_pt.Dim2*1.1, 'CONSTV', color='gray')
#
#
#
# # axes & labels
# # inertia = famd.explained_inertia_
# ax.set_xlabel(f"Dim1 (%)")
# ax.set_ylabel(f"Dim2 (%)")
# ax.legend()
# plt.tight_layout()
# plt.show()








import pandas as pd
import numpy as np
import prince
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler


# 1) Load your data — now only one metric, Performance
df = pd.read_excel('sample_ca_dataset.xlsx', sheet_name='Data3')

# df = df.query("~Brand.isin(['Hisense'])")


# 2) Split categorical vs continuous
attr_cols = [
    'Best picture quality',
    'Leader in TV technology',
    'Stylish TV',
    'Best sound quality',
    'Durable TV',
    'Is a brand I trust',
    'Is great for playing video games on',
    'Come to mind first when thinking about',
    'Is great for entertainment',
    'Provide excellent customer service',
    'Liked by young people',
    'Has user friendly interface',
    'Support a wide variety of video content apps (eg. Netflix, Youtube)',
    'Able to control by voice',
    'IoT compability',
    'Advantaged Google Assistant functions',
    'Good for Movie',
    'Good for watching sports',
    'Studio mastering quality/professional quality',
]

# df_cat = df[['Brand'] + attr_cols].astype(str)   # for MCA

df_cat: pd.DataFrame = df[['Brand'] + attr_cols]

df_cat_melted = df_cat.melt(id_vars='Brand', var_name='Attribute').query("value == 1")
contingency = pd.pivot_table(
    data=df_cat_melted,
    index='Attribute',
    columns='Brand',
    values='value',
    aggfunc='count',
)


df_num = df[['PUR2TV']].astype(float)       # single metric


ca = prince.CA(
    # n_components=2,      # number of dimensions to keep
    n_iter=20,           # number of power-iterations
    # copy=True,           # leave the original table intact
    # check_input=True,
    # engine='sklearn',
    random_state=42
).fit(contingency)

row_coords = ca.row_coordinates(contingency)
col_coords = ca.column_coordinates(contingency)

row_coords.columns = ['Dim1', 'Dim2']
col_coords.columns = ['Dim1', 'Dim2']

# # 5) Compute average purchase intent by brand
purchase_by_brand = df.groupby('Brand')['PUR2TV'].mean()
purchase_by_brand = pd.DataFrame(purchase_by_brand)


std_scaler = StandardScaler()
pur2tv_std = std_scaler.fit_transform(purchase_by_brand)
purchase_by_brand['PUR2TV'] = pur2tv_std



# # 6) Compute the PUR2TV arrow (correlations with columns)
# dx = purchase_by_brand.corr(col_coords['Dim1'])
# dy = purchase_by_brand.corr(col_coords['Dim2'])

#
# X = col_coords[['Dim1', 'Dim2']]
# X = sm.add_constant(X)
# res = sm.OLS(purchase_by_brand, X).fit()
#
# # use the Dim1 and Dim2 slopes:
# dx, dy = res.params['Dim1'], res.params['Dim2']


dx = pd.concat([purchase_by_brand, col_coords['Dim1']], axis=1).corr().loc['Dim1', 'PUR2TV']
dy = pd.concat([purchase_by_brand, col_coords['Dim2']], axis=1).corr().loc['Dim2', 'PUR2TV']


# 7) Plot
fig, ax = plt.subplots(figsize=(10, 8))

# Attributes
ax.scatter(row_coords['Dim1'], row_coords['Dim2'],
           marker='o', color='red', label='Attributes')
for attr, (x, y) in row_coords.iterrows():
    ax.text(x, y, attr, color='red', fontsize=8)

# Brands
ax.scatter(col_coords['Dim1'], col_coords['Dim2'],
           marker='D', color='blue', s=100, label='Brands')
for brand, (x, y) in col_coords.iterrows():
    ax.text(x, y, brand, color='blue', fontsize=10, fontweight='bold')

# PUR2TV arrow
ax.arrow(0, 0, dx, dy,
         length_includes_head=True,
         head_width=0.02, head_length=0.03,
         color='gray', linewidth=2)
ax.text(dx*1.1, dy*1.1, 'PUR2TV', color='gray', fontsize=10)

# Axes lines
ax.axhline(0, color='black', linewidth=0.8)
ax.axvline(0, color='black', linewidth=0.8)

# Labels & title
# inertia = ca.explained_inertia_
ax.set_xlabel(f"Dim1 (% inertia)")
ax.set_ylabel(f"Dim2 (% inertia)")
ax.set_title("CA Biplot: Attributes, Brands & Purchase Intention", fontsize=14)
ax.legend(loc='best')
plt.tight_layout()
plt.show()




# # 3) Run MCA on the 7 categorical columns
# # mca = prince.MCA(n_components=2, n_iter=10, random_state=42).fit(df_cat)
# mca = prince.MCA(n_components=2, n_iter=10, random_state=42).fit(df_cat)
#
# # 4) Extract modality coordinates and rename axes
# mod_coords = mca.column_coordinates(df_cat)
# mod_coords.columns = ['Dim1','Dim2']
#
# # 5) Pull off the Brand points
# brand_pts = mod_coords.loc[mod_coords.index.str.startswith("Brand")].copy()
# brand_pts.index = [name.split("_",1)[-1] for name in brand_pts.index]
#
# # 6) Pull off the attribute=1 points
# attr_pts = mod_coords.loc[mod_coords.index.str.endswith("_1")].copy()
# attr_pts.index = [name.rsplit("_",1)[0] for name in attr_pts.index]
#
# # 7) Compute the Performance arrow
# row_coords = mca.row_coordinates(df_cat)
# row_coords.columns = ['Dim1','Dim2']
# perf_arrow = (
#     df_num['PUR2TV'].corr(row_coords['Dim1']),
#     df_num['PUR2TV'].corr(row_coords['Dim2'])
# )
#
#
# # 8) Get inertia for axis labels
# # inertia = mca.explained_inertia_
#
# # 9) Plot
# fig, ax = plt.subplots(figsize=(8, 6))
#
# # brands
# ax.scatter(brand_pts['Dim1'], brand_pts['Dim2'],
#            marker='D', s=150, color='tab:blue', label='Brands')
# for b,(x,y) in brand_pts.iterrows():
#     ax.annotate(b, (x,y), xytext=(4,4), textcoords='offset points',
#                 fontsize=11, fontweight='bold')
#
# # attributes
# ax.scatter(attr_pts['Dim1'], attr_pts['Dim2'],
#            marker='o', s=100, color='tab:red', label='Attributes')
# for a,(x,y) in attr_pts.iterrows():
#     ax.annotate(a, (x,y), xytext=(4,4), textcoords='offset points',
#                 fontsize=9, color='tab:red')
#
# # PUR2TV arrow
# dx, dy = perf_arrow
# ax.arrow(0,0, dx,dy,
#          length_includes_head=True,
#          head_width=0.03, head_length=0.05,
#          color='gray')
# ax.text(dx*1.1, dy*1.1, 'PUR2TV',
#         fontsize=10, ha='center', va='center', color='gray')
#
# # axes lines & labels
# ax.axhline(0, color='gray', linewidth=0.8)
# ax.axvline(0, color='gray', linewidth=0.8)
# ax.set_xlabel(f"Dim1 (% inertia)")
# ax.set_ylabel(f"Dim2 (% inertia)")
#
# ax.set_title("MCA Biplot: Brands, Attributes + PUR2TV")
# ax.legend(loc='best')
# plt.tight_layout()
# plt.show()




#
# import pandas as pd
# import numpy as np
# import prince
# import matplotlib.pyplot as plt
#
# # 1) Load your data
# df = pd.DataFrame({
#     'Brand': [
#       'Sony','Samsung','LG','Sony','Samsung','Sony','Sony','Samsung','Samsung',
#       'Sony','Samsung','Sony','Samsung','LG','Sony','Samsung','LG','Sony',
#       'Samsung','Samsung','LG','Sony','Samsung','LG','Samsung','LG'
#     ],
#     'Performance': [10,2,6,9,3,1,9,9,10,4,2,9,8,2,7,8,7,3,2,7,8,6,9,10,10,3],
#     'Closeness':   [8,7,8,7,7,2,7,8,4,5,5,7,5,7,5,6,8,2,2,2,2,5,6,4,2,9],
#     'Able to control by voice':                  [1,1,0,1,1,0,1,1,0,1,1,0,0,1,1,1,1,0,1,1,0,1,1,1,1,0],
#     'Advantaged Google Assistant functions':     [1,1,0,0,0,0,1,0,1,1,0,1,1,0,0,1,0,1,1,1,0,0,0,1,1,1],
#     'Best picture quality':                      [0,0,0,0,1,1,0,0,1,1,1,1,0,0,1,1,1,0,0,0,0,0,0,0,0,1],
#     'Best sound quality':                        [1,1,1,0,1,0,1,1,0,0,1,0,1,0,1,1,1,0,1,1,0,0,0,0,0,0],
#     'Come to mind first when thinking about':    [1,1,0,0,0,0,0,1,1,0,0,1,1,1,1,0,1,0,0,0,1,0,0,0,1,0],
#     'Durable TV':                                [1,1,0,0,1,0,1,0,1,0,1,1,0,1,0,1,0,1,1,0,1,1,0,0,1,1]
# })
#
# # 2) Split into categorical vs continuous
# attr_cols = [
#     'Able to control by voice',
#     'Advantaged Google Assistant functions',
#     'Best picture quality',
#     'Best sound quality',
#     'Come to mind first when thinking about',
#     'Durable TV'
# ]
# df_cat = df[['Brand'] + attr_cols].astype(str)
# df_num = df[['Performance','Closeness']].astype(float)
#
# # 3) Run MCA on the categorical block
# mca = prince.MCA(n_components=2, n_iter=5, random_state=42).fit(df_cat)
#
# # 4) Extract and rename the modality coordinates
# mod_coords = mca.column_coordinates(df_cat)
# mod_coords.columns = ['Dim1','Dim2']
#
# # 5) (Optional) Inspect how modalities are named
# print("Modalities:\n", list(mod_coords.index), "\n")
#
# # 6) Extract brand points
# brand_mask = mod_coords.index.str.startswith("Brand")
# brand_pts  = mod_coords.loc[brand_mask].copy()
# # use plain Python split to strip off the prefix
# brand_pts.index = [name.split("_",1)[-1] for name in brand_pts.index]
#
# # 7) Extract attribute=1 points
# attr_mask = mod_coords.index.str.endswith("_1")
# attr_pts  = mod_coords.loc[attr_mask].copy()
# # strip off the trailing '_1'
# attr_pts.index = [name.rsplit("_",1)[0] for name in attr_pts.index]
#
# # 8) Compute continuous‐variable vectors from correlations
# row_coords = mca.row_coordinates(df_cat)
# row_coords.columns = ['Dim1','Dim2']
# num_arrows = {
#     var: (
#       df_num[var].corr(row_coords['Dim1']),
#       df_num[var].corr(row_coords['Dim2'])
#     )
#     for var in df_num.columns
# }
#
# # 9) Compute inertia for axis labeling
# # inertia = mca.explained_inertia_
#
# # 10) Plot everything
# fig, ax = plt.subplots(figsize=(8,6))
#
# # Brands
# ax.scatter(brand_pts['Dim1'], brand_pts['Dim2'],
#            marker='D', s=150, color='tab:blue', label='Brands')
# for b,(x,y) in brand_pts.iterrows():
#     ax.annotate(b, (x,y), xytext=(4,4), textcoords='offset points',
#                 fontsize=11, fontweight='bold')
#
# # Attributes
# ax.scatter(attr_pts['Dim1'], attr_pts['Dim2'],
#            marker='o', s=100, color='tab:red', label='Attributes')
# for a,(x,y) in attr_pts.iterrows():
#     ax.annotate(a, (x,y), xytext=(4,4), textcoords='offset points',
#                 fontsize=9, color='tab:red')
#
# # Continuous arrows
# for var,(dx,dy) in num_arrows.items():
#     ax.arrow(0,0, dx,dy,
#              length_includes_head=True,
#              head_width=0.03, head_length=0.05,
#              color='gray')
#     ax.text(dx*1.1, dy*1.1, var,
#             fontsize=10, ha='center', va='center', color='gray')
#
# # Axes lines & labels
# ax.axhline(0, color='gray', linewidth=0.8)
# ax.axvline(0, color='gray', linewidth=0.8)
# ax.set_xlabel(f"Dim1 (% inertia)")
# ax.set_ylabel(f"Dim2 (% inertia)")
#
# ax.set_title("MCA Biplot: Unique Brands, Attributes + Metrics")
# ax.legend(loc='best')
# plt.tight_layout()
# plt.show()














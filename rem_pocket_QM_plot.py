import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# plot REM ion interaction with 7CCO trimmed pocket QM 
# results relative to those for La3+
# and compare to experiment

# Pocket QM Results
# Read in the csv as a dataframe
pocket_df = pd.read_csv("pocket_results.csv")

# make Gas Single Point and PCM Single Point columns
# decide which to use when there are 2 values
# by finding which values are closest to each other
# I'm sure there is something more elegant but this my caveman way
for index, row in pocket_df.iterrows():
    G1 = row["Gas SP 1"]
    G2 = row["Gas SP 2"]
    P1 = row["PCM SP 1"]
    P2 = row["PCM SP 2"]
    diff1 = G1 - P1
    diff2 = G1 - P2
    diff3 = G2 - P1
    diff4 = G2 - P2
    diffs = {'G1P1': diff1 , 'G1P2': diff2, 'G2P1': diff3 , 'G2P2': diff4 }
    smallest_dif = min(diffs, key=diffs.get)
    if smallest_dif == 'G1P1' :
         GasSP = G1
         PcmSP = P1
    if smallest_dif == 'G1P2' :
         GasSP = G1
         PcmSP = P2
    if smallest_dif == 'G2P1' :
         GasSP = G2
         PcmSP = P1
    if smallest_dif == 'G2P2' :
         GasSP = G2
         PcmSP = P2       
    pocket_df.loc[index, 'Gas SP'] = GasSP
    pocket_df.loc[index, 'PCM SP'] = PcmSP       

#print(pocket_df['Electronic + ZPE'])

pocket_df['Electronic'] = pocket_df['Electronic + ZPE'] - pocket_df['ZPE Corr']
print(pocket_df['Electronic'])
pocket_df['PCM Corr'] = pocket_df['PCM SP'] - pocket_df['Electronic']
pocket_df['PCM Corr'] *= 627.5
pocket_df['Thermal Corr'] = pocket_df['Electronic + Thermal FE'] - pocket_df['Electronic']
pocket_df['Thermal Corr'] *= 627.5

# relative to La
La_pocket_df = pocket_df.loc[pocket_df['Element'] == "La"]
for index, row in pocket_df.iterrows():
    La_PCM = La_pocket_df.loc[0, 'PCM Corr']
    pocket_df['Rel PCM Corr'] = pocket_df['PCM Corr'] - La_PCM
    La_ThermCorr = La_pocket_df.loc[0,'Thermal Corr']
    pocket_df['Rel Thermal Corr'] = pocket_df['Thermal Corr'] - La_ThermCorr




# #################################################

# Pocket QM Results
# Read in the csv as a dataframe
water_df = pd.read_csv("water_results.csv")

# make Gas Single Point and PCM Single Point columns
# decide which to use when there are 2 values
# by finding which values are closest to each other
# I'm sure there is something more elegant but this my caveman way
for index, row in water_df.iterrows():
    G1 = row["Gas SP 1"]
    G2 = row["Gas SP 2"]
    P1 = row["PCM SP 1"]
    P2 = row["PCM SP 2"]
    diff1 = G1 - P1
    diff2 = G1 - P2
    diff3 = G2 - P1
    diff4 = G2 - P2
    diffs = {'G1P1': diff1 , 'G1P2': diff2, 'G2P1': diff3 , 'G2P2': diff4 }
    smallest_dif = min(diffs, key=diffs.get)
    if smallest_dif == 'G1P1' :
         GasSP = G1
         PcmSP = P1
    if smallest_dif == 'G1P2' :
         GasSP = G1
         PcmSP = P2
    if smallest_dif == 'G2P1' :
         GasSP = G2
         PcmSP = P1
    if smallest_dif == 'G2P2' :
         GasSP = G2
         PcmSP = P2       
    water_df.loc[index, 'Gas SP'] = GasSP
    water_df.loc[index, 'PCM SP'] = PcmSP       

#print(water_df['Electronic + ZPE'])

water_df['Electronic'] = water_df['Electronic + ZPE'] - water_df['ZPE Corr']
print(water_df['Electronic'])
water_df['PCM Corr'] = water_df['PCM SP'] - water_df['Electronic']
water_df['PCM Corr'] *= 627.5
water_df['Thermal Corr'] = water_df['Electronic + Thermal FE'] - water_df['Electronic']
water_df['Thermal Corr'] *= 627.5

# relative to La
La_water_df = water_df.loc[pocket_df['Element'] == "La"]
for index, row in water_df.iterrows():
    La_PCM = La_water_df.loc[0, 'PCM Corr']
    water_df['Rel PCM Corr'] = water_df['PCM Corr'] - La_PCM
    La_ThermCorr = La_water_df.loc[0,'Thermal Corr']
    water_df['Rel Thermal Corr'] = water_df['Thermal Corr'] - La_ThermCorr

# #################################################

# add prefixes to column names in both dataframes
pocket_df = pocket_df.add_prefix('Pocket ')
pocket_df['Element'] = pocket_df['Pocket Element']
water_df = water_df.add_prefix('Water ')
water_df['Element'] = water_df['Water Element']
results_df = pd.merge(pocket_df, water_df, how="outer", on="Element")

# # add columns for experimental results
# dG_expt = {
#     "La": "-6.75",	
#     "Nd": "-8.3",
#     "Sm": "-8.7",
#     "Gd": "-9",
#     "Tb": "-9.1",
#     "Yb": "-9.15",
#     "Lu": "-9"
# }
# dG_expt_df = pd.DataFrame(data=[*dG_expt.values()], columns=['Element','dG_expt'])

# ddG_expt = {
#     "La": "0",
#     "Nd": "-1.55",
#     "Sm": "-1.95",
#     "Gd": "-2.25",
#     "Tb": "-2.35",
#     "Yb": "-2.4",
#     "Lu": "-2.25"
# }
# ddG_expt_df = pd.DataFrame(data=[*ddG_expt.values()], columns=['Element','ddG_expt'])

# # put experimental dfs together
# expt_df = pd.merge(dG_expt_df, ddG_expt_df, how="outer", on="Element")

# # combine QM and experimental result dfs
# df = pd.merge(results_df, expt_df, how="outer", on="Element")

# # add column for relative binding
# #'RelBinding' = ( 'Pocket RelPCM' - 'Water  RelPCM' )
# df.loc['RelBinding'] = df.loc['Pocket RelPCM'] - df.loc['Water  RelPCM']

# #################################################

# # make color palette 
# #TolPalette = ['#332288', '#117733', '#44AA99', '#88CCEE', '#DDCC77', '#CC6677', '#AA4499', '#882255']
# #Tol color palette for reference
# #332288 # violet
# #117733 # green
# #44AA99 # aqua
# #88CCEE # light blue
# #DDCC77 # yellow
# #CC6677 # peach
# #AA4499 # pink
# #882255 # mauve-ish

# # plot figure
# #fig, ax = plt.subplots()
# X = df['Element']
# Y_QM = df['RelBinding']
# Z_Ex = df['ddG_expt']

# X_axis = np.arrange(len(X))

# plt.bar(X_axis - 0.2, Y_QM, 0.4, label = 'QM', color = '#CC6677')
# plt.bar(X_axis + 0.2, Z_Ex, 0.4, label = 'Expt', color = '#88CCEE')
  
# plt.xticks(X_axis, X)
# plt.xlabel("Element")
# plt.ylabel("Relative Interaction Energy (kcal/mol)")
# plt.title("Interaction Energies of REMs with Lanthanum Binding Tag 7CCO (Relative to Lanthanum)")
# plt.legend()
# plt.show()

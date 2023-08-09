import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# plot REM ion interaction with 7CCO trimmed pocket QM 
# results relative to those for La3+
# and compare to experiment

# Pocket QM Results
# Read in the csv as a dataframe
pocket_df = pd.read_csv("pocket_results.csv")

# do need to decide which to use when there are 2 values
#[(ele+thermo)-(ele)]*627.5
pocket_df.loc['Gas-Therm'] = pocket_df.loc['Electronic + Thermal FE'] - pocket_df.loc['SP Gas 1']
pocket_df['Gas-Therm'] *= 627.5

# do need to decide which to use when there are 2 values
#(PCM-Gas)*627.5
pocket_df.loc['PCM-Gas'] = pocket_df.loc['SP PCM 1 (B3LYP/6-31G* + def2-TZVP)'] - pocket_df.loc['SP Gas 1']
pocket_df['PCM-Gas'] *= 627.5

# relative to La
# get La row
La_pocket_df = pocket_df.loc[pocket_df['Element'] == "La",]
#'RelGas' = 'PCM-Gas' - La.'PCM-Gas'
pocket_df.loc['RelGas'] = pocket_df.loc['Gas-Therm'] - La_pocket_df.loc['Gas-Therm']
#'RelPCM' = 'PCM-Gas' - La.'PCM-Gas'
pocket_df.loc['RelPCM'] = pocket_df.loc['PCM-Gas'] - La_pocket_df.loc['PCM-Gas']

#################################################

# Water QM Results
# Read in the csv as a dataframe
water_df = pd.read_csv("water_results.csv")

# do need to decide which to use when there are 2 values
#[(ele+thermo)-(ele)]*627.5
water_df.loc['Gas-Therm'] = water_df.loc['Electronic + Thermal FE'] - water_df.loc['SP Gas 1']
water_df['Gas-Therm'] *= 627.5

#'Gas-Therm' = ('Electronic + Thermal FE' - 'SP Gas 1') * 627.5
# do need to decide which to use when there are 2 values
#(PCM-Gas)*627.5
water_df.loc['PCM-Gas'] = water_df.loc['SP PCM 1 (B3LYP/6-31G* + def2-TZVP)'] - water_df.loc['SP Gas 1']
water_df['PCM-Gas'] *= 627.5

# relative to La
# get La row
La_water_df = water_df.loc[water_df['Element'] == "La",]
#'RelGas' = 'PCM-Gas' - La.'PCM-Gas'
water_df.loc['RelGas'] = water_df.loc['Gas-Therm'] - La_water_df.loc['Gas-Therm']
#'RelPCM' = 'PCM-Gas' - La.'PCM-Gas'
water_df.loc['RelPCM'] = water_df.loc['PCM-Gas'] - La_water_df.loc['PCM-Gas']

#################################################

# add prefixes to column names in both dataframes
pocket_df.add_prefix('Pocket ')
water_df.add_prefix('Water ')
results_df = pd.merge(pocket_df, water_df, how="outer", on="Element")

# add columns for experimental results
dG_expt = {
    "La": "-6.75",	
    "Nd": "-8.3",
    "Sm": "-8.7",
    "Gd": "-9",
    "Tb": "-9.1",
    "Yb": "-9.15",
    "Lu": "-9"
}
dG_expt_df = pd.DataFrame(data=[*dG_expt.values()], columns=['Element','dG_expt'])

ddG_expt = {
    "La": "0",
    "Nd": "-1.55",
    "Sm": "-1.95",
    "Gd": "-2.25",
    "Tb": "-2.35",
    "Yb": "-2.4",
    "Lu": "-2.25"
}
ddG_expt_df = pd.DataFrame(data=[*ddG_expt.values()], columns=['Element','ddG_expt'])

# put experimental dfs together
expt_df = pd.merge(dG_expt_df, ddG_expt_df, how="outer", on="Element")

# combine QM and experimental result dfs
df = pd.merge(results_df, expt_df, how="outer", on="Element")

# add column for relative binding
#'RelBinding' = ( 'Pocket RelPCM' - 'Water  RelPCM' )
df.loc['RelBinding'] = df.loc['Pocket RelPCM'] - df.loc['Water  RelPCM']

#################################################

# make color palette 
#TolPalette = ['#332288', '#117733', '#44AA99', '#88CCEE', '#DDCC77', '#CC6677', '#AA4499', '#882255']
#Tol color palette for reference
#332288 # violet
#117733 # green
#44AA99 # aqua
#88CCEE # light blue
#DDCC77 # yellow
#CC6677 # peach
#AA4499 # pink
#882255 # mauve-ish

# plot figure
#fig, ax = plt.subplots()
X = df['Element']
Y_QM = df['RelBinding']
Z_Ex = df['ddG_expt']

X_axis = np.arrange(len(X))

plt.bar(X_axis - 0.2, Y_QM, 0.4, label = 'QM', color = '#CC6677')
plt.bar(X_axis + 0.2, Z_Ex, 0.4, label = 'Expt', color = '#88CCEE')
  
plt.xticks(X_axis, X)
plt.xlabel("Element")
plt.ylabel("Relative Interaction Energy (kcal/mol)")
plt.title("Interaction Energies of REMs with Lanthanum Binding Tag 7CCO (Relative to Lanthanum)")
plt.legend()
plt.show()

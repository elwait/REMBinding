import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# This script is for organizing results from QM calculations of REM binding,
# procesing those results to get binding energies (relative to La3+),
# and comparing with experimental data

#################################################

# Pocket QM Results
# Read in the csv as a dataframe
# This csv file should have been already created using a different script
pocket_df = pd.read_csv("pocket_results.csv")

# Make Gas Single Point and PCM Single Point columns
# Somtimes Gaussian prints 2 values
# We decide which to use by finding which values are closest to each other
# I'm sure there is some more elegant solution but this my caveman way
for index, row in pocket_df.iterrows():
    G1 = row["Gas SP 1"]
    G2 = row["Gas SP 2"]
    P1 = row["PCM SP 1"]
    P2 = row["PCM SP 2"]
    diff1 = abs(G1 - P1)
    #print(diff1)
    diff2 = abs(G1 - P2)
    #print(diff2)
    diff3 = abs(G2 - P1)
    #print(diff3)
    diff4 = abs(G2 - P2)
    #print(diff4)
    # Store all differences in dict with keys to know which are which
    diffs = {'G1P1': diff1 , 'G1P2': diff2, 'G2P1': diff3 , 'G2P2': diff4 }
    #print(diffs)
    # Find pair with smallest difference
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
    # Keep vals from pair with smallest difference
    pocket_df.loc[index, 'Gas SP'] = GasSP
    pocket_df.loc[index, 'PCM SP'] = PcmSP       

# Electronic Energy = 'Electornic Energy + ZPE Correction' - 'ZPE Correction' 
pocket_df['Electronic'] = pocket_df['Electronic + ZPE'] - pocket_df['ZPE Corr']
# PCM Correction (implicit solvent contribution) = 'Energy of system in PCM'
#                                                  - 'Electronic energy of system'
pocket_df['PCM Corr'] = pocket_df['PCM SP'] - pocket_df['Electronic']
# Multiply by 627.5 to convert to Kcal
pocket_df['PCM Corr'] *= 627.5
# Thermal Correction (from opt/freq job) = 'Electronic + Thermal Free Energy'
#                                          - 'Electronic energy of system'
pocket_df['Thermal Corr'] = pocket_df['Electronic + Thermal FE'] - pocket_df['Electronic']
# Multiply by 627.5 to convert to Kcal
pocket_df['Thermal Corr'] *= 627.5

# Energies relative to La
# Store values only for La
La_pocket_df = pocket_df.loc[pocket_df['Element'] == "La"]
# Store values in variables for easy math
La_PCM = La_pocket_df.loc[0, 'PCM Corr']
La_ThermCorr = La_pocket_df.loc[0,'Thermal Corr']
La_GasSP = La_pocket_df.loc[0, 'Gas SP']
# for each row in pocket dataframe
for index, row in pocket_df.iterrows():
    # Ion Pocket PCM Correction - La Pocket PCM Correction
    pocket_df['Rel PCM Corr'] = pocket_df['PCM Corr'] - La_PCM
    # Ion Pocket Thermal Correction - La Pocket Thermal Correction
    pocket_df['Rel Thermal Corr'] = pocket_df['Thermal Corr'] - La_ThermCorr
    # Ion Pocket Gas Single Point Energy - La Pocket Gas Single Point Energy
    pocket_df['Rel Gas SP'] = pocket_df['Gas SP'] - La_GasSP

#################################################

# Pocket QM Results
# Read in the csv as a dataframe
# This csv file should have been already created using a different script
water_df = pd.read_csv("water_results.csv")

# Make Gas Single Point and PCM Single Point columns
# Somtimes Gaussian prints 2 values
# We decide which to use by finding which values are closest to each other
for index, row in water_df.iterrows():
    G1 = row["Gas SP 1"]
    G2 = row["Gas SP 2"]
    P1 = row["PCM SP 1"]
    P2 = row["PCM SP 2"]
    diff1 = abs(G1 - P1)
    diff2 = abs(G1 - P2)
    diff3 = abs(G2 - P1)
    diff4 = abs(G2 - P2)
    # Store all differences in dict with keys to know which are which
    diffs = {'G1P1': diff1 , 'G1P2': diff2, 'G2P1': diff3 , 'G2P2': diff4 }
    # Find pair with smallest difference
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
    # Keep vals from pair with smallest difference
    water_df.loc[index, 'Gas SP'] = GasSP
    water_df.loc[index, 'PCM SP'] = PcmSP       

# Electronic Energy = 'Electornic Energy + ZPE Correction' - 'ZPE Correction' 
water_df['Electronic'] = water_df['Electronic + ZPE'] - water_df['ZPE Corr']
# PCM Correction (implicit solvent contribution) = 'Energy of system in PCM'
#                                                  - 'Electronic energy of system'
water_df['PCM Corr'] = water_df['PCM SP'] - water_df['Electronic']
# Multiply by 627.5 to convert to Kcal
water_df['PCM Corr'] *= 627.5
# Thermal Correction (from opt/freq job) = 'Electronic + Thermal Free Energy'
#                                          - 'Electronic energy of system'
water_df['Thermal Corr'] = water_df['Electronic + Thermal FE'] - water_df['Electronic']
# Multiply by 627.5 to convert to Kcal
water_df['Thermal Corr'] *= 627.5

# Energies relative to La
# Store values only for La
La_water_df = water_df.loc[pocket_df['Element'] == "La"]
# Store values in variables for easy math
La_PCM = La_water_df.loc[0, 'PCM Corr']
La_ThermCorr = La_water_df.loc[0,'Thermal Corr']
La_GasSP = La_water_df.loc[0, 'Gas SP']
# for each row in water dataframe
for index, row in water_df.iterrows():
    # La Water PCM Correction - Ion Water PCM Correction
    water_df['Rel PCM Corr'] = La_PCM - water_df['PCM Corr']
    # La Water Thermal Correction - Ion Water Thermal Correction
    water_df['Rel Thermal Corr'] = La_ThermCorr - water_df['Thermal Corr']
    # Ion Water Gas Single Point Energy - La Water Gas Single Point Energy
    water_df['Rel Gas SP'] = water_df['Gas SP'] - La_GasSP

#################################################

# Add prefixes to column names in both dataframes
pocket_df = pocket_df.add_prefix('Pocket ')
# Rename Element so it doesn't have prefix and can be used to merge dataframes
pocket_df = pocket_df.rename(columns={'Pocket Element': 'Element'})
water_df = water_df.add_prefix('Water ')
# Rename Element so it doesn't have prefix and can be used to merge dataframes
water_df = water_df.rename(columns={'Water Element': 'Element'})
# Merge water and pocket dataframes on Element
results_df = pd.merge(pocket_df, water_df, how="outer", on="Element")

#################################################

# Add columns for experimental results

# Dictionary of experimental binding free energies
dG_expt = {
    'La': -6.75,	
    'Nd': -8.3,
    'Sm': -8.7,
    'Gd': -9.0,
    'Tb': -9.1,
    'Yb': -9.15,
    'Lu': -9.0
}
# Dataframe of experimental binding free energies
dG_expt_df = pd.DataFrame(dG_expt.items(), columns=['Element', 'dG Expt'])

# Dictionary of experimental relative binding free energies
ddG_expt = {
    'La': 0.0,
    'Nd': -1.55,
    'Sm': -1.95,
    'Gd': -2.25,
    'Tb': -2.35,
    'Yb': -2.4,
    'Lu': -2.25
}
# Dataframe of experimental relative binding free energies
ddG_expt_df = pd.DataFrame(ddG_expt.items(), columns=['Element', 'ddG_expt'])

# Put experimental dfs together
expt_df = pd.merge(dG_expt_df, ddG_expt_df, how="outer", on="Element")

# Combine QM and experimental result dfs
df = pd.merge(results_df, expt_df, how="outer", on="Element")

#################################################

# Add column for relative binding energy in Kcal (gas phase)
df['Relative Binding Energy (Kcal)'] = df['Pocket Rel Gas SP'] - df['Water Rel Gas SP'] 
df['Relative Binding Energy (Kcal)'] *= 627.5
#print(df['Relative Binding Energy (Kcal)'])

# Add column for relative binding FREE energy in Kcal (with corrections) 
df['Relative Binding Free Energy (Kcal)'] = ( df['Relative Binding Energy (Kcal)'] + 
                                            df['Pocket Rel Thermal Corr'] + df['Pocket Rel PCM Corr'] + 
                                            df['Water Rel Thermal Corr'] + df['Water Rel PCM Corr'] )
#print(df['Relative Binding Free Energy (Kcal)'])

# Create smaller dataframe with just the important results
# because the dataframe with EVERYTHING is useful but hard to look at
important_results = df[['Element', 'Pocket Rel PCM Corr', 'Water Rel PCM Corr', 
                        'Pocket Rel Thermal Corr', 'Water Rel Thermal Corr', 
                        'Pocket Rel Gas SP', 'Water Rel Gas SP', 'Relative Binding Energy (Kcal)', 
                        'Relative Binding Free Energy (Kcal)']].copy()

#################################################

# Export results to .csv file

# Will import data from these csvs later to excel to look at + plot
# unless we change our minds later and just use matplotlib to plot
important_results.to_csv('REM-binding_important_results.csv', index=False)
df.to_csv('REM-binding_all_results.csv', index=False)

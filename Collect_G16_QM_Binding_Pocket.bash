#!/bin/bash

working_dir="/work/eew947/sandia/QM-binding/pocket" #$PWD
opt_dir="/work/eew947/sandia/QM-binding/pocket/opt"
sp_pcm_dir="/work/eew947/sandia/QM-binding/pocket/sp_pcm"
sp_gas_dir="/work/eew947/sandia/QM-binding/pocket/sp_gas"

touch pocket_results.csv
echo 'Element,SP PCM 1 (B3LYP/6-31G* + def2-TZVP),SP PCM 2,SP Gas 1 (B3LYP/def2-TZVP + Sapporo-DKH3-TZVP),SP Gas 2,ZPE Corr,Thermal Corr Energy,Thermal Corr Enthalpy,Thermal Corr Gibbs FE,Electronic + ZPE,Electronic+Thermal Energies,Electronic + Thermal Enthalpies,Electronic + Thermal FE' > pocket_results.csv

while IFS= read -r line; do
    element=$(echo ${line} | awk '{ print $1 }' ) # use awk to grab 1st part of line
    echo $element
    #multiplicity=$(echo ${line} | awk '{ print $2 }' ) # use awk to grab 2nd part
    # collect energies from gaussian output for each element
    sp_pcm_energy_full=$(grep "SCF Done" ${sp_pcm_dir}/${element}/${element}_sp_pcm.log | awk '{ print $5 }')
    #echo $sp_pcm_energy_full
    # There was something Dr. Ren said about which values to use if there were 2 but I am confused so I will include both
    sp_pcm_energy_1=$(echo ${sp_pcm_energy_full} | awk '{ print $1 }')
    #echo "sp_pcm_energy_1 = ${sp_pcm_energy_1}"
    sp_pcm_energy_2=$(echo ${sp_pcm_energy_full} | awk '{ print $2 }')
    #echo "sp_pcm_energy_2 = ${sp_pcm_energy_2}" 
    sp_gas_energy_full=$(grep "SCF Done" ${sp_gas_dir}/${element}/${element}_sp.log  | awk '{ print $5 }')
    #echo "$sp_gas_energy_full"
    sp_gas_energy_1=$(echo ${sp_gas_energy_full} | awk '{ print $1 }')
    #echo "sp_gas_energy_1 = ${sp_gas_energy_1}"
    sp_gas_energy_2=$(echo ${sp_gas_energy_full} | awk '{ print $2 }')
    #echo "sp_gas_energy_2 = ${sp_gas_energy_2}"
    zp_corr=$(grep "Zero-point correction=" ${opt_dir}/${element}/${element}_def2tzvp.log | awk '{ print $3 }')
    #echo "zp_corr = ${zp_corr}"
    therm_corr_ener=$(grep "Thermal correction to Energy=" ${opt_dir}/${element}/${element}_def2tzvp.log | awk '{ print $5 }')
    #echo "therm_corr_ener = ${therm_corr_ener}"
    therm_corr_enth=$(grep "Thermal correction to Enthalpy=" ${opt_dir}/${element}/${element}_def2tzvp.log | awk '{ print $5 }')
    #echo "therm_corr_enth = ${therm_corr_enth}"
    therm_corr_gib=$(grep "Thermal correction to Gibbs Free Energy=" ${opt_dir}/${element}/${element}_def2tzvp.log | awk '{ print $7 }')
    #echo "therm_corr_gib = ${therm_corr_gib}"
    sum_ele_zpe=$(grep "Sum of electronic and zero-point Energies=" ${opt_dir}/${element}/${element}_def2tzvp.log | awk '{ print $7 }')
    #echo "sum_ele_zpe = ${sum_ele_zpe}"
    sum_ele_therm_ener=$(grep "Sum of electronic and thermal Energies=" ${opt_dir}/${element}/${element}_def2tzvp.log | awk '{ print $7 }')
    #echo "sum_ele_therm_ener = ${sum_ele_therm_ener}"
    sum_ele_therm_enth=$(grep "Sum of electronic and thermal Enthalpies=" ${opt_dir}/${element}/${element}_def2tzvp.log | awk '{ print $7 }')
    #echo "sum_ele_therm_enth = ${sum_ele_therm_enth}"
    sum_ele_therm_fe=$(grep "Sum of electronic and thermal Free Energies=" ${opt_dir}/${element}/${element}_def2tzvp.log | awk '{ print $8 }')
    #echo "sum_ele_therm_fe = ${sum_ele_therm_fe}"
    # write results for this element into pocket_results.csv
    echo "${element},${sp_pcm_energy_1},${sp_pcm_energy_2},${sp_gas_energy_1},${sp_gas_energy_2},${zp_corr},${therm_corr_ener},${therm_corr_enth},${therm_corr_gib},${sum_ele_zpe},${sum_ele_therm_ener},${sum_ele_therm_enth},${sum_ele_therm_fe}" >> pocket_results.csv
done < element_list.txt


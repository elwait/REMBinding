#!/bin/bash

# Purpose:
# Prepare input for REM QM binding calculations
# At this time, script creates jobs for each element for gas phase opt in 9 waters
# lines for job submission are written to a *sh file also

# Start script in working dir (ex: /work/eew947/sandia/QM-binding/water)
# make sure element_list.txt is in working dir

#B3LYP/6-31G* & def2-TZVP (ion) for gas-phase opt and PCM cal (PCM does not work with DKH )
#B3LYP/Sapporo-DKH3-TZVP (ion) & def2-TZVP for gas-phase singe point energy w/ relativistic effect; “int=DKH”


g16_rc="/home/eew947/.g16.bashrc"
template_dir="/work/eew947/sandia/QM-binding/water"
template="XX_water_opt.com"
working_dir="/work/eew947/sandia/QM-binding/water" #$PWD


basis1="def2tzvp"
basis1_dir="/work/eew947/sandia/QM-binding/basissets/def2tzvp"
basis2="S-dkh3tzp"
basis2_dir="/work/eew947/sandia/QM-binding/basissets/sapporoDKH3TZP"
#basis filename examples
# Lu_def2tzvp.txt
# Lu_S-dkh3tzp.txt


touch ${working_dir}/water_opt_jobs.txt
echo "source /home/eew947/.g16.bashrc" >> ${working_dir}/water_opt_jobs.txt
### Setting up input files for gas phase opt with basis 1 ###
# for each line in element_list.txt
while IFS= read -r line; do
    echo $line
    element=$(echo ${line} | awk '{ print $1 }' ) # use awk to grab 1st part of line
    multiplicity=$(echo ${line} | awk '{ print $2 }' ) # use awk to grab 2nd part
    #mkdir ${working_dir}/${element} 
    #cp ${template_dir}/${template} ${working_dir}/${element}/${element}_water_opt.com
    # replace "XX" with element symbol
    #sed -i "s+XX+${element}+g" ${working_dir}/${element}/${element}_water_opt.com
    # replace "mult" with correct multiplicity
    #sed -i "s+mult+${multiplicity}+g" ${working_dir}/${element}/${element}_water_opt.com
    # replace "basis" with name of basis set being used
    #sed -i "s+basis+${basis1}+g" ${working_dir}/${element}/${element}_water_opt.com
    # append basis set and sphere radius info to end of input file
    cat "/work/eew947/sandia/QM-binding/basissets/def2tzvp/${element}_${basis1}.txt" >> "${working_dir}/${element}/${element}_water_opt.com"
    # write line for submitting job to gas_opt_jobs.txt
    job_line="cd ${working_dir}/${element} ; nohup g16 ${working_dir}/${element}/${element}_water_opt.com > ${working_dir}/${element}/${element}_water_opt.out &"
    echo "${job_line}" >> ${working_dir}/water_opt_jobs.txt
    echo "wait" >> ${working_dir}/water_opt_jobs.txt
done < element_list.txt


# will set up automation for submitting jobs on multiple nodes but for now will do manually
#echo "source ${g16_rc}" > ${working_dir}/gas_opt_jobs.txt
#%Mem=180GB
#MaxDisk=500GB
#node_list.txt



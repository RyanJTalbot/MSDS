#!/bin/bash

#SBATCH --ntasks=4
#SBATCH --output=weak_timing.txt


declare -a input=()
i=0
# reading file in row mode, insert each line into array
while IFS= read -r line; do
    input[i]=$line
    let "i++"
    # reading from file path
done < "weak_input.dat"

j=0
for i in 1 2 4
do
    mpiexec -np $i ./scale.fexe ${input[j]}
    let "j++"
done
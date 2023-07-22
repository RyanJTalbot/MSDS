#!/bin/bash
#SBATCH -N 4                      # Number of nodes
#SBATCH -o week2_hellompi.txt     # Output file for standard output
#SBATCH -t 30                     # Maximum run time in seconds

# Load the openmpi or mpich module (replace "module load" with the correct command for your system)
module load openmpi   # or module load mpich

# Compile the Fortran program
mpif90 hello_new.f90 -o hello_new

# Execute the program on 4 processes
mpirun -np 4 ./hello_new

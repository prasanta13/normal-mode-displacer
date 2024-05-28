from rw_xyz import read_xyz,write_xyz
from displace_coords import displace_coords 
from read_frequency import read_freq
import numpy as np
import os


####################################################
#    The section of parameters required comes here
####################################################
equ_xyz = 'equilibrium.xyz' # Equilibrium geometry

N = 3 #Number of geometries to generate
a = np.linspace(-0.5,0.5,N) #Range of distortion of geometries
freqcm1 = read_freq('g09/h2o.log') #Read the frequencies
print("The frequencies are",freqcm1)
Modes = [(mode + 1) for mode in range(len(freqcm1))] #selected modes
print("Modes = ",Modes)
nmodes = len(Modes)
print("Total number of modes = ",nmodes)
output_directory = 'test_xyz/'  # Directory for storing output files
# Create the output directory if it does not exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
####################################################
#               Parameters end here
####################################################

AtomList,R0,comment = read_xyz(equ_xyz)  # read starting coordinates
n_structure_count = 0
for j in range(N):  # loop N times
    print("-"*15)
    print('Step j =' + str(j+1))
    print("-"*15)
    D = R0  # Starting coordinates
    for i in range(nmodes):  # Loop over modes
        print("i = ",i)
        imode=Modes[i]  # Mode number
        #for k in a:
        Factor = a[j]
        print("Factor = ",Factor)
        print("Freqcm1",freqcm1[i])
        D = displace_coords(D,imode,freqcm1[i],Factor)	# Displace coordinates along mode 'imode' by 'Factor'
    n_structure_count += 1
    x = len(str(N))
    frmat = "%0" + str(x) + "d"
    fname = output_directory + str(frmat % (j+1))  + '.xyz'	# Output file name
    print("filename = ",fname)
    comment=' '  # comment on 2nd line of xyz file
    write_xyz(AtomList,D,fname,comment)  # write to xyz

####################################################
print(n_structure_count)
if n_structure_count != N:
    print("There is some error in the code")

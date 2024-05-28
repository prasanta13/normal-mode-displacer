from rw_xyz import read_xyz,write_xyz
from displace_coords import displace_coords 
import numpy as np
import os

####################################################
#    The section of parameters required comes here
####################################################
# Number of geometries to generate
N = 3
# Range of distortion of geometries
a = np.linspace(-0.5,0.5,N)
# Frequencies(cm-1) of selected modes [to be changed later for more automation]
freqcm1 = [1722.4496, 3799.4476, 3925.0128] 
# selected modes
Modes = [1,2,3]
print("Modes = ",Modes)
nmodes = len(Modes)
output_directory = 'test_xyz/'  # Directory for storing output files
# Create the output directory if it does not exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
####################################################
#               Parameters end here
####################################################

AtomList,R0,comment = read_xyz('equilibrium.xyz')  # read starting coordinates
n_structure_count = 0
for j in range(N):  # loop N times
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

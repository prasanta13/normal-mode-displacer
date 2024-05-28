from rw_xyz import read_xyz,write_xyz
from Z2m import Z2m
#from displace_coords import displace_coords 
from read_frequency import read_freq
import numpy as np
import os


####################################################
#    The section of parameters required comes here
####################################################
N = 20 #Number of geometries to generate
a = np.linspace(-0.5,0.5,N) #Range of distortion of geometries
normalmode_file = 'normalmodes_h2otrimer.txt'
equ_xyz = 'equilibrium_h2otrimer.xyz' # Equilibrium geometry
freqcm1 = read_freq(normalmode_file) #Read the frequencies
output_directory = 'test_xyz/'  # Directory for storing output files

# Only change the above parts
# Lower parts are for debugging

print("The frequencies are",freqcm1)
Modes = [(mode + 1) for mode in range(len(freqcm1))] #selected modes
print("Modes = ",Modes)
nmodes = len(Modes)
print("Total number of modes = ",nmodes)
# Create the output directory if it does not exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
####################################################
#               Parameters end here
####################################################


def displace_coords(Coords,imode,freqcm1,Factor):
    ##################################################
    # displace_coords: Displace coords from xyz file 'equilibrium.xyz' along mode 'imode' (0<int<=Nmode) by 'Factor' (float)
    # Inputs:	Coords (float list), coordinates as column vector with the format X1,Y1,Z1,X2,Y2,Z2,...
    #		imode (int), the coordinates are displaced along mode number 'imode'
    #		freqcm1 (float), the frequency in cm-1 of the mode
    # 		Factor (float), the coordinates are displaced along the mode by 'Factor' atomic units  
    # Outputs:	D (float list), displaced coordinates with same formatting as 'Coords'
    ##################################################

    Nat=len(Coords)/3				# Number of atoms 
    Displc=read_displacements(Nat,imode)		# Read normal mode displacements (vector of length 3*Nat)
    mi = Z2m(equ_xyz)
    D=[]
    for i in range( 3 * int(Nat) ):			# Loop over coordinates
        mass = mi[ int( (i - 1) / 3 ) ]  # int rounds down by default
        displacement_constant = (mass**.5 * 0.172*freqcm1**.5)**-1
        #extra_factor = 1e5*freqcm1**-3
        #D.append( Coords[i] + extra_factor * displacement_constant * Factor * Displc[i] ) 	# Displaced coordinates
        D.append( Coords[i] + displacement_constant * Factor * Displc[i] ) 	# Displaced coordinates
    ################################################## 
    return D


def read_displacements(Nat,imode):
    ##################################################
    # read_displacements: Reads displacement coordinates for mode 'imode' from 'normalmodes.txt'
    # Inputs: 	Nat (int), total number of atoms
    #		imode (int), the displacements are taken from mode number 'imode'
    # Outputs:	D (float list), single column of displacement coordinates (length 3*Nat)
    ##################################################
    # Definitions
    N = 3*Nat  # Number of coordinates
    # Error checks
    if Nat==2:
        Nmode=2
    elif Nat>2:
        Nmode=N-6
    else:
        print("ERROR: Something wrong with number of atoms")
        print("Are there <2 atoms?")
        return
 
    if imode>=1 and imode<=Nmode:
        pass
        #print "Reading displacements for mode " + str(imode)
    else:
        print('ERROR: imode out of range (1,Nmode).')
        return
    # Known pattern of g09 frequencies output file...
    row = int((imode-1)/5)
    a = (row+1)*7 + row*N
    b = (row+1)*(7 + N)
    d = row*5
    # Append displacements from file to column vector 'Displc'
    c=0
    Displc=[]
    with open(normalmode_file,'r') as f:
        for line in f:
            c+=1
            if c>a and c<=b:
                Displc.append(float(line.split()[imode+2-d]))
    ##################################################
    return Displc


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

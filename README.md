# normal\_mode\_displacer

** Forked from https://github.com/tnorthey/normal-mode-displacer **

## Description
Displace atomic coordinates along molecular normal modes. Works for any molecule with g09 freq=hpmodes and equilibrium.xyz starting geometry. Water is shown as an example below.

![watermodes](watermodes.gif)

## Requirements

- Gaussian quantum chemistry package
- python2.7 or python3

## How to use

### Files

1. equilibrium.xyz, the starting geometry.

2. normalmodes.txt, contains the normal modes from a Gaussian (g09) calculation with freq=hpmodes option enabled. This file can be generated easiy with bash. If you want contents between i and jth line of the gaussian output file, use, *sed -n 'i,jp' gaussian_output > normalmodes.txt*

3. run.py, run this to start generating randomly displaced geometries (xyz files).

### Functions

No need to edit these:

- displace\_coords.py, displace equilibrium.xyz coordinates along the normal modes 

- read\_displacements.py, read displacement factors from normalmodes.txt

- rw\_xyz.py, read or write xyz files 

- Z2m.py, converts between atom name (H,C,N,O, etc.) or atomic number to atomic mass

### Usage

First run a Gaussian (g09) calculation with "freq=hpmodes". Then manually extract the file 'normalmodes.txt' from the frequencies section of the .log file. Make sure 'equilibrium.xyz' is the starting geometry you want (probably the optimised geometry from the same .log file, but it doesn't have to be). 

Define the variables in `run.py':

```python
# Number of random geometries to generate
N = 100

# We are using a range of displacements along the normal modes. Within this range, the displacement will happen by total range/N number. It can be and done by a = np.linspace(-0.5,0.5,N). User please change the numbers according to their needs.

# frequencies (cm-1) of selected modes
freqcm1 = [1722.4496, 3799.4476, 3925.0128] 

# selected modes
Modes = [1,2,3] # For displacement of all modes
nmodes = len(freqcm1)

```

``N`` is the number of geometries that will be outputted, ``a`` defines the range of random displacement ``[-a,a]`` along each normal mode, ``freqcm1`` is a list of the frequencies of the normal modes in units cm-1, and ``nmodes`` is the number of normal modes to include, or you can specify which modes to include by the ``Modes`` list. The displacements are defined as,

```math 
xᵢ= x₀ + aΔxᵢ
```
for ``x₀`` the equilibrium geometry (from equilibrium.xyz), ``xᵢ`` the displaced geometry, and ``Δxᵢ`` the normal mode coordinate for mode ``i`` out of a total of ``nmodes``. 

Running the script,
```python
python run.py
```

produces ``N`` .xyz files in the xyz directory.

### Examples

Here, the water molecule is used as an example. The Gaussian files for water (input file and resulting log file) are in the g09 directory.
Water has 3 normal modes as shown in the image. They are "symmetric stretch", "bending", and "anti-symmetric stretch". 

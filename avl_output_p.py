'''
Created on 6 Mar 2018
This is the module that reads the results from file and produces the two output
'pressure.txt' and 'efficiency.txt'.
@author: Fabio C.
'''

import os
import numpy as np

from isa_atmosphere import IsaAtmosphere



# out_dir = os.path.join(os.getcwd(), 'OS')
# print(out_dir)

def get_efficiency(results, output_dir):
    '''
    This function reads the results.txt file generated by AVL and gives back
    the drag coefficient relative to the semi-wing.

    Parameters
    ----------
    results:         is the results.txt generated by AVL.
    output_dir:      is the output directory to save the files containing the 
                     pressure and the efficiency.

    Returns
    -------
    efficiency.txt :  is the file containing just the CD value.
    '''
    
    file_path = os.path.join(output_dir, results)
    f = open(file_path)
    content = f.readlines()
    content = [x.split() for x in content]
    
    #Eff = []
    file_path = os.path.join(output_dir, results)
    f = open(file_path)
    for i, line in enumerate(f):
        if line.startswith('  Forces referred to Ssurf, Cave'):
            Eff = content[i+1]
            break
    CL = float(Eff[2])
    CD = float(Eff[5])       
    eff = open(os.path.join(output_dir,'efficiency.txt'),'w')
    eff.write('{:6.5f}  {:6.5f}\n'.format(CL/2, CD/2))
    eff.close()


def get_pressure(results_file, output_dir, Mach, z):
    '''
    This function reads the results.txt file generated by AVL and containing the
    DCp distribution on the wing surface. Then it gives back the pressure 
    distribution (DP [Mpa]) which is later saved in a *.csv file for Optistruct.
    Before saving the pressure is corrected for compressibility according to the
    Prandtl-Glauert rule.

    Parameters
    ----------
    results_file:    in the input file containing the pressuresgenerated by AVL.
    output_dir:      is the output directory to save the files containing the 
                     pressure and the efficiency.
    Mach:            is the Mach number used for the compressibility correction.    
    z :              is the flight heigth in [m].

    Returns
    -------
    pressures.csv :  is the file containing the pressure values and the 
                     corresponding points. It is in csv format.
    '''
    
    '''
    Computing the dynamic pressure 'p_dyn' and the compressibility correction 
    'b'.
    '''
    flight_conditions = IsaAtmosphere(z)
    rho = flight_conditions.compute_density()
    c = flight_conditions.compute_sound_speed()
    p_dyn = 0.5 * rho * (Mach*c)**2
    b = np.sqrt(1-Mach**2)


    file_path = os.path.join(output_dir, results_file)
    f = open(file_path)
    content = f.readlines()
    content = [x.split() for x in content]

    DCp0 = []
    f = open(file_path)
    for i, line in enumerate(f):
        if line.startswith('    I        X           Y           '):
            for j in range(20):
                DCp0.append([float(val) for val in content[i+j+1]])
        elif line.startswith('  Surface # 2     wing (YDUP)'):
            break    
    
    vector = np.array(DCp0)
    vector[:,6] *= (p_dyn * 1e-6)
    vector[:,6] *= 1/b
    vector[:,1] *= 1000
    vector[:,2] *= 1000
       
    file = open(os.path.join(output_dir, 'pressure.csv'),'w')
    for k in range(len(vector)):
        file.write('{:.2f},{:.2f},{:.2f},{:5.4f}\n'.format(vector[k,1], vector[k,2], vector[k,3], vector[k,6]))
    file.close()    
    
    'In the file I write four columns. Which are respectively: x, y, z and DCp.'

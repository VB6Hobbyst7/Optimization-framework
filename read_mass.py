'''
Created on 15 Feb 2018
This is a simple script which read the mass value from the *.out file of OS and
write it on a text file called mass.txt.
@author: Fabio C.
'''
import os
import re

 
def read_mass(OUTfile, output_dir):
    '''
    This function reads, from bottom to top, the *.out file generated by OS and
    when it finds the string containing the MASS value it copies this value in a
    new file mass.txt .

    Parameters
    ----------
    OUTfile : is the file.out generated by OS during the analysis.

    Returns
    -------
    mass :    returns the mass value.
    

    '''
    local_path = os.path.join(output_dir,'mass.txt')
    mass = None
    regexp = re.compile(r'       1 MASS  Mass              --        2  SOLI   .*?([0-9E.-]+)')
    for line in reversed(list(open(OUTfile))):
        #print(line)
        match = regexp.match(line)
        #print(match)
        if match:
            mass = open(local_path,'w')
            mass.write(match.group(1))
            mass.close()
            break
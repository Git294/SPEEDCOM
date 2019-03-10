import numpy as np
import os
import pubchempy as pcp
import scipy.signal

from SPEEDCOM.models import utilities

"""
The data obtaining functions.  Please note that many of these functions
should only need to be run when training a new model.
"""

#DATA_DIR global variable containing the path to the data
def get_emission_files():
  """
  Get the total files containing emission spectra.  Expects the files to be of
  type *.ems.txt and have the naming convention *.ems.txt will return a list of
  strings to be parsed later.
  """
  return [fn for fn in os.listdir(DATA_DIR)
              if any(fn.endswith(.ems.txt))]

def get_absorption_files():
  """
  Get the total files containing absorption spectra.  Expects the files to be
  of type *.txt and have the naming convention *.abs.txt will return a list of
  strings to be parsed later.
  """
  return [fn for fn in os.listdir(DATA_DIR)
              if any(fn.endswith(.abs.txt))]

def get_molecule_cid(file_name):
  """ 
  Take a file_name, remove the ending and prefix and return the pubchem
  CID number.  If the file_name does not have the cas number, try the name
  of the system,   else return None so as to disreguard the molecule
  from training.
  """
  file = file_name.split("_")
  #try to get the cas # if not then try name.
  try:
    cas = file[1]
    pcp.get_compounds(cas, 'name')[0].cid

  except:
    pass

  #file doesn't have a cas number with it, try name
  try:
    cid = pcp.get_compounds[file[1], 'name'][0].cid

  #Couldn't determine name.
  except:
    cid = None

  return cid

def get_molecular_weight(cid):
  """
  Takes the PUBCHEM CID and returns the molecular weight as a float.
  """
  return pcp.Compound.from_cid(cid).molecular_weight

def get_molecular_smiles(cid):
  """
  Takes the PUBCHEM CID and returns the canonical SMILES string.
  """
  return pcp.Compound.from_cid(cid).canonical_smiles

def get_spectra(file_name):
  """
  Iterates through the file and pulls out the normalized spectrum contained
  within.  The X is in wavelentgh, and the intensity is normalized to the
  most intense peak.
  """
  spectra = []
  with open (file_name,'r') as file:
    next(file)
    for line in file:
      tmp = line.split()
      spectra.append([float(tmp[0]), float(tmp[1])])
  return np.asarray(spectra)

def get_peaks(spectra):
  peaks = []
  """
  This will take in the spectra from the get_spectra function and will return
  a list of [x,Y] coordinates for the peaks.
  """
  peak_locations = scipy.signal.find_peaks(spectra[:,1])[0]
  for i in peak_locations:
    peaks.append(spectra[i, :])
  return np.asarry(peaks)

def initiate_molecules():
  """
  Takes in the directory containing all of the data files and returns a list
  of populated molecule objects.
  """
  my_molecules = []
  #For all applicable emission spectra put properties into molecule objects,
  #and place objects into list for molecules.
  for ems_file in get_emission_files():
    cid = get_molecule_cid(ems_file) 
    if cid:
      spectra = get_spectra(ems_file)
      absorp = None
      columb = None
      emiss = get_peaks(spectra)
      smiles = get_molecular_smiles(cid)
      weight = get_molecular_weight(cid)
      my_molecules.append(molecule(absorp, cid, columb, emiss, smiles, weight))
    else:
      pass
  #For all applicable absorption spectra put properties into molecule objects,
  #and place objects into list for molecules.
  for abs_file in get_absorption_files():
    found = 0
    cid = get_molecule_cid(abs_file)
    #Check to see if the molecule already exists in the list, and if it does
    #does it already have valid absorption peaks:
    if cid:
      for mol in my_molecules:
        if mol.cid == cid:
          found = 1
          spectra = get_spectra(abs_file)
          mol.absorption_peaks = get_peaks(spectra)
          break
        else:
          pass
      if not found:
        spectra = get_spectra(abs_file)
        absorp = get_peaks(spectra)
        columb = None
        emiss = None
        smiles = get_molecular_smiles
        weight = get_molecular_weight(cid)
        my_molecules.append(molecule(absorp, cid, columb, emiss, smiles, \
          weight))
  return my_molecules
# Core.py below

#Location (relative) for the `DATA` directory
DATA_DIR = "../DATA"

class molecule:
  """
  The molecule class holds the information about the different molecules:
    * absorption_peaks: The absorption peaks (2D numpy array).
    * cid:              The PUBCHEM CID (float).
    * columb:           The columb matrix for the molecule.
    * emission_peaks:   The emission peaks (2D numpy array).
    * smiles:           The canonical SMILES string (string).
    * weight:           The molecular weight (float).
  """
  def __init__(absorp, cid, columb, emiss, smiles, weight):
    self.absorption_peaks = absorp
    self.cid = cid
    self.columb = columb
    self.emission_peaks = emiss
    self.smiles = smiles
    self.weight = weight

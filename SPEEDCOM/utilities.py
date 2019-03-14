import numpy as np
import pandas as pd
import os
import json
import NNModels
from NNModels import Descriptors
from rdkit import Chem

#import rdkit
#from rdkit import Chem
#from rdkit.Chem import AllChem
# from rdkit.ForceField.rdForceField import MMFFMolProperties as properties
# import rdkit.Chem.Draw as draw

def remove_deliminators(my_strings):
    """
    Remove deliminators from numbers (comma) so as
    to be able to process numbers as int or float types in place of
    strings.  Takes in 'my_array', an array of strings, and will return
    an array of floats.
    """
    my_array = []
    for i in my_strings:
        number = i
        if ',' in i:
            tmp = i.split(",")
            number = tmp[0] + tmp[1]
        try:
            my_array.append(float(number))
        except:
            print('String ' + i + ' not able to be cast to float, characters'
                  + " other than ',' or '.'?")
    return np.asarray(my_array)

def remove_cations(smiles):
    """
    Remove the 1st and 7th row cat/anions from the smiles strings.
    """
    split_smiles = smiles.split(".")
    ion_list = ['[Li+]', '[Na+]', '[K+]', '[Rb+]', '[Cs+]', '[Fr+]', '[F-]',
                '[Cl-]', '[Br-]', '[I-]', '[At-]']
    smiles = [i for i in split_smiles if i not in ion_list]
    smiles = '.'.join(smiles)
    return smiles

def draw_molecule(SMILES, filename):
    """
    Draws the 2D skeletal structure of a molecule using the rdkit
        package, returning the output to a file.

    Args:
    -----
        SMILES (str) -- a string representation of the molecule
        filename () --

    """
    # Assertions
    assert isinstance(SMILES, str), \
        'the SMILES must be a string'
    assert isinstance(filename, )

    # Functionality
    mol = Chem.MolFromSmiles(SMILES)
    Chem.Draw.MolToFile(mol, filename, kekulize=False)

    return

def get_l_max(wavelength_intensity):
    """
    args:
    wavelength_intensity -- np.array(2D), dtypes float64
    first column: wavelength; seconde column: intensity
    return:
    lambda_max(float)
    """
    wavelength_intensity.view('f8,f8').sort(order=['f1'], axis = 0)
    return wavelength_intensity[-1][0]

def get_em_max(clean_df, em_file_colname,prefix_dir):
    """
    from list of emission file names, get the lambda max from existing files
    and fill None if file not exist
    """
    from data_extract import get_spectra, get_peaks
    emission=[]
    for x in clean_df[em_file_colname].astype(str):#cast dtype to string
        if x != 'nan':
            em_max = get_l_max(get_peaks(get_spectra(os.path.join(prefix_dir, x))))
            emission.append(em_max)
        else:
            emission.append(None)
    return emission



def pad_ndarrays(input_dict):
    """
    Pads out all arrays in the given input dictionary of arrays
        with zeros so that they are all the same size and the largest input array.

    Args:
    -----
        input_dict (dict) -- input dictionary of arrays

    Returns:
    --------
        input_dict (dict) -- the modified input dictionary,
            where all arrays have been padded out.
    """
    # Assertions
    assert isinstance(input_dict, dict), \
        'Wrong Type: input must be a dictionary'
    # Functionality
    lens_of_arrays = []
    for array_i in input_dict.values():
        lens_of_arrays.append(len(array_i))

    max_len = max(lens_of_arrays)

    for array_i_key in input_dict.keys():
        array_i_len = len(input_dict[array_i_key])
        if(array_i_len < max_len):
            input_dict[array_i_key] = \
                np.pad(input_dict[array_i_key], (0, max_len-array_i_len),
                       'constant').tolist()

    return input_dict

def compute_fingerprints(df,SMILES_column='SMILES',key_name=None,radius=2,
                         nBits=2048, use_features=False, padding=True,
                         output_file=None):
    """
    Compute the fingerprints for an input dataframe with all the SMILES, and
    output the results as an dictionary with json txt format

    Args:
    -----
        df (pandas.DataFrame)  -- an input dataframe with SMILES info
        SMILES_column (str)    -- the column name of SMILES
        key_name (str)         -- the column name for output dict key
        radius (int)           --
        nBits (int)            -- maxium number of bits for fingerprints
                                  computation
        use_features (boolean) -- If True (default as False), use features to
                                  compute fingerprints
        padding (boolean)      -- If True (default), pad all the
            fingerprints to the maxium length in the dictionary
            with zeros
        output_file (str)     -- If None, return a dict. Otherwise
            returns a json .txt file of filename given by the string.
            
    Returns:
    --------
        fps_dict (dict)   --  an dictionary contains the fingerprints
                              key    -- name or index of the molecules
                              values -- a list of int
    """
    #Assertions
    assert isinstance(df, pd.DataFrame), \
        'Wrong Type: input df must be a pandas dataframe'
    assert isinstance(SMILES_column, str), \
        'Wrong Type: column names must be a strings'
    assert isinstance(key_name, (str, type(None))), \
        'Wrong Type: key name must be a string or NoneType'
    assert isinstance(radius, int), \
        'Wrong Type: radius must be an integer'
    assert isinstance(nBits, int), \
        'Wrong Type: number of bits must be an integer'
    assert nBits > 0, 'nBits must be a positive integer'
    assert isinstance(use_features, boolean), \
        'Wrong Type: padding must be a boolean'
    assert isinstance(padding, boolean), \
        'Wrong Type: padding must be a boolean'
    assert isinstance(output_file, (str, type(None))), \
        'Wrong Type: output_file must be a string or NoneType'

    # Initializing the descriptor engine:
    spD_engine = NNModels.Descriptors()

    fps_dict = {}
    for rowi_idx, rowi in df.iterrows():
        spD_engine.set_molecule(rowi[SMILES_column])
        rowi_fp = spD_engine.get_Morgan_fingerprint(radius,nBits,use_features)
        if(key_name is not None):
            rowi_idx = rowi[key_name]

        fps_dict[rowi_idx] = rowi_fp

    if(padding):
        pad_ndarrays(fps_dict)

    if(output_file is not None):
        with open(output_file, 'w') as f:
            f.write(json.dumps(fps_dict))
    else:
        return fps_dict

def compute_coulumb_matrixes(df,SMILES_column='SMILES', key_name=None, use_eigval=False,
                             eig_sort=True, padding=True, output_file=None):
    """
    Compute the fingerprints for an input dataframe with all the SMILES,
        and output the results as an dictionary with json txt format

    Args:
    -----
        df (pandas.DataFrame) -- an input dataframe with SMILES info
        SMILES_column (str)   -- the column name of SMILES
        key_name (str)        -- the column name for output dict key
        eig_sort (boolean)    -- If True (default), sort the coulomb
            matrixes with their eigenvalues.
        padding (boolean)     -- If True (default), pad all the coulomb
            matrices to the maxium length in the dictionary with zeros.
        output_file (str)     -- If None, return a dict. Otherwise,
            return a json txt file of the name given by the string.

    Returns:
    --------
        fps_dict (dict)   --  an dictionary whose values are the
            fingerprints of the molecules, and the keys are the index
            or names of the molecules.
    """
    #Assertions
    assert isinstance(df, pd.DataFrame), \
        'Wrong Type: input df must be a pandas dataframe'
    assert isinstance(SMILES_column, str), \
        'Wrong Type: column names must be a strings'
    assert isinstance(key_name, (str, type(None))), \
        'Wrong Type: key name must be a string or NoneType'
    assert isinstance(use_eigval, boolean), \
        'Wrong Type: use_eigval must be a boolean'
    assert isinstance(eig_sort, boolean), \
        'Wrong Type: eig_sort must be a boolean'
    assert isinstance(padding, boolean), \
        'Wrong Type: padding must be a boolean'
    assert isinstance(output_file, (str, type(None))), \
        'Wrong Type: output_file must be a string or NoneType'

    # Initializing the descriptor engine:
    spD_engine = NNModels.Descriptors()

    CMs_dict = {}
    for rowi_idx, rowi in df.iterrows():
        spD_engine.set_molecule(rowi[SMILES_column])
        # print(rowi_idx)
        # print(rowi[key_name])
        rowi_CM = spD_engine.get_coulomb_matrix(output_eigval=use_eigval)
        if(key_name is not None):
            rowi_idx = rowi[key_name]

        CMs_dict[rowi_idx] = rowi_CM

    if(padding):
        pad_ndarrays(CMs_dict)

    if(output_file is not None):
        with open(output_file, 'w') as f:
            f.write(json.dumps(CMs_dict))
    else:
        return CMs_dict

def compute_properties(df,SMILES_column='SMILES',index_name=None,
                       output_file=None):
    """
    Compute the fingerprints for an input dataframe with all the SMILES, and
    output the results as a csv txt file (exported by pandas)

    Args:
    -----
        df (pandas.DataFrame) -- an input dataframe with SMILES info
        SMILES_column (str)   -- the column name of SMILES
        index_name (str)      -- the index name for output DataFrame index
        output_file (str)     -- If None, return a dataframe
                                 Otherwise output an csv txt file.
    Returns:
    --------

    """
    #initilized the descriptor engine:
    spD_engine = Descriptors()

    prop_df = pd.DataFrame()
    for rowi_idx, rowi in df.iterrows():
        spD_engine.set_molecule(rowi[SMILES_column])
        rowi_prop = spD_engine.get_properties()
        if(index_name is not None):
            rowi_idx = rowi[index_name]

        rowi_prop = pd.DataFrame.from_dict(rowi_prop, orient='index',
                                           columns=[rowi_idx]).T

        prop_df = prop_df.append(rowi_prop)

    if(output_file is not None):
        prop_df.to_csv(output_file)
    else:
        return prop_df

def compute_features(df,SMILES_column='SMILES',key_name=None, output_file=None):
    """
    Compute the fingerprints for an input dataframe with all the SMILES, and
    output the results as a csv txt file (exported by pandas)

    Args:
    -----
        df (pandas.DataFrame) -- an input dataframe with SMILES info
        SMILES_column (str)   -- the column name of SMILES
        key_name (str)        -- the column name for output dict key
        output_file (str)     -- If None, return a dict
                                 Otherwise output an json txt file.
    Returns:
    --------
    """
    spD_engine = Descriptors()

    feats_dict = {}
    for rowi_idx, rowi in df.iterrows():
        spD_engine.set_molecule(rowi[SMILES_column])
        rowi_feat = spD_engine.get_features()
        if(key_name is not None):
            rowi_idx = rowi[key_name]

        feats_dict[rowi_idx] = rowi_feat

    if(output_file is not None):
        with open(output_file, 'w') as f:
            f.write(json.dumps(feats_dict))
    else:
        return feats_dict

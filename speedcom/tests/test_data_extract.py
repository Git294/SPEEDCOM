"""
Unit tests for the data_extract.py file
"""
import os
import unittest
import speedcom.tests.context as context
#import speedcom.speedcom

#Variables for testing
testing_dir = os.path.join(os.path.dirname(__file__), 'DATA_CLEAN_TEST_DIR/')
cid_test = "ZZZ_64-17-5_ethanol.txt"
name_test = "ZZZ_ethanol_ZZZ.txt"

# Unit tests
class get_emission_files(unittest.TestCase):
    def test_nonexistant_directory(self):
        """
        Tests that a non-existant directory returns an error.  Should be
        handeled by built in python os package.
        """
        self.assertRaises(Exception, lambda:context.data_extract.\
            get_emission_files("NONEXISTANTDIRECTORY"))

    def test_emission_files(self):
        """
        Tests the proper number of ems.txt files are returned.
        """
        assert len(context.data_extract.get_emission_files(testing_dir)) == 3,\
            'get_emission_files gets improper number of files'

class get_absorption_files(unittest.TestCase):
    def test_nonexistant_directory(self):
        """
        Tests that a non-existant directory returns an error.  Should be
        handeled by built in python os package.
        """
        self.assertRaises(Exception, lambda:context.data_extract.\
        get_absorption_files("NONXISTANTDIRECTORY"))

    def test_emission_files(self):
        """
        Tests the proper number of abs.txt files are returned.
        """
        assert len(context.data_extract.get_absorption_files(testing_dir)) == \
        3, 'get_emission_files gets improper number of files'

class get_molecule_cid(unittest.TestCase):
    def test_cid_from_cas(self):
        """
        Tests able to get CID from the cas number
        """
        assert context.data_extract.get_molecule_cid(cid_test).cid == 702, \
            'get_molecule_cid unable to ID from cid'
        return

    def test_cid_from_name(self):
        """
        Tests able to get CID from name
        """
        assert context.data_extract.get_molecule_cid(name_test).cid == 702, \
            'get_molecule_cid unable to ID from name'
        return

class get_spectra(unittest.TestCase):
    def test_proper_length(self):
        """
        Ensure returned spectrum is of the proper length
        """
        assert len(context.data_extract.get_spectra(testing_dir + \
        "1_118-96-7_X.abs.txt")) == 20, \
        "get_spectra returns spectum of improper size"
        return

class get_peaks(unittest.TestCase):
    def test_proper_length(self):
        """
        Ensure returned peak list is of appropriate size
        """
        spectra = context.data_extract.get_spectra(testing_dir + \
            "1_118-96-7_X.abs.txt")
        assert len(context.data_extract.get_peaks(spectra)) == 2, \
            'get_peaks retuns improper number of peaks'
        return

class electrostatic_potentials(unittest.TestCase):
    def test_valid_return_with_known(self):
        assert context.data_extract.electrostatic_potentials('acetic acid') \
            == 6.20, "electrostatic_potentils returns incorrect value"
        return

    def test_valid_return_unknown(self):
        assert context.data_extract.electrostatic_potentials("NOT MOLECULES")\
            == 1.0, "electrostatic_potentials unable to return for unknowns"
        return

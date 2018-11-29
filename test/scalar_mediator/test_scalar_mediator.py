"""
Test module for the scalar mediator model.
"""

from hazma.scalar_mediator import ScalarMediator
import numpy as np
import unittest

sm1_dir = 'Hazma/test/scalar_mediator/sm1_data/'
sm2_dir = 'Hazma/test/scalar_mediator/sm2_data/'


class TestScalarMediator(unittest.TestCase):

    def setUp(self):
        self.load_sm1_data()
        self.load_sm2_data()

        self.sm1 = ScalarMediator(**self.params1)
        self.sm2 = ScalarMediator(**self.params2)

    def tearDown(self):
        pass

    def load_sm1_data(self):
        """
        Loads in the data for the first scalar mediator object.

        Notes
        -----
        This is a Higgs portal-like model with:
            mx         = 250 MeV
            ms         = 550 Mev
            gsxx       = 1
            sin(theta) = 10^-3
            Lambda     = 246 GeV
        We aslo set the cme to:
            cme = 2 mx (1 + 0.5 v_rel^2)
        with v_rel = 10^-3.

        """
        self.params1 = np.load(sm1_dir + 'params.npy')[()]
        self.cme1 = np.load(sm1_dir + 'cme.npy')
        self.cs1_old = np.load(sm1_dir + 'ann_cross_sections.npy')[()]
        self.bf1_old = np.load(sm1_dir + 'ann_branching_fractions.npy')[()]
        self.vs1 = np.load(sm1_dir + 'vs.npy')
        self.spec1_old = np.load(sm1_dir + 'spectra.npy')[()]
        self.egams1 = np.load(sm1_dir + 'spectra_egams.npy')
        self.ps1_old = np.load(sm1_dir + 'partial_widths.npy')[()]
        self.eng_ps1 = np.load(sm1_dir + 'eng_ps.npy')
        self.pspec1_old = np.load(sm1_dir + 'positron_spectra.npy')[()]
        self.lns1_old = np.load(sm1_dir + 'ps_lines.npy')[()]

    def load_sm2_data(self):
        """
        Loads in the data for the second scalar mediator object.

        Notes
        -----
        This is a Higgs portal-like model with:
            mx         = 250 MeV
            ms         = 200 Mev
            gsxx       = 1
            sin(theta) = 10^-3
            Lambda     = 246 GeV
        We aslo set the cme to:
            cme = 2 mx (1 + 0.5 v_rel^2)
        with v_rel = 10^-3.

        """
        self.params2 = np.load(sm1_dir + 'params.npy')[()]
        self.cme2 = np.load(sm1_dir + 'cme.npy')
        self.cs2_old = np.load(sm1_dir + 'ann_cross_sections.npy')[()]
        self.bf2_old = np.load(sm1_dir + 'ann_branching_fractions.npy')[()]
        self.vs2 = np.load(sm1_dir + 'vs.npy')
        self.spec2_old = np.load(sm1_dir + 'spectra.npy')[()]
        self.egams2 = np.load(sm1_dir + 'spectra_egams.npy')
        self.ps2_old = np.load(sm1_dir + 'partial_widths.npy')[()]
        self.eng_ps2 = np.load(sm1_dir + 'eng_ps.npy')
        self.pspec2_old = np.load(sm1_dir + 'positron_spectra.npy')[()]
        self.lns2_old = np.load(sm1_dir + 'ps_lines.npy')[()]

    def test_description(self):
        """
        Test that the scalar mediator class desciption is working.
        """
        self.sm1.description()
        self.sm2.description()

    def test_list_final_states(self):
        """
        Test that the scalar mediator final state are equal to:
            'mu mu', 'e e', 'g g', 'pi0 pi0', 'pi pi', 's s'
        """
        list_fs = ['mu mu', 'e e', 'g g', 'pi0 pi0', 'pi pi', 's s']

        assert self.sm1.list_annihilation_final_states() == list_fs
        assert self.sm2.list_annihilation_final_states() == list_fs

    def test_cross_sections(self):
        """
        Test the scalar mediator cross sections for:
            'g g', 'e e', 'pi0 pi0', 'total', 's s', 'mu mu', 'pi pi'
        """
        cs1_new = self.sm1.annihilation_cross_sections(self.cme1)
        cs2_new = self.sm2.annihilation_cross_sections(self.cme2)

        for key in self.cs1_old.keys():
            assert np.isclose(self.cs1_old[key], cs1_new[key],
                              atol=0.0, rtol=1e-3)

        for key in self.cs2_old.keys():
            assert np.isclose(self.cs2_old[key], cs2_new[key],
                              atol=0.0, rtol=1e-3)

    def test_branching_fractions(self):
        """
        Test the scalar mediator branching fractions for:
            'g g', 'e e', 'pi0 pi0', 'total', 's s', 'mu mu', 'pi pi'
        """
        bf1_new = self.sm1.annihilation_branching_fractions(self.cme1)
        bf2_new = self.sm2.annihilation_branching_fractions(self.cme2)

        for key in self.bf1_old.keys():
            val1, val2 = self.bf1_old[key], bf1_new[key]
            assert np.isclose(val1, val2, atol=0.0, rtol=1e-3)

        for key in self.bf2_old.keys():
            val1, val2 = self.bf2_old[key], bf2_new[key]
            assert np.isclose(val1, val2, atol=0.0, rtol=1e-3)

    def test_compute_vs(self):
        """
        Test that the scalar mediator vev is correct.
        """
        assert self.sm1.compute_vs() == self.vs1
        assert self.sm2.compute_vs() == self.vs2

    def test_spectra(self):
        """
        Test the scalar mediator spectra for:
            'total', 'e e', 'pi0 pi0', 's s', 'mu mu', 'pi pi'
        """
        spec1_new = self.sm1.spectra(self.egams1, self.cme1)
        spec2_new = self.sm2.spectra(self.egams2, self.cme2)

        for key in self.spec1_old.keys():
            for (val1, val2) in zip(self.spec1_old[key], spec1_new[key]):
                assert np.isclose(val1, val2, atol=0.0, rtol=1e-3)

        for key in self.spec2_old.keys():
            for (val1, val2) in zip(self.spec2_old[key], spec2_new[key]):
                assert np.isclose(val1, val2, atol=0.0, rtol=1e-3)

    def test_spectrum_functions(self):
        self.sm1.spectrum_functions()
        self.sm2.spectrum_functions()

    def test_partial_widths(self):
        """
        Test the scalar mediator partial widths for:
            'x x', 'e e', 'pi0 pi0', 'total', 'g g', 'mu mu', 'pi pi'
        """
        ps1_new = self.sm1.partial_widths()
        ps2_new = self.sm2.partial_widths()

        for key in self.ps1_old.keys():
            val1, val2 = self.ps1_old[key], ps1_new[key]
            assert np.isclose(val1, val2, atol=0.0, rtol=1e-3)

        for key in self.ps2_old.keys():
            val1, val2 = self.ps2_old[key], ps2_new[key]
            assert np.isclose(val1, val2, atol=0.0, rtol=1e-3)

    def test_positron_spectra(self):
        """
        Test the positron spectra for:
            'total', 'mu mu', 'pi pi'
        """
        pspec1_new = self.sm1.positron_spectra(self.eng_ps1, self.cme1)
        pspec2_new = self.sm2.positron_spectra(self.eng_ps2, self.cme2)

        for key in self.pspec1_old.keys():
            for (val1, val2) in zip(self.pspec1_old[key], pspec1_new[key]):
                assert np.isclose(val1, val2, atol=0.0, rtol=1e-3)

        for key in self.pspec2_old.keys():
            for (val1, val2) in zip(self.pspec2_old[key], pspec2_new[key]):
                assert np.isclose(val1, val2, atol=0.0, rtol=1e-3)

    def test_positron_lines(self):
        """
        Test the positron lines for 'e e'.
        """
        lns1_new = self.sm1.positron_lines(self.cme1)
        lns2_new = self.sm2.positron_lines(self.cme2)

        assert np.isclose(
            lns1_new['e e']['bf'],  self.lns1_old['e e']['bf'],
            atol=0.0, rtol=1e-3)

        assert np.isclose(
            lns1_new['e e']['energy'], self.lns1_old['e e']['energy'],
            atol=0.0, rtol=1e-3)

        assert np.isclose(
            lns2_new['e e']['bf'], self.lns2_old['e e']['bf'],
            atol=0.0, rtol=1e-3)

        assert np.isclose(
            lns2_new['e e']['energy'], self.lns2_old['e e']['energy'],
            atol=0.0, rtol=1e-3)
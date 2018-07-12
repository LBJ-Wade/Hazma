from ..theory import Theory

from pseudo_scalar_mediator_parameters import PseudoScalarMediatorParameters

from pseudo_scalar_mediator_cross_sections import branching_fractions as bfs
from pseudo_scalar_mediator_cross_sections import cross_sections as cs

from pseudo_scalar_mediator_spectra import (dnde_mumu, dnde_ee, dnde_pi0pipi,
                                            dnde_pp)
from pseudo_scalar_mediator_spectra import spectra as specs
from pseudo_scalar_mediator_spectra import gamma_ray_lines as gls
from pseudo_scalar_mediator_positron_spectra import positron_spectra as pss
from pseudo_scalar_mediator_positron_spectra import positron_lines as pls

import warnings
from ..hazma_errors import PreAlphaWarning


class PseudoScalarMediator(Theory, PseudoScalarMediatorParameters):
    r"""
    Create a pseudoscalar mediator model object.
    """

    def __init__(self, mx, mp, gpxx, gpuu, gpdd, gpss, gpee, gpmumu, gpGG,
                 gpFF):
        super(PseudoScalarMediator, self).__init__(mx, mp, gpxx, gpuu, gpdd,
                                                   gpss, gpee, gpmumu, gpGG,
                                                   gpFF)

    def description(self):
        warnings.warn("", PreAlphaWarning)
        pass

    @classmethod
    def list_final_states(cls):
        """
        Return a list of the available final states.

        Returns
        -------
        fs : array-like
            Array of the available final states.
        """
        return ['e e', 'mu mu', 'g g', 'pi0 pi pi', 'p p']

    def cross_sections(self, cme):
        """
        Compute the all the cross sections of the theory.

        Parameters
        ----------
        cme : float
            Center of mass energy.

        Returns
        -------
        cs : dictionary
            Dictionary of the cross sections of the theory.
        """
        return cs(cme, self.params)

    def branching_fractions(self, cme):
        """
        Compute the branching fractions for two fermions annihilating through a
        psuedo-scalar mediator to mesons and leptons.

        Parameters
        ----------
        Q : float
            Center of mass energy.

        Returns
        -------
        bfs : dictionary
            Dictionary of the branching fractions.
        """
        return bfs(cme, self.params)

    def gamma_ray_lines(self, cme):
        return gls(cme, self)

    def spectra(self, egams, cme):
        """
        WARNING: This function is pre-alpha.

        Compute the total spectrum from two fermions annihilating through a
        vector mediator to mesons and leptons.

        Parameters
        ----------
        egams : array-like, optional
            Gamma ray energies to evaluate the spectrum at.
        cme : float
            Center of mass energy.

        Returns
        -------
        specs : dictionary
            Dictionary of the spectra
        """
        return specs(egams, cme, self.params)

    def spectrum_functions(self):
        """
        Returns a dictionary of all the avaiable spectrum functions for
        a pair of initial state fermions with mass `mx` annihilating into
        each available final state.

        Each argument of the spectrum functions in `eng_gams`, an array
        of the gamma ray energies to evaluate the spectra at and `cme`, the
        center of mass energy of the process.
        """
        return {'mu mu': lambda e_gams, cme: dnde_mumu(e_gams, cme, self),
                'e e': lambda e_gams, cme: dnde_ee(e_gams, cme, self),
                'pi0 pi pi': lambda e_gams, cme:
                    dnde_pi0pipi(e_gams, cme, self),
                'p p': lambda e_gams, cme:
                    dnde_pp(e_gams, cme, self)}

    def positron_spectra(self, eng_ps, cme):
        return pss(eng_ps, cme, self)

    def positron_lines(self, cme):
        return pls(cme, self)

    def constraints(self):
        pass

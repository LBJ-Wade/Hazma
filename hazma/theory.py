from .gamma_ray_limits.gamma_ray_limit_parameters import (A_eff_e_astrogam,
                                                          T_obs_e_astrogam,
                                                          dSph_params,
                                                          dPhi_dEdOmega_B_default)
from .gamma_ray_limits.compute_limits import compute_limit

import numpy as np
from scipy.interpolate import interp1d
from abc import ABCMeta, abstractmethod


class Theory(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def description(self):
        pass

    @abstractmethod
    def list_final_states(self):
        pass

    @abstractmethod
    def cross_sections(self, cme):
        pass

    @abstractmethod
    def branching_fractions(self, cme):
        pass

    @abstractmethod
    def spectra(self, eng_gams, cme):
        pass

    @abstractmethod
    def spectrum_functions(self):
        pass

    def compute_limit(self, n_sigma=5., A_eff=A_eff_e_astrogam,
                      T_obs=T_obs_e_astrogam, target_params=dSph_params,
                      dPhi_dEdOmega_B=dPhi_dEdOmega_B_default):
        """Computes smallest value of <sigma v> detectable for given target and
        experiment parameters.

        Notes
        -----
        We define a signal to be detectable if

        .. math:: N_S / sqrt(N_B) >= n_\sigma,

        where :math:`N_S` and :math:`N_B` are the number of signal and
        background photons in the energy window of interest and
        :math:`n_\sigma` is the significance in number of standard deviations.
        Note that :math:`N_S \propto \langle \sigma v \rangle`. While the
        photon count statistics are properly taken to be Poissonian and using a
        confidence interval would be more rigorous, this procedure provides a
        good estimate and is simple to compute.

        Parameters
        ----------
        dN_dE_DM : float -> float
            Photon spectrum per dark matter annihilation as a function of
            photon energy
        mx : float
            Dark matter mass
        dPhi_dEdOmega_B : float -> float
            Background photon spectrum per solid angle as a function of photon
            energy
        self_conjugate : bool
            True if DM is its own antiparticle; false otherwise
        n_sigma : float
            Number of standard deviations the signal must be above the
            background to be considered detectable
        delta_Omega : float
            Angular size of observation region in sr
        J_factor : float
            J factor for target in MeV^2 / cm^5
        A_eff : float
            Effective area of experiment in cm^2
        T_obs : float
            Experiment's observation time in s

        Returns
        -------
        <sigma v> : float
            Smallest detectable thermally averaged total cross section in units
            of cm^3 / s
        """
        # Create function to interpolate spectrum over energy window
        e_gams = np.logspace(np.log10(self.mx / 100.), np.log10(self.mx), 200)
        dN_dE_DM = interp1d(e_gams,
                            self.spectra(e_gams, 2.001*self.mx)["total"])

        return compute_limit(dN_dE_DM, self.mx, self_conjugate=False,
                             n_sigma, A_eff, T_obs, target_params,
                             dPhi_dEdOmega_B)

    def compute_limits(self, mxs, n_sigma=5., A_eff=A_eff_e_astrogam,
                       T_obs=T_obs_e_astrogam, target_params=dSph_params):
        """Computes gamma ray constraints over a range of DM masses.

        See documentation for :func:`compute_limit`.
        """
        limits = []

        for mx in mxs:
            self.mx = mx
            limits.append(self.compute_limit(n_sigma, A_eff, T_obs,
                                             target_params, dPhi_dEdOmega_B))

        return np.array(limits)

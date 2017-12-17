cimport decay_charged_pion
cimport decay_neutral_pion
import numpy as np
cimport numpy as np
from scipy.integrate import quad
from libc.math cimport sqrt
import cython
include "parameters.pxd"

"""
Module for computing the photon spectrum from radiative short kaon decay.

Description:
    The short kaon has many decay modes:

        ks -> pi + pi
        ks -> pi0 + pi0

    For the the two-body final states, the sum of the decay spectra are
    computed given the known energies of the final state particles in the
    kaon's rest frame. The spectrum is then boosted into the lab frame.
"""

""" Interpolating spectrum functions """
# Gamma ray energies for interpolating functions. Need a very low lower bound
# in order to no pass outside interpolation bounds when called from kaon decay.
__eng_gams_interp = np.logspace(-5.5, 3.0, num=10000, dtype=np.float64)

__spec_PiPi = decay_charged_pion.CSpectrum(__eng_gams_interp, MASS_K / 2.0)
__spec_PiPi += decay_charged_pion.CSpectrum(__eng_gams_interp, MASS_K / 2.0)

__spec_Pi0Pi0 = decay_neutral_pion.CSpectrum(__eng_gams_interp, MASS_K / 2.0)
__spec_Pi0Pi0 += decay_neutral_pion.CSpectrum(__eng_gams_interp, MASS_K / 2.0)


cdef double __interp_PiPi(double eng_gam):
    return np.interp(eng_gam, __eng_gams_interp, __spec_PiPi)

cdef double __interp_Pi0Pi0(double eng_gam):
    return np.interp(eng_gam, __eng_gams_interp, __spec_Pi0Pi0)


@cython.cdivision(True)
cdef double __integrand(double cl, double eng_gam, double eng_k):
    """
    Integrand for K -> X, where X is a any final state. The X's
    used are
        mu + nu
        pi  + pi0
        pi + pi + pi
        pi0 + mu + nu.
    When the ChargedKaon object is instatiated, the energies of the FSP are
    computed using RAMBO and energy distributions are formed. All the
    energies from the energy distributions are summed over against their
    weights.

    Keyword arguments::
        cl: Angle of photon w.r.t. charged kaon in lab frame.
        eng_gam: Energy of photon in laboratory frame.
        eng_k: Energy of kaon in laboratory frame.
    """
    cdef double gamma_k = eng_k / MASS_K
    cdef double beta_k = sqrt(1.0 - (MASS_K / eng_k)**2)
    cdef double eng_gam_k_rf = eng_gam * gamma_k * (1.0 - beta_k * cl)

    cdef int i, j
    cdef double ret_val = 0.0
    cdef double pre_factor \
        = 1.0 / (2.0 * gamma_k * (1.0 - beta_k * cl))

    ret_val += BR_KS_TO_PIPI * __interp_PiPi(eng_gam_k_rf)
    ret_val += BR_KS_TO_PI0PI0 * __interp_Pi0Pi0(eng_gam_k_rf)

    return pre_factor * ret_val



def SpectrumPoint(double eng_gam, double eng_k):
    """
    Returns the radiative spectrum value from charged kaon at
    a single gamma ray energy.

    Keyword arguments::
        eng_gam: Energy of photon is laboratory frame.
        eng_k: Energy of charged kaon in laboratory frame.
    """
    cdef double result = 0.0

    return quad(__integrand, -1.0, 1.0, points=[-1.0, 1.0], \
                  args=(eng_gam, eng_k), epsabs=10**-10., \
                  epsrel=10**-4.)[0]

@cython.boundscheck(False)
@cython.wraparound(False)
def Spectrum(np.ndarray[np.float64_t, ndim=1] eng_gams, double eng_k):
    """
    Returns the radiative spectrum dNde from charged kaon for a
    list of gamma ray energies.

    Keyword arguments::
        eng_gams: List of energies of photon in laboratory frame.
        eng_k: Energy of charged kaon in laboratory frame.
    """
    cdef double result = 0.0

    cdef int numpts = len(eng_gams)

    cdef np.ndarray spec = np.zeros(numpts, dtype=np.float64)

    cdef int i = 0

    for i in range(numpts):
        spec[i] = quad(__integrand, -1.0, 1.0, points=[-1.0, 1.0], \
                       args=(eng_gams[i], eng_k), epsabs=0.0, \
                       epsrel=10**-4.)[0]

    return spec
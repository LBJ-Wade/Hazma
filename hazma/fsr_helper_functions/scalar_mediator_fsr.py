"""Module for computing fsr spectrum from a scalar mediator.

@author - Logan Morrison and Adam Coogan.
@data - December 2017

"""
import numpy as np
import os

from ..parameters import vh, b0, alpha_em, fpi
from ..parameters import charged_pion_mass as mpi
from ..parameters import up_quark_mass as muq
from ..parameters import down_quark_mass as mdq

from ..field_theory_helper_functions.three_body_phase_space import u_to_st
from ..field_theory_helper_functions.three_body_phase_space import E1_to_s
from ..field_theory_helper_functions.three_body_phase_space import \
    phase_space_prefactor
from ..field_theory_helper_functions.three_body_phase_space import \
    t_integral

from ..field_theory_helper_functions.common_functions import \
    cross_section_prefactor

e = np.sqrt(4 * np.pi * alpha_em)


def fermion(eng_gam, cme, mass_f):
    """Return the fsr spectra for fermions from decay of scalar mediator.

    Computes the final state radiaton spectrum value dNdE from a scalar
    mediator given a gamma ray energy of `eng_gam`, center of mass energy `cme`
    and final state fermion mass `mass_f`.

    Paramaters
    ----------
    eng_gam : float
        Gamma ray energy.
    cme: float
        Center of mass energy of mass of off-shell scalar mediator.
    mass_f : float
        Mass of the final state fermion.

    Returns
    -------
    spec_val : float
        Spectrum value dNdE from scalar mediator.
    """
    val = 0.0

    if 0 < eng_gam and eng_gam < (cme**2 - 2 * mass_f**2) / (2 * cme):
        e, m = eng_gam / cme, mass_f / cme

        prefac = (4 * alpha_em) / (e * (1 - 4 * m**2)**1.5 * np.pi * cme)

        terms = np.array([
            2 * (-1 + 4 * m**2) *
            np.sqrt((1 - 2 * e) * (1 - 2 * e - 4 * m**2)),
            2 * (1 + 2 * (-1 + e) * e - 6 * m**2 + 8 * e * m**2 + 8 *
                 m**4) * np.arctanh(np.sqrt(1 - (4 * m**2) / (1 - 2 * e))),
            (1 + 2 * (-1 + e) * e - 6 * m**2 + 8 * e * m**2 + 8 * m**4) *
            np.log(1 + np.sqrt(1 - (4 * m**2) / (1 - 2 * e))),
            (-1 - 2 * (-1 + e) * e + 6 * m**2 - 8 * e * m**2 - 8 * m**4) *
            np.log(1 - np.sqrt(1 - (4 * m**2) / (1 - 2 * e)))
        ])

        val = np.real(prefac * np.sum(terms))

    return val


""" Charged Pion FSR """

# Set path for the unitarized squared matrix element for pi pi -> pi pi data
# file
DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "unitarization",
                         "final_state_int_unitarizated.dat")

# Load the data for the unitarized squared matrix element for pi pi -> pi pi.
unitarizated_data = np.genfromtxt(DATA_PATH, delimiter=',')


def unit_matrix_elem_sqrd(cme):
    """
    Returns the unitarized squared matrix element for :math:`\pi\pi\to\pi\pi`
    divided by the leading order, ununitarized squared matrix element for
    :math:`\pi\pi\to\pi\pi`.

    Parameters
    ----------
    cme : double
        Invariant mass of the two charged pions.

    Results
    -------
    unit_matrix_elem_sqrd : double
        The unitarized matrix element for :math:`\pi\pi\to\pi\pi`, |t_u|^2,
        divided by the un-unitarized squared matrix element for
        :math:`\pi\pi\to\pi\pi`, |t|^2; |t_u|^2 / |t|^2.
    """
    t_mod_sqrd = np.interp(cme, unitarizated_data[0], unitarizated_data[1])
    additional_factor = (2 * cme**2 - mpi**2) / (32. * fpi**2 * np.pi)
    return t_mod_sqrd / additional_factor**2


def __xx_to_s_pipig_mat_elem(s, t, Q, mx, ms, cxxs, cffs, cggs, vs):
    """
    Returns the squared matrix element for two fermions annihilating into two
    charged pions and a photon.

    Parameters
    ----------
    s : double
        Mandelstam variable associated with the photon, defined as (P-pg)^2,
        where P = ppip + ppim + pg.
    t : double
        Mandelstam variable associated with the charged pion, defined as
        (P-ppip)^2, where P = ppip + ppim + pg.
    Q : double
        Center of mass energy, or sqrt((ppip + ppim + pg)^2).
    mx : double
        Mass of the initial state fermion.
    ms : double
        Mass of the scalar mediator.
    cxxs : double
        Coupling of the initial state fermion to the scalar mediator.
    cffs : double
    cggs : double
        Coupling of the scalar to gluons.
    vs : double
        Vacuum expectation value of the scalar mediator.

    Returns
    -------
    Returns matrix element squared for
    :math:`\chi\bar{\chi}\to\pi^{+}\pi^{-}\gamma`.
    """
    u = u_to_st(0.0, mpi, mpi, Q, s, t)

    mat_elem_sqrd = (-16 * cxxs**2 *
                     (-4 * mx**2 + Q**2) *
                     (4 * mpi**6 - s * t * u + mpi**2 *
                         (t + u) * (s + t + u) - mpi**4 * (s + 4 * (t + u))) *
                     (2 * cggs * (4 * mpi**2 - s - t - u) *
                         (-9 * vh - 9 * cffs * vs + 2 * cggs * vs) *
                         (9 * vh + 8 * cggs * vs) +
                         b0 * (mdq + muq) * (9 * vh + 4 * cggs * vs) *
                         (54 * cggs * vh - 32 * cggs**2 * vs + 9 * cffs *
                          (9 * vh + 16 * cggs * vs)))**2 * e**2) / \
        ((ms**2 - Q**2)**2 *
         (mpi**2 - t)**2 * (mpi**2 - u)**2 *
         (9 * vh + 9 * cffs * vs - 2 * cggs * vs)**2 *
         (9 * vh + 4 * cggs * vs)**2 * (9 * vh + 8 * cggs * vs)**2)

    return mat_elem_sqrd * unit_matrix_elem_sqrd(np.sqrt(s))


def __xx_to_s_pipi_xsec(cme, mx, ms, cxxs, cffs, cggs, vs):
    """
    Returns the squared matrix element for two fermions annihilating into two
    charged pions.

    Parameters
    ----------
    cme : double
        Center of mass energy.
    mx : double
        Mass of the initial state fermion.
    ms : double
        Mass of the scalar mediator.
    cxxs : double
        Coupling of the initial state fermion to the scalar mediator.
    cffs : double
    cggs : double
        Coupling of the scalar to gluons.
    vs : double
        Vacuum expectation value of the scalar mediator.

    Returns
    -------
    Returns matrix element squared for :math:`\chi\bar{\chi}\to\pi^{+}\pi^{-}`.
    """
    mat_elem_sqrd = (-2 * cxxs**2 * (4 * mx**2 - cme**2) *
                     (2 * cggs * (2 * mpi**2 - cme**2) *
                      (-9 * vh - 9 * cffs * vs + 2 * cggs * vs) *
                      (9 * vh + 8 * cggs * vs) +
                      b0 * (mdq + muq) * (9 * vh + 4 * cggs * vs) *
                      (54 * cggs * vh - 32 * cggs**2 * vs + 9 * cffs *
                       (9 * vh + 16 * cggs * vs)))**2) / \
        ((ms**2 - cme**2)**2 *
         (9 * vh + 9 * cffs * vs - 2 * cggs * vs) ** 2 *
         (9 * vh + 4 * cggs * vs)**2 * (9 * vh + 8 * cggs * vs)**2)

    p_i = np.sqrt(cme**2 / 4.0 - mx**2)
    p_f = np.sqrt(cme**2 / 4.0 - mpi**2)

    prefactor = 1.0 / (16. * np.pi * cme**2) * p_f / p_i

    return prefactor * unit_matrix_elem_sqrd(np.sqrt(cme**2)) * mat_elem_sqrd


def __xx_to_s_pipig(eng_gam, cme, mx, ms, cxxs, cffs, cggs, vs):
    """
    Returns the gamma ray energy spectrum for two fermions annihilating into
    two charged pions and a photon.

    Parameters
    ----------
    eng_gam : double
        Gamma ray energy.
    cme : double
        Center of mass energy, or sqrt((ppip + ppim + pg)^2).
    mx : double
        Mass of the initial state fermion.
    ms : double
        Mass of the scalar mediator.
    cxxs : double
        Coupling of the initial state fermion to the scalar mediator.
    cffs : double
    cggs : double
        Coupling of the scalar to gluons.
    vs : double
        Vacuum expectation value of the scalar mediator.

    Returns
    -------
    Returns gamma ray energy spectrum for
    :math:`\chi\bar{\chi}\to\pi^{+}\pi^{-}\gamma`.
    """
    s = E1_to_s(eng_gam, 0.0, cme)

    def mat_elem_sqrd(t):
        return __xx_to_s_pipig_mat_elem(s, t, cme, mx, ms, cxxs,
                                        cffs, cggs, vs)

    prefactor1 = phase_space_prefactor(cme)
    prefactor2 = 2 * cme / \
        __xx_to_s_pipi_xsec(cme, mx, ms, cxxs, cffs, cggs, vs)
    prefactor3 = cross_section_prefactor(mx, mx, cme)

    prefactor = prefactor1 * prefactor2 * prefactor3

    int_val, err = t_integral(s, 0.0, mpi, mpi, cme,
                              mat_elem_sqrd=mat_elem_sqrd)

    return prefactor * int_val, err


def xx_to_s_pipig(eng_gams, cme, mx, ms, cxxs, cffs, cggs, vs):
    """
    Returns the gamma ray energy spectrum for two fermions annihilating into
    two charged pions and a photon.

    Parameters
    ----------
    eng_gam : numpy.ndarray or double
        Gamma ray energy.
    cme : double
        Center of mass energy, or sqrt((ppip + ppim + pg)^2).
    mx : double
        Mass of the initial state fermion.
    ms : double
        Mass of the scalar mediator.
    cxxs : double
        Coupling of the initial state fermion to the scalar mediator.
    cffs : double
    cggs : double
        Coupling of the scalar to gluons.
    vs : double
        Vacuum expectation value of the scalar mediator.

    Returns
    -------
    Returns gamma ray energy spectrum for
    :math:`\chi\bar{\chi}\to\pi^{+}\pi^{-}\gamma` evaluated at the gamma ray
    energy(ies).
    """
    if hasattr(eng_gams, '__len__'):
        return [__xx_to_s_pipig(eng_gam, cme, mx, ms, cxxs, cffs, cggs, vs)
                for eng_gam in eng_gams]
    else:
        __xx_to_s_pipig(eng_gam, cme, mx, ms, cxxs, cffs, cggs, vs)

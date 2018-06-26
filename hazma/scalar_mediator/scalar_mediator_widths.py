from cmath import sqrt, pi

from ..parameters import vh, b0, alpha_em
from ..parameters import charged_pion_mass as mpi
from ..parameters import neutral_pion_mass as mpi0
from ..parameters import up_quark_mass as muq
from ..parameters import down_quark_mass as mdq
from ..parameters import electron_mass as me
from ..parameters import muon_mass as mmu


def width_s_to_gg(params):
    """
    Returns the partial decay width of the scalar decaying into photon.
    """
    return ((alpha_em**2 * (5.*params.gsFF/3.)**2 * (params.ms**2)**1.5) /
            (512. * pi**3 * vh**2))


def width_s_to_pi0pi0(params):
    """
    Returns the partial decay width of the scalar decaying into
    neutral pions.
    """
    ms = params.ms

    if ms > 2. * mpi0:
        gsff = params.gsff
        gsGG = params.gsGG
        vs = params.vs

        ret_val = (sqrt(-4 * mpi0**2 + ms**2) *
                   (-162 * gsGG * (2 * mpi0**2 - ms**2) * vh *
                    (3 * vh + 3 * gsff * vs + 6 * gsGG * vs) +
                    b0 * (mdq + muq) * (9 * vh + 12 * gsGG * vs) *
                    (162. * gsGG * vh - 288 * gsGG**2 * vs +
                     9 * gsff * (9 * vh + 48 * gsGG * vs)))**2) / \
            (11664. * ms**2 * pi * vh**2 *
             (3 * vh + 3 * gsff * vs + 6 * gsGG * vs)**2 *
             (9 * vh + 12 * gsGG * vs)**2)

        assert ret_val.imag == 0
        assert ret_val.real >= 0

        return ret_val
    else:
        return 0.


def width_s_to_pipi(params):
    """
    Returns the partial decay width of the scalar decaying into
    charged pion.
    """
    ms = params.ms

    if ms > 2. * mpi:
        gsff = params.gsff
        gsGG = params.gsGG
        vs = params.vs

        ret_val = (sqrt(-4 * mpi**2 + ms**2) *
                   (-162 * gsGG * (2 * mpi**2 - ms**2) * vh *
                    (3 * vh + 3 * gsff * vs + 6 * gsGG * vs) +
                    b0 * (mdq + muq) * (9 * vh + 12 * gsGG * vs) *
                    (162 * gsGG * vh - 288 * gsGG**2 * vs +
                     9 * gsff * (9 * vh + 48 * gsGG * vs)))**2) / \
            (11664. * ms**2 * pi * vh**2 *
             (3 * vh + 3 * gsff * vs + 6 * gsGG * vs)**2 *
             (9 * vh + 12 * gsGG * vs)**2)

        assert ret_val.imag == 0
        assert ret_val.real >= 0

        return ret_val
    else:
        return 0.


def width_s_to_xx(params):
    """
    Returns the partial decay width of the scalar decaying into
    two fermions x.
    """

    ms = params.ms
    mx = params.mx

    if ms > 2. * mx:
        gsxx = params.gsxx

        ret_val = (gsxx**2 * (ms - 2 * mx) * (ms + 2 * mx) *
                   sqrt(ms**2 - 4 * mx**2)) / (32. * ms**2 * pi)

        assert ret_val.imag == 0
        assert ret_val.real >= 0

        return ret_val
    else:
        return 0.0


def width_s_to_ff(mf, params):
    """
    Returns the partial decay width of the scalar decaying into
    two fermions x.

    Parameters
    ----------
    mf : double
        Mass of the final state fermion.
    """
    ms = params.ms

    if ms > 2. * mf:
        gsff = params.gsff

        ret_val = -(gsff**2 * mf**2 * (2 * mf - ms) * (2 * mf + ms) *
                    sqrt(-4 * mf**2 + ms**2)) / (32. * ms**2 * pi * vh**2)

        assert ret_val.imag == 0
        assert ret_val.real >= 0

        return ret_val
    else:
        return 0.


def partial_widths(params):
    """
    Returns a dictionary for the partial decay widths of the scalar
    mediator.

    Returns
    -------
    width_dict : dictionary
        Dictionary of all of the individual decay widths of the scalar
        mediator as well as the total decay width. The possible decay
        modes of the scalar mediator are 'g g', 'pi0 pi0', 'pi pi', 'x x' and
        'f f'. The total decay width has the key
        'total'.
    """
    w_gg = width_s_to_gg(params).real
    w_pi0pi0 = width_s_to_pi0pi0(params).real
    w_pipi = width_s_to_pipi(params).real
    w_xx = width_s_to_xx(params).real

    w_ee = width_s_to_ff(me, params).real
    w_mumu = width_s_to_ff(mmu, params).real

    total = w_gg + w_pi0pi0 + w_pipi + w_xx + w_ee + w_mumu

    width_dict = {'g g': w_gg,
                  'pi0 pi0': w_pi0pi0,
                  'pi pi': w_pipi,
                  'x x': w_xx,
                  'e e': w_ee,
                  'mu mu': w_mumu,
                  'total': total}

    return width_dict

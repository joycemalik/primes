import math

import primewaves as pw


def close(a, b, tol):
    assert abs(a - b) <= tol, f"{a} is not within {tol} of {b}"


def test_primes():
    assert len(pw.primes(100)) == 25
    assert len(pw.primes(100_000)) == 9592


def test_prime_wave_exact_up_to_p_squared():
    assert pw.prime_wave(97, 7) == 0
    assert pw.prime_wave(98, 7) > 0
    good, bad = pw.wave_survivors(200, 7)
    assert bad[0] == 121
    assert all(n > 49 for n in bad)


def test_z_arrow_prime_powers():
    for n in (2, 7, 9, 16, 25):
        close(abs(pw.z_arrow(n)), 1, 1e-12)
    assert abs(abs(pw.z_arrow(6)) - 1) > 1e-6


def test_gamma_and_zeta():
    close(pw.gamma(5).real, 24, 1e-9)
    close(pw.zeta(2).real, math.pi ** 2 / 6, 1e-12)
    close(pw.zeta(-1).real, -1 / 12, 1e-10)
    close(abs(pw.zeta(complex(0.5, pw.ZETA_ZEROS[0]))), 0, 1e-5)
    z = pw.zeta(complex(0.5, 30))  # mpmath: -0.12064229 - 0.58369121i
    close(z.real, -0.12064229, 1e-7)
    close(z.imag, -0.58369121, 1e-7)


def test_explicit_formula():
    close(pw.psi_explicit(30.5, 1000), pw.psi(30.5), 0.6)


def test_robin_and_cipolla():
    assert pw.sigma(12) == 28
    assert pw.robin_ratio(5040) > pw.ROBIN_BOUND
    assert pw.robin_ratio(10080) < pw.ROBIN_BOUND
    close(pw.nth_prime_estimate(100_000) / 1_299_709, 1, 0.001)

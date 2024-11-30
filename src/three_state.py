import numpy as np


def get_roots(
        a: float,
        b: float,
        c: float,
        d: float,
) -> tuple(float, float, float):
    """
    Returns roots of the equation
    a*x^3 + b*x^2 + c*x + d = 0
    """
    delta0 = b**2 - 3*a*c
    delta1 = 2 * b**2 - 9 * a * b * c + 27 * a**2 * d
    theC = pow(0.5 * (delta1 + pow(delta1**2 - 4 * delta0**3, 0.5)), 1/3)
    unity_root3 = 0.5 * (-1 + 1j * pow(3, 0.5))
    x0 = -(b + theC + delta0/theC)/(3*a)
    x1 = -(b + unity_root3**1 * theC + delta0/(unity_root3**1 * theC))/(3*a)
    x2 = -(b + unity_root3**2 * theC + delta0/(unity_root3**2 * theC))/(3*a)
    return x0, x1, x2


def get_eigenvalues(
        q: float,
        energyA: float,
        energyB: float,
        energyC: float,
        lambdaAB: float,
        lambdaAC: float,
) -> tuple(float, float, float):
    """ Return eigenvalues of the matrix
    energyA + q * kappa1A + q**2 * kappa2A & lambdaAB * q & lambdaAC * q \\
    lambdaAB * q & energyB + q * kappa1B + q**2 kappa2B & 0 \\
    """
    kappa1A = 0.0
    kappa2A = 0.0
    kappa1B = 0.0
    kappa2B = 0.0
    kappa1C = 0.0
    kappa2C = 0.0
    hamiltonian: np.ndarray = np.array([
        [energyA + kappa1A * q + kappa2A * q, lambdaAB*q, lambdaAC*q],
        [lambdaAB * q, energyB + kappa1B * q + kappa2B * q, 0],
        [lambdaAC * q, 0,  energyC + kappa1C * q + kappa2C * q],
    ])
    trace = hamiltonian.trace()
    sum_minors = 0
    determinant = hamiltonian
    a = -1
    b = trace
    c = -sum_minors
    d = determinant

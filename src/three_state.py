import numpy as np

NUMERICAL_ZERO = 1e-10

def get_roots(
        a: float,
        b: float,
        c: float,
        d: float,
) -> tuple[float, float, float]:
    """
    Returns roots of the equation
    a*x^3 + b*x^2 + c*x + d = 0
    """
    # print("Characteristic equation:")
    # print(f"{a:.0f} x**3 + {b:.0f} x**2 + {c:.0f} x + {d:.0f} = 0")
    delta0 = b**2 - 3*a*c
    delta1 = 2 * b**2 - 9 * a * b * c + 27 * a**2 * d
    tmp0 = delta1**2 + 4 * delta0**3
    if tmp0 < 0:
        theC = pow(0.5 * (delta1 + 1j * pow(-tmp0, 0.5)), 1/3)
    else:
        theC = pow(0.5 * (delta1 + pow(tmp0, 0.5)), 1/3)
    unity_root3 = 0.5 * (-1 + 1j * pow(3, 0.5))
    x0 = -(b + theC + delta0/theC)/(3*a)
    x1 = -(b + unity_root3**1 * theC + delta0/(unity_root3**1 * theC))/(3*a)
    x2 = -(b + unity_root3**2 * theC + delta0/(unity_root3**2 * theC))/(3*a)
    # if abs(x0.imag) > NUMERICAL_ZERO:
    #     raise RuntimeError(f"Non-real root of a symmetric matrix: {x0=}")
    # if abs(x1.imag) > NUMERICAL_ZERO:
    #     raise RuntimeError(f"Non-real root of a symmetric matrix: {x1=}")
    # if abs(x2.imag) > NUMERICAL_ZERO:
    #     raise RuntimeError(f"Non-real root of a symmetric matrix: {x2=}")
    return x0, x1, x2

#     return x0.real, x1.real, x2.real


def get_sum_of_minors(matrix: np.ndarray) -> np.dtype:
    """
    works only for a matrix of the shape
    | a  g  f |
    | g  b  0 |
    | f  0  c |
    and returns
    det |b 0|  + det |a f|  + det |a g|
        |0 c|        |f c|        |g b|
    But does not check if that is the case
    """
    if matrix.ndim != 2:
        raise ValueError("Only 3x3 matrices are supported.")

    # TODO: check if square
    if matrix.size != 9:
        raise ValueError("Only 3x3 matrices are supported.")

    sum = matrix[1][1] * matrix[2][2]  # bc

    sum += matrix[0][0] * matrix[2][2]  # ac
    sum -= matrix[0][2] * matrix[2][0]  # f^2

    sum += matrix[0][0] * matrix[1][1]  # ab
    sum -= matrix[0][1] * matrix[1][0]  # g^2

    return sum


def get_eigenvalues(
        q: float,
        energyA: float,
        energyB: float,
        energyC: float,
        lambdaAB: float,
        lambdaAC: float,
) -> tuple[float, float, float]:
    """ Return eigenvalues of the matrix
    energyA + q * kappa1A + q**2 * kappa2A & lambdaAB * q & lambdaAC * q \\
    lambdaAB * q & energyB + q * kappa1B + q**2 kappa2B & 0 \\
    """
    kappa1A = 0.0
    kappa2A = 600
    kappa1B = 0.0
    kappa2B = 600
    kappa1C = 0.0
    kappa2C = 600
    hamiltonian: np.ndarray = np.array([
        [energyA + kappa1A * q + kappa2A * q, lambdaAB*q, lambdaAC*q],
        [lambdaAB * q, energyB + kappa1B * q + kappa2B * q, 0],
        [lambdaAC * q, 0,  energyC + kappa1C * q + kappa2C * q],
    ])
    trace = hamiltonian.trace()
    sum_minors = get_sum_of_minors(hamiltonian)
    determinant = np.linalg.det(hamiltonian)
    roots = get_roots(a=-1, b=trace, c=-sum_minors, d=determinant)
    return roots

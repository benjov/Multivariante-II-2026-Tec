"""Análisis factorial en numpy/scipy: adecuación, estimación, rotación y puntuaciones.

Módulo compartido del curso de Análisis Multivariante (capítulo 3 de las notas).
Uso desde un cuaderno en una subcarpeta de dos niveles:
    import sys; sys.path.insert(0, "../../utils")
    import factorial as fa
"""
import numpy as np
from scipy import optimize, stats


# ---------------------------------------------------------------- adecuación
def bartlett_esfericidad(R, n):
    """Prueba de esfericidad de Bartlett: H0: P = I. Devuelve (estadístico, gl, p)."""
    p = R.shape[0]
    est = -(n - 1 - (2 * p + 5) / 6) * np.log(np.linalg.det(R))
    gl = p * (p - 1) / 2
    return est, gl, stats.chi2.sf(est, gl)


def correlaciones_parciales(R):
    """Matriz de correlaciones parciales (cada par, dadas las demás variables)."""
    Om = np.linalg.inv(R)
    d = np.sqrt(np.diag(Om))
    A = -Om / np.outer(d, d)
    np.fill_diagonal(A, 1.0)
    return A


def kmo(R):
    """Medida KMO global y MSA por variable."""
    A = correlaciones_parciales(R)
    r2 = R ** 2
    a2 = A ** 2
    np.fill_diagonal(r2, 0)
    np.fill_diagonal(a2, 0)
    global_ = r2.sum() / (r2.sum() + a2.sum())
    msa = r2.sum(0) / (r2.sum(0) + a2.sum(0))
    return global_, msa


# ---------------------------------------------------------------- estimación
def fa_componentes(R, m):
    """Método de componentes principales: L = G_m Lambda_m^{1/2}."""
    lam, G = np.linalg.eigh(R)
    lam, G = lam[::-1], G[:, ::-1]
    return G[:, :m] * np.sqrt(lam[:m])


def fa_ejes_principales(R, m, tol=1e-8, max_iter=1000):
    """Ejes principales iterados, con comunalidades iniciales = R^2 múltiple (SMC)."""
    h2 = 1 - 1 / np.diag(np.linalg.inv(R))
    for it in range(max_iter):
        Rr = R.copy()
        np.fill_diagonal(Rr, h2)
        lam, G = np.linalg.eigh(Rr)
        lam, G = lam[::-1][:m], G[:, ::-1][:, :m]
        L = G * np.sqrt(np.clip(lam, 0, None))
        h2_new = (L ** 2).sum(1)
        if np.max(np.abs(h2_new - h2)) < tol:
            return L, it + 1
        h2 = h2_new
    return L, max_iter


def _L_dado_psi(R, psi, m):
    """Para Psi fija, la L que maximiza la verosimilitud (Lawley)."""
    s = 1 / np.sqrt(psi)
    Rs = R * np.outer(s, s)                 # Psi^{-1/2} R Psi^{-1/2}
    lam, G = np.linalg.eigh(Rs)
    lam, G = lam[::-1][:m], G[:, ::-1][:, :m]
    return np.sqrt(psi)[:, None] * G * np.sqrt(np.clip(lam - 1, 0, None))


def discrepancia_mv(R, L, psi):
    """F = log|Sigma| + tr(R Sigma^{-1}) - log|R| - p."""
    Sig = L @ L.T + np.diag(psi)
    p = R.shape[0]
    return (np.linalg.slogdet(Sig)[1] + np.trace(R @ np.linalg.inv(Sig))
            - np.linalg.slogdet(R)[1] - p)


def fa_maxima_verosimilitud(R, m):
    """Máxima verosimilitud: minimiza F sobre Psi (perfilando L)."""
    p = R.shape[0]
    h2 = 1 - 1 / np.diag(np.linalg.inv(R))
    f = lambda psi: discrepancia_mv(R, _L_dado_psi(R, psi, m), psi)
    res = optimize.minimize(f, 1 - h2, method="L-BFGS-B", bounds=[(0.005, 1)] * p)
    psi = res.x
    return _L_dado_psi(R, psi, m), psi, res.fun


def prueba_ajuste_mv(F, n, p, m):
    """Prueba chi-cuadrada de Bartlett para H0: m factores bastan."""
    est = (n - 1 - (2 * p + 5) / 6 - 2 * m / 3) * F
    gl = ((p - m) ** 2 - p - m) / 2
    return est, gl, stats.chi2.sf(est, gl)


# ---------------------------------------------------------------- rotación
def varimax(L, normalizar=True, tol=1e-10, max_iter=1000):
    """Rotación varimax (Kaiser). Devuelve (L rotada, matriz de rotación T)."""
    p, m = L.shape
    h = np.sqrt((L ** 2).sum(1)) if normalizar else np.ones(p)
    A = L / h[:, None]
    T = np.eye(m)
    d_old = 0
    for _ in range(max_iter):
        B = A @ T
        U, s, Vt = np.linalg.svd(A.T @ (B ** 3 - B @ np.diag((B ** 2).sum(0)) / p))
        T = U @ Vt
        d = s.sum()
        if d - d_old < tol * d:
            break
        d_old = d
    return (A @ T) * h[:, None], T


def promax(L, k=4):
    """Rotación oblicua promax. Devuelve (patrón, correlación entre factores)."""
    Lv, _ = varimax(L)
    P = np.abs(Lv) ** k * np.sign(Lv)              # objetivo
    U = np.linalg.lstsq(Lv, P, rcond=None)[0]
    U = U * np.sqrt(np.diag(np.linalg.inv(U.T @ U)))[None, :]   # factores con varianza 1
    patron = Lv @ U
    Phi = np.linalg.inv(U.T @ U)
    return patron, Phi


def varimax_criterio(L):
    """Valor del criterio varimax (suma de varianzas de cargas al cuadrado normalizadas)."""
    h2 = (L ** 2).sum(1, keepdims=True)
    B = L ** 2 / h2
    return ((B ** 2).mean(0) - B.mean(0) ** 2).sum()


# ---------------------------------------------------------------- puntuaciones
def puntuaciones_regresion(Z, R, L):
    """Método de regresión (Thomson): F = Z R^{-1} L."""
    return Z @ np.linalg.solve(R, L)


def puntuaciones_bartlett(Z, L, psi):
    """Mínimos cuadrados ponderados (Bartlett): F = Z Psi^{-1} L (L' Psi^{-1} L)^{-1}."""
    Pi = np.diag(1 / psi)
    return Z @ Pi @ L @ np.linalg.inv(L.T @ Pi @ L)


def alfa_cronbach(X):
    """Alfa de Cronbach de los reactivos (columnas de X)."""
    k = X.shape[1]
    return k / (k - 1) * (1 - X.var(0, ddof=1).sum() / X.sum(1).var(ddof=1))

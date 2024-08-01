import numpy as np
import scipy.integrate as integrate
import scipy.optimize as optimize
from math import exp
from math import sin


def M(n, q):
    """
    мат. ожидание
    :param n:
    :param q:
    :return:
    """
    return n*q**2


def sko(n, q):
    """
    среднеквадратичное отклонение
    :param n:
    :param q:
    :return:
    """
    return np.sqrt(n*q**2)


def src_func(x):
    """
    Подинтегральная экспонента
    :param x:
    :return:
    """
    return exp(-x**2)


def erf(x):
    """
    аналог erf из Mathcad
    :param x:
    :return:
    """
    return 2./np.sqrt(np.pi)*integrate.quad(src_func, 0, x)[0]


def Phi(x):
    """
    Интеграл вероятности
    :param x:
    :return:
    """
    return 0.5*(1+erf(x/np.sqrt(2.)))


def eq_fun(x, *args):
    """
    функция корень которой ищем
    :param x:
    :return:
    """
    return 1-Phi(x/sko(args[0], args[1]))-args[2]


def lp0(n, q, F):
    """
    порог обнаружения
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.root_scalar.html#scipy.optimize.root_scalar
    :param n:
    :param q:
    :param F: порог F
    :return:
    """
    res = optimize.root_scalar(f=eq_fun, args=(n, q, F), bracket=[-15, 15], x0=0., method='newton')
    return res.root

def find_root_sin():

    res  = optimize.root_scalar(f=sin,bracket=[-15,15],x0=2., method='newton'  )
    return res
    
def D(n, q, F):
    """
    Характеристика обнаружения
    :param n:
    :param q:
    :param F:
    :return:
    """
    return 1 - Phi((lp0(n, q, F)-M(n, q))/sko(n, q))

def D0(n, q, F):
    """
    Характеристика обнаружения. Пропуск полезного сигнала
    :param n:
    :param q:
    :param F:
    :return:
    """
    return 1 - D(n, q, F)

def eq_fun_F(x, *args):
    """
    функция, корень которой ищем для графиков с F
    :param x:
    :return:
    """
    return 1-Phi((x-M(args[0], args[1]))/sko(args[0], args[1]))-args[2]
def lp0_F(n, q, DD):
    """
    порог обнаружения для графиков с F
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.root_scalar.html#scipy.optimize.root_scalar
    :param n:
    :param q:
    :param DD: порог D
    :return:
    """
    print(q)
    res = optimize.root_scalar(f=eq_fun_F, args=(n, q, DD),bracket=[-2,10000],x0=2., method='brentq')
    return res.root
def F1(n, q, DD):
     """
     Характеристика обнаружения
     :param n:
     :param q:
     :param DD:
     :return:
     """
     return 1 - Phi(lp0_F(n, q, DD)/sko(n, q))

if __name__ == "__main__":
    pass
    # print(lp0_F(1,30.2,0.75))
   

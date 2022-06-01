from typing import Callable
import numpy as np
from numpy import ndarray

'''
This is from a previous project, I'm trying to reuse code
'''


def RK4(model: Callable[[float, ndarray], ndarray], state_prev: ndarray, t_now: float, t_step: float):
    '''
    Range-Kutta 4\nIntegra o estado `state_prev` pelo modelo `model`
    no passo `t_now` até o passo `t_now + t_step`
    '''
    len = 3
    state_prev = np.ravel(state_prev)
    state_prev = np.reshape(state_prev, (len, 1))

    k1: ndarray = model(t_now, state_prev)
    k2: ndarray = model(t_now+t_step/2., state_prev + (k1 * t_step/2.))
    k3: ndarray = model(t_now+t_step/2., state_prev + (k2 * t_step/2.))
    k4: ndarray = model(t_now+t_step, state_prev + k3 * t_step)
    k: ndarray = (1/6)*(k1 + 2*k2 + 2*k3 + k4)

    delta_state: ndarray = (k * t_step)
    state_next:  ndarray = state_prev + delta_state

    return state_next

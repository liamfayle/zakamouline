
import numpy as np
import sys
sys.path.append('../BSM')
from bsm import BsmOption, OptionPosition
from copy import deepcopy


def getH0(lambda_, gamma_lower, spot, sigma, time):
    '''
    lambda_     -> Proportional transaction cost where "tc = lambda_ * spot * numShares" \n
    gamma_lower -> Risk aversion parameter \n
    spot        -> Spot price \n
    sigma       -> BSM Volatility \n
    time        -> BSM time value \n
    '''
    return lambda_ / (gamma_lower * spot * sigma**2 * time)


def getH1(lambda_, time, r, sigma, gamma_upper, gamma_lower):
    '''
    lambda_     -> Proportional transaction cost where "tc = lambda_ * spot * numShares" \n
    time        -> BSM time value \n
    r           -> risk free rate used in BSM \n
    sigma       -> BSM Volatility \n
    gamma_upper -> BSM Gamma \n
    gamma_lower -> Risk aversion parameter \n
    '''
    return 1.12 * lambda_**0.31 * time**0.05 * (np.exp(-r*time)/sigma)**0.25 * (np.abs(gamma_upper) / gamma_lower)**0.5


def getK(lambda_, time, r, sigma, gamma_lower, spot, gamma_upper):
    '''
    lambda_     -> Proportional transaction cost where "tc = lambda_ * spot * numShares" \n
    time        -> BSM time value \n
    r           -> risk free rate used in BSM \n
    sigma       -> BSM Volatility \n
    gamma_lower -> Risk aversion parameter \n
    spot        -> Spot price \n
    gamma_upper -> BSM Gamma \n
    '''
    return -4.76 * (lambda_**0.78 / time **0.02) * (np.exp(-r*time)/sigma)**0.25 * (gamma_lower * spot**2 * np.abs(gamma_upper))**0.15


def getSigmaModified(sigma, k, isLong):
    '''
    sigma  -> BSM volatility \n
    k      -> Adjustment parameter calculated using getK() \n
    isLong -> true if long option, false if short option \n
    '''
    if isLong:
        return np.sqrt(sigma**2 * (1 + k))
    else:
        return np.sqrt(sigma**2 * (1 - k))


def hedgebands(position, lambda_, gamma_lower):
    '''
    NOTE [1] Since taking position as argumenet if if single option it must be added to a position object \n
    NOTE [2] Since getting first leg and using params['isLong'] will not work for spreads that are not either ALL long or ALL short (ie straddle would be fine but short condor would fail) \n

    TODO Fix note 2  \n

    @Params position - OptionPosition Position\n
            lambda_ - proportional tracnsaction cost where "tc = lambda_ * spot * numShares" \n
            gamma_lower - risk aversion param \n
    @Return h_plus - positive delta hedge band \n
            h_neg  - negative delta hedge band \n

            Note option sigma is not changed (is reset in func)
    '''

    params = position.getLeg(0).params
    k = getK(lambda_, params['T'], params['r'], position.sigma(), gamma_lower, params['S'], position.gamma())
    h0 = getH0(lambda_, gamma_lower, params['S'], position.sigma(), params['T'])
    h1 = getH1(lambda_, params['T'], params['r'], position.sigma(), position.gamma(), gamma_lower)

    position_copied = deepcopy(position)
    sigma_m = getSigmaModified(position.sigma(), k, params['isLong']) #Applies to NOTE 2
    position_copied.updateSigma(sigma_m)
    h_plus = position_copied.delta() + (h1 + h0)
    h_neg = position_copied.delta() - (h1 + h0)

    return h_plus, h_neg

import numpy as np


def run_experiment(i,j, pars=None, add_noise=False):
    # to be changed: genereate all data here
    X=[i,j]
    np.random.seed(2)
    if not pars:
        x0 = np.random.randn(1)[0]*15+45.5
        y0 = np.random.randn(1)[0]+4.0
        fwhm = np.random.normal(loc=7.5,scale=5, size=100).mean()
    else:
        x0, y0, fwhm = pars
        
    func = 10*np.exp(-4*np.log(2) * ((X[0]-x0)**2 + (X[1]-y0)**2) / fwhm**2) + 5*np.exp(-4*np.log(2) * ((X[0]-x0+7)**2 + (X[1]-y0+2)**2) / fwhm**2) 
    
    if add_noise:
        func = add_noise_func(func)
    
    return func

def add_noise_func(input_data, mean_noise=2):
    # incomplete: refactor code to generate data + noise in one function
    avg_data = np.mean(input_data)
    noise_ = np.random.normal(mean_noise, np.sqrt(avg_data), 1)[0]
    output_data = input_data + noise_
    
    return output_data
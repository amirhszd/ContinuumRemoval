# ContinuumRemoval
[![DOI](https://zenodo.org/badge/180401442.svg)](https://zenodo.org/badge/latestdoi/180401442)

The Continuum Removal approach, applied by [Kokaly and Clark](https://www.sciencedirect.com/science/article/pii/S0034425798000844), enhances absorption features in spectroscopic measurements. This approach is extensively used in regression-type problems and attributes 

The repository requires 'numpy' and 'matplotlib' library and runs smoothly in 'Python 3.X'.

**How it works**

The algorithm takes in spectra of samples, the wavelength vector, and the feature regions user is interested in. 

Feature regions is a list of either numpy arrays of specified wavelengths or length-two tuples (start,end).

The algorithm is a class with a set of functions as below:

- _Continuum_Removal(spectra, wavelength, feature_regions)_: inputs are spectra, wavelengths vector and specified feauture regions either as a list of tuples or a list of numpy arrays.
- _find_near(wl_region)_: finds nearest wavlengths based on the given wavelength region or point
- _R_value(spectra,wl_region)_ identifies reflectance values based on a given wavelength point or region
- _slope_intercept(spectra,wl_region)_ specifies slope and intercept of a spectra based on a given wavelength region
- _cont_rem()_: calculates the continuum removed spectra based on inputs
- _plot_spectra(self)_: plots all given spectra
- _plot_cr(self)_: plots all continuum removed curves


![Figure_1](https://user-images.githubusercontent.com/35879739/55817654-fa3d7e00-5ac2-11e9-8ea7-ad92065d12d5.png)
![Figure_2](https://user-images.githubusercontent.com/35879739/55817655-fa3d7e00-5ac2-11e9-9b79-bbfacdf825ae.png)

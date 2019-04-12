# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 13:09:30 2019

@author: Amirh
"""

import numpy as np
import matplotlib.pyplot as plt
#%%


class continuum_removal:
    """
    Spectra vector:
        should be MxN matrix where M is the number of samples and N is the number of features.
    
    WL_vector:
        is the wavelength vector. flattened array, N number of elements.
    
    feature_regions:
        regions where user is interested in applying the continuum removal to.
        
    
    The output is a continuum removed vector based on number of samples and 
    regions.
    """

    def __init__(self,spectra,wl_vector,feature_regions):
        self.spectra = spectra

        if len(wl_vector)==1:
            self.wl = np.squeeze(wl_vector)
        else:
            self.wl = wl_vector
       
        for i in feature_regions:
            if type(i) is not np.ndarray and type(i) is not tuple:
                raise Exception("Each wavelength region should either be an array or a tuple(start,end)")
            else:
                self.feature_regions = feature_regions                  
    # this function find the nearest wavelength values to a given wavelength
    # region or wavelength end estimates values 
    def find_near(self,wl_region):
        """
        this function find the nearest wavelength values to a given wavelength
        region or wavelength end estimates values 

        """
        if isinstance(wl_region, tuple) or type(wl_region) is np.ndarray:
            LL = self.wl[np.argsort(np.abs(wl_region[0]-self.wl))[0]]
            UL = self.wl[np.argsort(np.abs(wl_region[-1]-self.wl))[0]]
            return self.wl[np.where(self.wl==LL)[0][0]:np.where(self.wl==UL)[0][0]+1]
        elif isinstance(wl_region, int) or isinstance(wl_region, float):
            point = self.wl[np.argsort(np.abs(wl_region-self.wl))[0]]
            return self.wl[np.where(self.wl==point)[0][0]]
        else:
            raise Exception("Entered feature region should either be a list of length-two tuples (start,end) or a list of arrays.")
        
    # this function will give out reflectance value of each spectra, given a 
    # wavelength region or wavelength end estimates values     
    def R_value(self,spectra,wl_region):     
        """
        This function finds the reflectance value, given a wavelegnth region 
        and spectra        
        """
        if isinstance(wl_region, tuple) or type(wl_region) is np.ndarray:
            axis=self.find_near(wl_region)
            LL_index = np.where(self.wl==axis[0])[0][0] #lower level index of spectra
            UL_index = np.where(self.wl==axis[-1])[0][0] #upper level index of spectra
            return spectra[LL_index:UL_index+1]    
        # or if given just one value 
        elif isinstance(wl_region, int) or isinstance(wl_region, float): 
            axis= self.find_near(wl_region)
            index= np.where(self.wl==axis)[0][0]
            return spectra[index]

        else:
            raise Exception("Entered feature region should either be a list of length-two tuples (start,end) or a list of arrays.")
        
        
    def slope_intercept(self,spectra,wl_region):
        """ 
        this function finds the slope and the intercept of a linear fit over
        the selected regions
        """
        x1 = self.find_near(wl_region)[0]  
        y1 = self.R_value(spectra,x1)
        x2 = self.find_near(wl_region)[-1]
        y2 = self.R_value(spectra,x2)
        slope = (y2-y1)/(x2-x1)
        intercept = y2 - slope*x2
        return slope,intercept
    
    # obtaining the continuum removed line from the given spectra
    def cont_rem(self):
        """
        This function calculates the continuum removed spectra by dividing the 
        fit lines by the original spectra
        """
        self.curve = []
        if len(self.spectra) > 1:
            for j in self.spectra:
                spectrum_curve=[]
                for region in self.feature_regions:
                   s,i =self.slope_intercept(j,region)
                   spectrum_curve.append(self.R_value(j,region)/(self.find_near(region)*s+i))
                self.curve.append(spectrum_curve)
        else:
            for region in self.feature_regions:
               s,i =self.slope_intercept(self.spectra,region)
               self.curve.append(self.R_value(self.spectra,region)/(self.find_near(region)*s+i))
            
        return self.curve
    
    def plot_spectra(self):
        """
        this function simply plots the original spectras
        """
        fig,ax=plt.subplots(nrows=1,ncols=1,figsize=(12,8))
        ax.plot(self.wl,self.spectra.T)
        ax.set_xlabel(r"Wavelength $(nm)$")
        ax.set_ylabel(r"Reflectance")
        ax.set_title("Spectra")
        ax.set_xlim(self.wl[0],self.wl[-1])
        ax.grid(True)
        return ax
        
    def plot_cr(self):
        """
        this function plots the continuum removed line of all spectra
        """
        fig,ax=plt.subplots(nrows=1,ncols=1,figsize=(12,8))
        count = 0
        for i in self.curve:
            color = np.random.rand(3,)
            for j in i:
                ax.plot(self.find_near(self.feature_regions[count]),j,c=color)
                count += 1
                if count == len(i):
                    count = 0                
        ax.set_xlabel(r"Wavelength $(nm)$")
        ax.set_ylabel(r"Reflectance")
        ax.set_title("Continuum Removed Spectra")
        ax.set_xlim(self.wl[0],self.wl[-1])
        ax.grid(True)
        return ax


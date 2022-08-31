import pandas as pd
import numpy as np 
from sklearn.impute import SimpleImputer

class PreproG():
    
    def __init__(self, DataFrame):
        self.frame = DataFrame
        self.mrks = self.frame.MRK.tolist()
        self.CHR = self.frame.CHR.tolist()
        self.MAF = self.frame.MAF.tolist()
        self.VALUES = self.frame.iloc[:, 3:].values
        self.GENOS_codes = self.frame.iloc[:, 3:].columns.tolist()
        self.GENOS_n = len(self.GENOS_codes)
        self.value = {self.mrks[index]:array for index, array in enumerate(self.VALUES)}
        

    def cut(self, values):
        self.frame = self.frame.drop(values, axis=0).reset_index(drop = True)
        self.mrks = self.frame.MRK.tolist()
        self.MAF = self.frame['MAF'].tolist()
        self.CHR = self.frame.CHR.tolist()
        self.VALUES = self.frame.iloc[:, 3:].values
        self.GENOS_codes = self.frame.iloc[:, 3:].columns.tolist()
        self.GENOS_n = len(self.GENOS_codes)
        self.value = {self.mrks[index]:array for index, array in enumerate(self.VALUES)}
        
    def cut_by_miss_frq (self, missing_data = None, numeric = False ,frq = 50, apply = False):
        my_markers = []
        for index , array in enumerate(np.array(list(self.value.values()))):
            if not numeric:
                perct = 100*(list(array).count(missing_data)/self.GENOS_n)
            else:
                perct = 100*(np.count_nonzero(np.isnan(array))/self.GENOS_n)  
            if perct >= frq:
                my_markers.append(index)
        if apply:
            self.cut(my_markers)
        else:
            return my_markers
    
    def cut_by_MAF(self, frq = 1, numeric = False, coef_pl = 2, MA = None, apply = False):
        my_markers = []
        for index , array in enumerate(np.array(list(self.value.values()))):
            value_to_inspect = MA if numeric else self.MAF[index]*coef_pl
            if not numeric:
                perct = 100*(list(array).count(value_to_inspect)/self.GENOS_n)
            else:
                perct = 100*(np.count_nonzero(array == value_to_inspect)/self.GENOS_n)
                
            if perct <= frq:
                my_markers.append(index)
        if apply:
            self.cut(my_markers)
        else:
            return my_markers

    def impute (self, strategy = 'mean', structure = 'array'):
        df = self.frame.iloc[:, 3:].T
        array = df.values
        imp_method = SimpleImputer(missing_values = np.nan, strategy=strategy)
        IMP = imp_method.fit_transform(array)
        if structure == 'DF':
            df = pd.DataFrame(IMP, index = self.GENOS_codes, columns = self.mrks)
            return df
        
        return IMP
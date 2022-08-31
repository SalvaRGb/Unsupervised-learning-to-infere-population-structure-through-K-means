
from abc import ABC, abstractmethod

class HapMap(ABC):
    
    common_atributes = [
                        'rs#', 
                        'alleles', 
                        'chrom', 
                        'pos', 
                        'strand', 
                        'assembly#', 
                        'center',
                        'protLSID', 
                        'assayLSID', 
                        'panelLSID', 
                        'QCcode'
                        ]
    
    IUPAC = {
            'A':'A',
            'C':'C',
            'G':'G',
            'T':'T',
            'R': 'AG', 
            'Y':'CT', 
            'K': 'GT', 
            'M': 'AC', 
            'S':'CG', 
             'W': 'AT', 
             'B':'CGT', 
             'D':'AGT', 
             'H':'ACT', 
             'V':'ACG', 
             'N':'ACGT', 
             '.':'gap', 
             '-':'gap'
             }       
    
    def __init__(self, DataFrame, ploidy_level = 2):
        
        self.ploidy_level = ploidy_level# by default 2
        self.frame = DataFrame
        
        self.none_biallelic_index, self.none_biallelic_markers = [], []
        for index, variants in enumerate(self.frame['alleles']):
            if len(''.join([SNP for SNP in variants if SNP in 'ACGT'])) !=2:
                self.none_biallelic_index.append(index)
                self.none_biallelic_markers.append(self.frame['rs#'][index])
        self.frame = self.frame.drop(self.none_biallelic_index, axis=0).reset_index(drop=True)   
        
        self.SNP_tag = self.frame['rs#'].tolist()
        self.SNP_n = len(self.frame['rs#'])
        self.CHR = self.frame['chrom'].unique().tolist()
        self.GENOS_codes = [genotypes for genotypes in self.frame.columns if genotypes not in HapMap.common_atributes]
        self.GENOS_n = len(self.GENOS_codes)
        self.VARIANTS_more_freq = {self.SNP_tag[ix] :[x for x in variants if x.isalpha()][0] for ix, 
                                   variants in enumerate(self.frame['alleles'])}
        self.VARIANTS_less_freq = {self.SNP_tag[ix] :[x for x in variants if x.isalpha()][-1] for ix, 
                                   variants in enumerate(self.frame['alleles'])}
        
        for i, v in enumerate(self.frame.columns):
            if v not in HapMap.common_atributes:
                self.first_geno = i
                break
                
        self.VALUES = {self.frame['rs#'][indx]: array for indx, array in enumerate(self.frame.iloc[:, self.first_geno:].values)}
        self.describe_density = {chrom: len(self.frame[self.frame['chrom'] == chrom]['chrom']) for chrom in self.CHR}
        
        self.AF = {}                  
        for k, v in self.VALUES.items():
            self.AF[k] = {code: list(v).count(code)/self.GENOS_n for code in np.unique(v)}
    
    @abstractmethod
    def Homozygous(self):
        pass
    
    @abstractmethod
    def Heterozygous(self):
        pass
#-------------------------------------------------------------------------------------------------
class MarkerS(HapMap):
    
    def __init__(self, DataFrame):
            super().__init__(DataFrame)
            self.value = np.array(list(self.VALUES.values()))
            self.type = self.value.dtype
            
    def Homozygous(self, numeric = False, interval_hm = [-1,1], ploidy = True,
                   output_format = 'd_', missing_data = None, add_index = True):
       
        if missing_data == None:
            missing_data = np.nan if numeric else ''
        pseudo_matrix = {}
        coef_pl = self.ploidy_level if ploidy else 1
        
        for index, array in enumerate(list(self.VALUES.values())):
            codes = [code for code in self.frame['alleles'][index] if code in 'ACGT']
            map_values = {}
            
            if numeric:
                code_values = dict(zip(codes, interval_hm))
                map_values = {code: float(code_values[code]) if code in code_values else missing_data for code in list(self.AF.values())[index]}  
            else:
                map_values = {code: code*coef_pl if code in codes else missing_data for code in list(self.AF.values())[index]}
            pseudo_matrix[self.SNP_tag[index]] = np.vectorize(map_values.get)(array)

        if numeric:
            self.value = np.array(list(pseudo_matrix.values())).astype('float16')
            self.type = self.value.dtype
        else:
            self.value = np.array(list(pseudo_matrix.values())).astype('unicode')
            self.type = self.value.dtype
            
        if output_format == 'DF':
            return pd.DataFrame.from_dict(pseudo_matrix, orient='index',columns=self.GENOS_codes)
        return pseudo_matrix
    
    def Heterozygous(self, frq = 0, extend_range = 2, numeric = False, 
                     n_value = 0, output_format = 'd_', missing_data = None, any_base = False):
        if missing_data == None:
            missing_data = np.nan if numeric else ''
        pseudo_matrix = {}       
        for index, array in enumerate(list(self.VALUES.values())):
            freq_s = list(self.AF.values())[index]
            map_values =  {}
            ht_variant = ''.join([code for code in self.frame['alleles'][index] if code in 'ACGT'])
            ht_variant = ht_variant if ht_variant in HapMap.IUPAC.values() else ht_variant[::-1]
            codes_per_row = np.unique(array)
            for code in codes_per_row:
                try:   
                    if freq_s[code]>=frq:
                        if ((ht_variant[0] and ht_variant[1]) in HapMap.IUPAC[code]):
                            if not any_base:
                                if code != 'N':
                                    if 1< len(HapMap.IUPAC[code]) <= extend_range:
                                        map_values[code] = float(n_value) if numeric else ht_variant
                                    else:
                                        map_values[code] = missing_data
                                else:
                                    map_values[code] = missing_data
                            else:
                                if 1< len(HapMap.IUPAC[code]) <= extend_range or code == 'N':
                                    map_values[code] = float(n_value) if numeric else ht_variant
                                else:
                                    map_values[code] = missing_data
                        else:
                            map_values[code] = missing_data
                    else:
                        map_values[code] = missing_data
                except KeyError as err:
                    map_values[code] = missing_data
            pseudo_matrix[self.SNP_tag[index]] = np.vectorize(map_values.get)(array)
            
        if numeric:
            self.value = np.array(list(pseudo_matrix.values())).astype('float16')
            self.type = self.value.dtype
        else:
            self.value = np.array(list(pseudo_matrix.values())).astype('unicode')
            self.type = self.value.dtype
            
        if output_format == 'DF':
            return pd.DataFrame.from_dict(pseudo_matrix, orient='index',columns=self.GENOS_codes)
        return pseudo_matrix
   
    def collapse(self, Marker_g_object, output_format = 'd_', replace_missing = []):
        if self.type == 'float16':
            config_type = True
            combine = np.where(np.isnan(self.value), Marker_g_object.value, self.value + np.nan_to_num(Marker_g_object.value))
        else:
            combine = np.core.defchararray.add(self.value, Marker_g_object.value)
            
        if replace_missing:
            old, new = replace_missing[0], replace_missing[1]
            combine = np.where(combine == old, new, combine)
        
        if output_format == 'd_':
            return {self.SNP_tag[i]:v for i, v in enumerate(combine)}
        my_df = pd.DataFrame(data = combine, index = self.SNP_tag, columns = self.GENOS_codes)
        my_df.reset_index(inplace = True)
        my_df.rename(columns={'index':'MRK'}, inplace = True)
        my_df.insert(1, 'CHR', self.frame['chrom'].tolist())
        my_df.insert(2, 'MAF', list(self.VARIANTS_less_freq.values()))
        
        return my_df
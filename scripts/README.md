
## **Whatis a HapMap file, description about the format and datatype:**

The Hapmap Project was initiated in 2001 by the International HapMap Consortium. Its database is freely available to the public through the NCBI database dbSNP. The Project is also described at Nature 426 :789-796, 2003 [PMID: 14685227]. The file format estabilished through the project is also used in others projects and **species** (* such as plant species and commonly used in the construction of genetic arrays with SNP markers for GWAS analysis*).
The Hapmap file format is a table which consists of 11 columns plus one column for each sample genotyped. The first row contains the header labels of your samples, and each additional row contains all the information associated with a single SNP. You can get a Hapmap file by chromosome or a general file.

Therefore, the HapMap files are structured following an stantard format containing the following attributes:

- **rs#** contains the SNP identifier;
- **alleles** contains SNP alleles according to NCBI database dbSNP;
- **chrom** contains the chromosome that the SNP was mapped;
- **pos** contains the respective position of this SNP on chromosome;
- **strand** contains the orientation of the SNP in the DNA strand. Thus, SNPs could be in the forward (+) or in the reverse (-) orientation relative to the reference genome;
- **assembly#** contains the version of reference sequence assembly (from NCBI);
- **center** contains the name of genotyping center that produced the genotypes;
- **protLSID** contains the identifier for HapMap protocol;
- **assayLSID** contain the identifier HapMap assay used for genotyping;
- **panelLSID** contains the identifier for panel of individuals genotyped;
- **QCcode** contains the quality control for all entries;
**subsequently, the list of sample names**.

**SNP** follows the **IUPAC** system for nucleotide codification:

| Nucleotide | Common display | Meaning |
| :---: | :---: | :---: |
| A | A | Adenine |
| C | C | Cytosine |
| G | G | Guanine |
| T (or U) | T | T (or U) (Thyamine or Uracile)|
| R | A/G | A or G |
| Y | C/T | C or T (or U) |
| K | G/T | G or T (or U) |
| M | A/C | A or C |
| S | C/G | C or G |
| W | A/T | A or T |
| B | C/G/T | Not A; C, G, T or U |
| D | A/G/T | Not C; A, G, T or U  |
| H | A/C/T | Not G; C, A, T or U  |
| V | A/C/G | Not T or U; C, G, A  |
| N | A/C/G/T | any base |
| . or - | - | Gap of indeterminate lenght |


**why should it be useful to automate data wrangling throught OOP?**

These files contains a lot of information about the genotyped population 

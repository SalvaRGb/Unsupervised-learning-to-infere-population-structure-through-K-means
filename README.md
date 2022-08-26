# From-HapMap-to-population-structure-throught-K-means
Unsupervided learning algorithm for population structure calculation

The Hapmap Project was initiated in 2001 by the International HapMap Consortium. Its database is freely available to the public through the NCBI database dbSNP. The Project is also described at Nature 426 :789-796, 2003 [PMID: 14685227]. The file format estabilished through the project is also used in others projects and species.
The Hapmap file format is a table which consists of 11 columns plus one column for each sample genotyped. The first row contains the header labels of your samples, and each additional row contains all the information associated with a single SNP. You can get a Hapmap file by chromosome or a general file.

- rs# contains the SNP identifier;
alleles contains SNP alleles according to NCBI database dbSNP;
chrom contains the chromosome that the SNP was mapped;
pos contains the respective position of this SNP on chromosome;
strand contains the orientation of the SNP in the DNA strand. Thus, SNPs could be in the forward (+) or in the reverse (-) orientation relative to the reference genome;
assembly# contains the version of reference sequence assembly (from NCBI);
center contains the name of genotyping center that produced the genotypes;
protLSID contains the identifier for HapMap protocol;
assayLSID contain the identifier HapMap assay used for genotyping;
panelLSID contains the identifier for panel of individuals genotyped;
QCcode contains the quality control for all entries;
subsequently, the list of sample names.

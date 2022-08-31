# From HapMap to population structure throught K-means

**An example of HapMap python class for diploid species to include in a work flow with unsupervided learning algorithm for population structure inference.**

Handling genotype data typed at hundreds of thousands of loci is a very time-consuming task, specially for population structure inference. Tools such as STRUCTURE (one of the most used and common softwares design for this purpose) based on *Markov chain Monte Carlo* are very time and memory consuming. 

From the perspective of machine learning, dealing with high-dimensional data usually involves preprocessing the data with dimension reduction and feature selection techniques. In addition, clustering techniques such as *k-Means*, in combination with dimension reduction algorithms such as *Principal component analysis* (**PCA**), may outperforme traditional algorithms and population structure techniques in terms of computational time, while competing in precision.  

The pipline described in this repository follows a logical process and is intendend to be an example of how to apply *HapMap_organizer.py* classes that involves:

- **Filtering and extracting useful genetic information for a properly configuration of the genetic matrix (working with HapMap files)** in order to decode the HapMap structure and contruct a customized genetic-marker matrix for population structure inference, this preprocessing involves:
     * Extraction and/or addition of homozygous and heterozygous
     * Substracting markers base on missing_data percentage 
     * Substracting markers base on MAF (*Minor allele frequency*)  
     * Imputation of nan values present in the result matrix
- **Selecting the best possible principal components to represent the data**
- **Apply k-means algorithm to the new features for population inference**


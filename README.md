### About
This collection of scripts follow the general rules descripted in Diehl2009,
in order to compute a Multivariate-Discriminant-Analysis (MDA) of the
Fisher coefficients for the 'MannekenPix Autopicker Algoritmh'.

This small routine has been carried out in order to give a possibility to users
to adopt an open-source approach instead of the macros and coomercial sofwares
suggested in the up-to-date guides [Alderson2004, Diehl2009, DiStefano2006].

This scripts should run smoothly in any Unix-like OS, as long as all
the necessary dependencies are correctly installed.
Starting from version 2.0, the scripts can be ran also in OSX.

### Dependencies
* Python v2.7.* or higher
* R
* Rscript

The needed package for R-statistics is called _DiscriMiner_.
To install it just type in an open R session:

```
> install.package(DiscriMiner)
```
### Getting Started
In order to execute MDA, the entire 'scripts' folder must be copied in your shell `PATH`. Then at shell promp just type:

```
$ MPXmda.sh -e MPXFILE -c CMNFILE [-wn]

  Where:
     -e ExportFile created by MPX
     -c CommandFile given in input to MPX
     -w TrueWeigth [Diehl2009] to be used in MDA (1,[2])
     -n Number of classes [4] % At the moment is tested only with 4 classes

  As output:
    - MannekenPix.cmn.OUT : an updated Command-file (*.cmn) version of ARG2,
                            containing the new Fisher Coefficients at the right
                            place. This file is ready-to-use for subsequent runs.
    - FisherCoeff.out : txt files with the results from lda in R
    - Format4MDA.csv : another formatting of *Exp for Excel/R analysis.

NB: The number of classes and the relative timing errors,
    MUST BE DEFINED INSIDE Format4MDA.py SCRIPT !!!
```

--------------------
### References
- Di Stefano, R et al. (2006). "Automatic seismic phase picking and consistent   observation error assessment: application to the Italian seismicity". In: Geophysical JournalInternational 165.1, pp. 121–134.
- Diehl, Tobias and Edi Kissling (2007). "Users guide for consistent phase picking at local to regional scales".
- Diehl, Tobias and Edi Kissling (2009). "Users Guide for MPX Picking System". In: PhD thesis–Appendix.
- Fisher, Ronald A (1936). "The use of multiple measurements in taxonomic problems". In: Annals of eugenics 7.2, pp. 179–18

### Author
Matteo Bagagli @ ETH-Zurich, 01-2017
<matteo.bagagli@erdw.ethz.ch>

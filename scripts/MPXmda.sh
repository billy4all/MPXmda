#!/bin/bash
### MPX_mda.sh
# Simple routine that create a new command file for MPX updated with new Fisher
# coefficients. For more info read the README file. As a third parameter
# user must append TW1 or TW2 (TrueWeight 1 or 2) in order to apply the MDA on
# a particular class scheme definition. The user is referred @ Diehl,2009
#
# NB: The number of classes and the relative timing errors,
#     MUST BE DEFINED INSIDE Format4MDA.py SCRIPT !!!
#
# USAGE: MPX_mda.sh -e MPXFILE -c CMNFILE [-wn]
# AUTHOR: Matteo Bagagli @ ETH-Zurich , 01-2017
#

#    MPXmda : Multivariable Discriminant Analysis open-source approach
#             for the phase picker "Manneken Pix (MPX)"
#    Copyright (C) 2018  Matteo Bagagli
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

VERSION="2.5"
# ----------------------------------------------------------------------- Check
if [ "$#" == "0" ] || [ "$1" == "-h" ]; then
  echo "[$(basename $0) v${VERSION}] USAGE: $(basename $0) -e MPXFILE -c CMNFILE [-wn]"
  echo "    Where:"
  echo "     -e ExportFile created by MPX"
  echo "     -c CommandFile given in input to MPX"
  echo "     -w TrueWeigth [Diehl2009] to be used in MDA (1,[2])"
  echo "     -n Number of classes [4]"
  echo "*** NB: The number of classes and the relative timing errors,"
  echo "        MUST BE DEFINED INSIDE Format4MDA.py SCRIPT !!!"
  exit
fi
# -------------------------------------------------------------------- Get Vars
while getopts 'e:c:w:n:' option
do
    case "${option}" in
            e) ExpFile="${OPTARG}";;
            c) CmnFile="${OPTARG}";;
            w) Weigth="${OPTARG}";;
            n) NClass="${OPTARG}";;
    esac
done
#
if [ -z "${ExpFile}" -o -z "${CmnFile}" ]; then
        echo "[$(basename $0) v${VERSION}] ERROR: need an *Exp AND a *cmn File !!!"
        exit
fi
# -------------------------------------------------------------------- Defaults
if [ -z "${Weigth}" ];then Weigth=2;fi
if [ -z "${NClass}" ];then NClass=4;fi
# ----------------------------------------------------------------- Expand Vars
#
if [ "${Weigth}" == "2" ]; then   # Preferred method
  weightfield=16
elif [ "${Weigth}" == "1" ]; then
  weightfield=15
else
  echo "[$(basename $0) v${VERSION}] ERROR: TrueWeight param. should be 1 or 2 !!!"
  exit
fi
# ------------------------------------------------------------------------ Main
echo "### Formatting"
Format4MDA.py ${ExpFile}
echo "### MDA"
### IN-File
echo "library(DiscriMiner)" > FisherMDA.R
echo "options(digits=5)" >> FisherMDA.R
echo "options(scipen=999)" >> FisherMDA.R        # To remove scientific notation
echo "rm(list=ls())" >> FisherMDA.R
echo "ExpFile <- read.csv('Format4MDA.csv',header=T)" >> FisherMDA.R
echo "colnames(ExpFile) <- c('FileID','MPX_tA','REF_tA','Ref_Class','AbsErr', \
                       'WFilStoN','GpDlStoN','GpDlAmpR','GpDlSigF','GpDlDelF', \
                       'ThrCFRat','PcAboThr','PcBelThr', 'CFNoiDev', \
                       'TrueW_M1','TrueW_M2','TrueW_M3')" >> FisherMDA.R
echo "df<-ExpFile[, c(${weightfield}, 6:14)]" >> FisherMDA.R
echo "df.lda2 <- linDA(df[,2:10], df[,1])" >> FisherMDA.R
echo "df.lda2\$functions" >> FisherMDA.R
# > summary(df.lda2) | If a summary of the analysis is wanted
###
Rscript FisherMDA.R > FisherCoeff.out

# ------------------------------------------------------------------ Out Format
sed '1d' FisherCoeff.out | awk '{sub($1 FS,"" );print}' > Fisher.cmn
# MAC+Linux v.2.0
cp ${CmnFile} MannekenPix.cmn.OUT
sed -i.trash "167s/.*/ $(sed  '1q;d' Fisher.cmn)/"  MannekenPix.cmn.OUT
sed -i.trash "170s/.*/ $(sed  '2q;d' Fisher.cmn)/"  MannekenPix.cmn.OUT
sed -i.trash "173s/.*/ $(sed  '3q;d' Fisher.cmn)/"  MannekenPix.cmn.OUT
sed -i.trash "176s/.*/ $(sed  '4q;d' Fisher.cmn)/"  MannekenPix.cmn.OUT
sed -i.trash "179s/.*/ $(sed  '5q;d' Fisher.cmn)/"  MannekenPix.cmn.OUT
sed -i.trash "182s/.*/ $(sed  '6q;d' Fisher.cmn)/"  MannekenPix.cmn.OUT
sed -i.trash "185s/.*/ $(sed  '7q;d' Fisher.cmn)/"  MannekenPix.cmn.OUT
sed -i.trash "188s/.*/ $(sed  '8q;d' Fisher.cmn)/"  MannekenPix.cmn.OUT
sed -i.trash "191s/.*/ $(sed  '9q;d' Fisher.cmn)/"  MannekenPix.cmn.OUT
sed -i.trash "194s/.*/ $(sed '10q;d' Fisher.cmn)/"  MannekenPix.cmn.OUT
#
rm Fisher.cmn FisherMDA.R MannekenPix.cmn.OUT.trash
#
echo "... DONE!"

# # ----::::----::::----::::----::::---- Improvement
# while getopts ':s:b:e:' option
# do
#     case "${option}"
#     in
#             s) Strain="${OPTARG}";;
#             b) Begin="${OPTARG}";;
#             e) End="${OPTARG}";;
#     esac
# done
# # ----::::----::::----::::----::::---- Check
# if [ -z "${Strain}" -o -z "${Begin}" -o -z "${End}" ]; then
#         echo "### MergeStrain2.0+: ERROR !!! All of the inputs required ..."
#         echo "###                  Type MergeStrain2.0+ without argouments "
#         echo "###                  for further help."
#         exit
# fi

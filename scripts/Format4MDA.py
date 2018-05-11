#!/usr/bin/env python
####
# This script format data in a proper way for a correct multivariate analysis
# of MannekenPix picker algorithm. Thi script format only PICKED phase by MPX.
# It returns the file Format4MDA.csv that can be loaded in R, SPSS or Excel
#
# USAGE:  Format4MDA.py *Exp
# AUTHOR: Matteo Bagagli @ ETH-Zurich // 012017

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


# ******************************************************************************
# ********************* Reference Pick Class Uncertainties *********************
# ******************************************************************************
NumberOfClass=4
ClassBoundDict={
    '0':0.03,
    '1':0.06,
    '2':0.12,
    '3':0.24,
}
# ******************************************************************************


# --------------------------------------------------------------- Check & Vars
import sys,os,glob
if len(sys.argv)!=2:
    sys.stdout.write('USAGE:  Format4MDA.py *Exp'+os.linesep)
    sys.exit()
else:
    ExportFile=sys.argv[1]
# *Exp Field for extract values
AP_timeField=18  # start from 0 in *.Exp MPX file
AP_classField=19 # start from 0 in *.Exp MPX file
RP_timeField=25  # start from 0 in *.Exp MPX file
RP_classField=26 # start from 0 in *.Exp MPX file

# -------------------------------------------------------------------- Methods
def Pawk(stdIn,field,sep=" "):
    ''' Simil GNU-awk command for fields printing only
        Default field separator is space !!!
        IN: file-path or string.
        OUT: list of str object realted to the field specified.
        *** N.B: Enumeration for fields start from 0 , not 1 as awk does ...
    '''
    try:
        if os.path.isfile(stdIn):
            f=open(stdIn,"r")
            out=[]
            for line in f.readlines():
                fields=line.strip().split(sep)
                fields=filter(lambda x: x!='',fields)    # v1.0.3  weird loading issue if sep specified
                out.append(fields[field])
            f.close()
            return out
        else:
            fields=stdIn.strip().split(sep)
            fields=filter(lambda x: x!='',fields)       # v1.0.3  weird loading issue if sep specified
            return fields[field]
    except(IOError,NameError):
        sys.stderr.write('[Pawk] ERROR: Wrong input object ...'+os.linesep)
        return False
    except(IndexError):
        sys.stderr.write('[Pawk] ERROR: Field number out of range ...'+os.linesep)
        return False

def TrueWeigth_M1(value,classDict):
    ''' Methods that define the true weigth based on Absolute Time Errors
        between reference and MPX picks. (as described in DiStefano 2006)
    '''
    outVal=None
    if 0<=value and value<classDict['0']:
        outVal='0'
    elif classDict['0']<=value and value<classDict['1']:
        outVal='1'
    elif classDict['1']<=value and value<classDict['2']:
        outVal='2'
    elif classDict['2']<=value and value<classDict['3']:
        outVal='3'
    elif value>=classDict['3']:
        outVal='4'
    else:
        sys.stderr.write("TrueWeigth_M1: ERROR !!! No match ...")
        sys.stderr.write(os.linesep)
        sys.exit()
    return outVal

def TrueWeigth_M2(value,RefClass,classDict):
    ''' Methods that define the true weigth based on Absolute Time Errors
        between reference and MPX picks AND the reference Class. (as described in Diehl 2009).
        NB: *** RefClass is type:string !!!
    '''
    outVal=None
    if RefClass=='0':
        if 0<=value and value<classDict['0']:
            outVal='0'
        else:
            outVal='1'
    elif RefClass=='1':
        if classDict['0']<=value and value<classDict['1']:
            outVal='1'
        else:
            outVal='2'
    elif RefClass=='2':
        if classDict['1']<=value and value<classDict['2']:
            outVal='2'
        else:
            outVal='3'
    elif RefClass=='3':
        if classDict['2']<=value and value<classDict['3']:
            outVal='3'
        else:
            outVal='4'
    elif RefClass=='4': # Already rejected
        outVal='4'
    else:
        # If this error appear, check into yout *Exp file in search of
        # weird REFERENCE CLASS (field 27)
        sys.stderr.write(('[%s] ERROR !!! Unknown RefClass: %r'+os.linesep)%(
                            sys.argv[0].split('/')[-1],RefClass))
        sys.stderr.write(('[%s] ERROR !!! Unknown RefClass: %r'+os.linesep)%(
                            sys.argv[0].split('/')[-1],RefClass))
    return outVal

# ----------------------------------------------------------------------- Main
with open('Format4MDA.csv','w') as outID:
    # Writing the header for CSV  file.
    outID.write('FileID,MPX_tA,REF_tA,Ref_Class,AbsErr,WFilStoN,GpDlStoN,' \
                'GpDlAmpR,GpDlSigF,GpDlDelF,ThrCFRat,PcAboThr,PcBelThr,' \
                'CFNoiDev,TrueW_M1,TrueW_M2,TrueW_M3')
    outID.write(os.linesep)
    with open(ExportFile,'r') as expID:
        for ll,line in enumerate(expID):
            # Skip the first 14 lines of *Exp file
            if ll<=13:
                pass
            else:
                MPX_tA=Pawk(line,AP_timeField)
                # Switch if Picked by MPX, otherwise skip line
                if MPX_tA=='*******':
                    continue
                else:
                    FileID=Pawk(line,0)
                    REF_tA=Pawk(line,RP_timeField)
                    Ref_Class=Pawk(line,RP_classField)
                    AbsErr=abs(float(REF_tA)-float(MPX_tA))
                    WFilStoN=Pawk(line,28)
                    GpDlStoN=Pawk(line,29)
                    GpDlAmpR=Pawk(line,30)
                    GpDlSigF=Pawk(line,31)
                    GpDlDelF=Pawk(line,32)
                    ThrCFRat=Pawk(line,33)
                    PcAboThr=Pawk(line,34)
                    PcBelThr=Pawk(line,35)
                    CFNoiDev=Pawk(line,36)
                    TrueW_M1=TrueWeigth_M1(AbsErr,ClassBoundDict)
                    TrueW_M2=TrueWeigth_M2(AbsErr,Ref_Class,ClassBoundDict)
                    TrueW_M3='nan' # todo
                    outID.write('%s,%s,%s,%s,%f,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' %(FileID,
                    MPX_tA,REF_tA,Ref_Class,AbsErr,WFilStoN,GpDlStoN,GpDlAmpR,GpDlSigF,GpDlDelF,
                    ThrCFRat,PcAboThr,PcBelThr,CFNoiDev,TrueW_M1,TrueW_M2,TrueW_M3))
                    outID.write(os.linesep)
#
sys.stdout.write('... DONE!'+os.linesep)

#################################################################
#       *** ADDITIONAL INFO ***
# When MannekenPix picks a seismogram, all predictors are usually populated even if
# some predictors are not used. Predictors are the variable values themselves while the
# coefficients of these variables are written in the command file. Unused predictors are
# expressed by coefficients of predictors equal to zero, not predictors necessarily equal to
# zero.

#!/usr/bin/python

import fnmatch
import os
import sys


def findReplace(directory, find, replace, filePattern):
    changed = 0
    examined = 0
    for path, dirs, files in os.walk(os.path.abspath(directory)):
        for filename in fnmatch.filter(files, filePattern):
            examined += 1
            filepath = os.path.join(path, filename)
            with open(filepath) as f:
                s = f.read()
            c = s.replace(find, replace)
            if s != c:
                changed += 1
                with open(filepath, "w") as f:
                    f.write(c)
    if changed > 0:
        print "changed {:4d} examined {:4d} {:s} -> {:s}".format(changed,examined,find,replace)

if len(sys.argv) < 2:
    print "Need to specify where to apply the script to"
    exit(0)

location = sys.argv[1]

print "Recursively apply search and replace to "+location

def F(find,replace):
    findReplace(location,find,replace,"*.java")

F("FixedMatrix","DMatrixFixed")
F("BlockMatrix","DMatrixBlock")
F("RowMatrix_","DMatrixRow_")

def G(patA,patB):
    F(patA+"32F",patB+"_F32")
    F(patA+"64F",patB+"_F64")

def H(patA,patB):
    F(patA+"32F",patB+"_C32")
    F(patA+"64F",patB+"_C64")

G("DenseMatrix","DMatrixRow")
G("BlockMatrix","DMatrixBlock")
G("EigenPair","EigenPair")
G("Complex","Complex")
G("ComplexPolar","ComplexPolar")
G("ComplexMath","ComplexMath")
H("CDenseMatrix","DMatrixRow")
H("ComplexMatrix","Matrix")

F("DenseMatrixBool","DMatrixRow_B")

for n in range(2,7):
    suf1 = str(n)
    suf2 = str(n)+"x"+str(n)

    F("FixedMatrix"+suf1+"_64F","DMatrixFixed"+suf1+"_F64")
    F("FixedMatrix"+suf2+"_64F","DMatrixFixed"+suf2+"_F64")
    F("FixedMatrix"+suf1+"_32F","DMatrixFixed"+suf1+"_F32")
    F("FixedMatrix"+suf2+"_32F","DMatrixFixed"+suf2+"_F32")
    F("FixedOps"+suf1+"\.","FixedOps"+suf1+"_F64\.")

F("_D64","_R64")
F("_D32","_R32")
F("_CD64","_CR64")
F("_CD32","_CR32")

F("CommonOps\.","CommonOps_R64\.")
F("CovarianceOps\.","CovarianceOps_R64\.")
F("EigenOps\.","EigenOps_R64\.")
F("MatrixFeatures\.","MatrixFeatures_R64\.")
F("NormOps\.","NormOps_R64\.")
F("RandomMatrices\.","RandomMatrices_R64\.")
F("SingularOps\.","SingularOps_R64\.")
F("SpecializedOps\.","SpecializedOps_R64\.")

print "Finished!"
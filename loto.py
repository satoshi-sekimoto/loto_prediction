#########################################################
#
#    Python code for loto6/7 prediction
#                                  by S.Sekimoto 2017
#########################################################
import csv
import numpy as np
import pandas as pd
import scipy.misc as scm
import os.path

class Numorder_dictionary:
    def __init__(self,loto):
        self.loto = loto

        self.arrayset() #set array for numorder
        self.calc_numorder()
        self.search_nn_estimator()
        testttt = self.nn_estimator(self.loto._nmax,2,200)
        out = self.decomp_dictionarynum(testttt)
        print("check")
        print(testttt)
        print(out)
        
    def search_nn_estimator(self):
        vecmax     = 10
        vecmin     = 2
        stnum      = self.loto._nmax-1 #10
        lsnum      = self.loto._nmax-1
        perinummin = 5
        perinummax = self.loto._nmax - 3 #-2 ?

        lotonum = self.loto._lotonum
        answer = np.zeros([lotonum],dtype='int8')

        header = "nndata_loto"
        num    = str(self.loto._lotonum)
        footer = ".dat"
        self.nn_data_name = header + num + footer #set file name

        if os.path.exists(self.nn_data_name):
            print("nndata file exist. read")
#            with open(self.nn_data_name,"w+") as f:
#                string = "puthontest222"
#                f.write(string)
        else:
            print("not, initial full calculation")

        for num in range(stnum,lsnum+1):
            for loto in range(self.loto._lotonum):
                answer[loto] = self.loto._num[num][loto]

            print(num,answer)
            for vec in range(vecmin,vecmax+1):
                for peri in range(perinummin,perinummax+1):
                    estmnum  = self.nn_estimator(num,vec,peri)
                    out      = self.decomp_dictionarynum(estmnum)
                    print(num,vec,peri,out)
        
    def nn_estimator(self,nlast,vecnum,perinum):
        #expect nlast+1 number 
        refvec  = np.zeros([vecnum],dtype='float32')
        vector  = np.zeros([vecnum],dtype='float32')
        invdist = np.zeros([self.loto._nmax],dtype='float32')
        #set reference vector
        for i in range(vecnum):
            refvec[i] = self.loto.nn_numorder[nlast-1-i-1]

        #set invdist
        for nnum in range(vecnum,nlast-1):
            for i in range(vecnum):
                vector[i] = self.loto.nn_numorder[nnum-1-i]
            invdist[nnum] = 1.0 / (np.linalg.norm(vector-refvec)**2)

        #sort array
        sortall  = np.sort(invdist)[::-1]
        sortpart = sortall[:perinum]
        sortcoef = sortpart / np.sum(sortpart)
        allsum = 0.0
        for nnum in range(perinum):
            index = np.where(invdist == sortpart[nnum])
            allsum += self.loto.nn_numorder[index] * sortcoef[nnum]

        return allsum
    def decomp_dictionarynum(self,danswer):
        answer  = int(danswer)
        nummax  = self.loto._nummax
        lotonum = self.loto._lotonum
        out_a   = np.zeros([lotonum],dtype='int8')
        
        temp   = answer - 1
        val1   = nummax
        inival = 1
        for num in range(1,lotonum+1):
            for n in range(inival,nummax+1):
                val2 = nummax - n + 1
                combtemp = int(scm.comb(val1,lotonum-num+1) - scm.comb(val2,lotonum-num+1))
                if temp == combtemp:
                    temp = temp - int(scm.comb(val1,lotonum-num+1) - scm.comb(val2,lotonum-num+1))
                    out_a[num-1] = n
                    inival       = n + 1
                    val1         = nummax - out_a[num-1] + 1
                elif temp < combtemp:
                    temp = temp - int(scm.comb(val1,lotonum-num+1) - scm.comb(val2+1,lotonum-num+1))
                    out_a[num-1] = n - 1
                    inival       = n
                    val1         = nummax - out_a[num-1]
                    break
        return out_a

    def arrayset(self):
        self.loto.nn_numorder = np.zeros([self.loto._nmax],dtype='int32')
        

    def calc_numorder(self):
        nummax  = self.loto._nummax
        lotonum = self.loto._lotonum
        for n in range(self.loto._nmax):
            temp    = scm.comb(nummax,lotonum)
            for num in range(1,lotonum):
                temp -= scm.comb(nummax-self.loto._num[n][num-1]+1,lotonum-num+1)
                temp += scm.comb(nummax-self.loto._num[n][num-1]  ,lotonum-num)
            temp -= scm.comb(nummax-self.loto._num[n][lotonum-1]+1,1)
            temp += 1
            self.loto.nn_numorder[n] = int(temp)


class Setlotodata(object):
    def __init__(self,lotonum):
        self._lotonum = lotonum
        if lotonum == 6:
            self._bonusnum = 1
            self._nummax   = 43
            self._leasthit = 3
            self._datafile = 'data/loto6.csv'
        elif lotonum == 7:
            self._bonusnum = 2
            self._nummax   = 37
            self._leasthit = 4
            self._datafile = 'data/loto7.csv'
            
        self.setfiledata()
        
    def setfiledata(self):
        with open(self._datafile,"r") as f:
            print('Datafile open for loto{0._lotonum}'.format(self))
            data   = csv.reader(f)
            header = next(data) #skip 1 line header
            for row in data:
                pass
            self._nmax = int(row[0]) #get max row
            f.seek(0)
            data   = csv.reader(f)
            header = next(data) #skip 1 line header

            self._num   = np.zeros([self._nmax,self._lotonum],dtype='int8')
            self._bonus = np.zeros([self._nmax,self._bonusnum],dtype='int8')
            i = -1
            for row in data:
                i += 1
                for j in range(2,2+self._lotonum):
                    self._num[i][j-2] = int(row[j])
                for j in range(2+self._lotonum,2+self._lotonum+self._bonusnum):
                    self._bonus[i][j-2-self._lotonum] = int(row[j])
            print('Datafile {0._datafile} close'.format(self))
        return
            
    def __str__(self):
        return "LOTO{0._lotonum},{0._bonusnum},{0._datafile},{0._leasthit}".format(self)

    

def example():
    print('testtsts')

if __name__ == '__main__':
    #generate instance of loto6/7 in Lotodata class.
    loto6 = Setlotodata(6)
    loto7 = Setlotodata(7)
    
    print(loto6._nmax)
    print(loto7._num[10])
    print(loto7._bonus[3])

    numorder6 = Numorder_dictionary(loto6)
    numorder7 = Numorder_dictionary(loto7)

    print(loto6.nn_numorder[150])
    example()

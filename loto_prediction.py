# -*- coding: utf-8 -*-
"""
参考URL
https://www.sejuku.net/blog/24331  :sys.exit
https://pycarnival.com/urlretreive_urlopen/  :urllib
https://www.headboost.jp/python-file-existance/  :ファイル存在確認
https://qiita.com/tackey/items/5b7b2be23af60335fe11  :Unicodeエラー
https://teratail.com/questions/134846 :列を関数処理
https://qiita.com/derodero24/items/91b6468e66923a87f39f  :組み合わせ計算
"""
loto7_url="https://loto7.thekyo.jp/data/loto7.csv"
loto7_savename="C:/Users/Satoshi/Desktop/lotowork/loto7.csv"
loto6_url="https://loto6.thekyo.jp/data/loto6.csv"
loto6_savename="C:/Users/Satoshi/Desktop/lotowork/loto6.csv"

clmn_dictionarynum="Dictnum"
clmn_dict1="dict1"
clmn_dict2="dict2"
clmn_dict3="dict3"
clmn_dict4="dict4"
clmn_dict5="dict5"
clmn_dict6="dict6"
clmn_dict7="dict7"
clmn_num0="第0数字"
clmn_num1="第1数字"
clmn_num2="第2数字"
clmn_num3="第3数字"
clmn_num4="第4数字"
clmn_num5="第5数字"
clmn_num6="第6数字"
clmn_num7="第7数字"
clmn_sensor_port="Portnum(0:noconecct,-1:pitot)"
clmn_sensor_portnew="Portnum"
clmn_sensor_output="Outputlistnum"

clmn_port_x="X/C"
clmn_port_y="Y/C"

# モジュールのインポート
import os, tkinter, tkinter.filedialog, tkinter.messagebox
import pprint
import pandas as pd
import numpy as np
import urllib.request
import sys
from scipy.special import comb

class Setlotodata(object):
    def __init__(self,lotonum):
        self._lotonum = lotonum
        if lotonum == 6:
            self._bonusnum = 1
            self._nummax   = 43
            self._leasthit = 3
            self._datafile = 'C:/Users/Satoshi/Desktop/lotowork/loto6.csv'
            self._url      = "https://loto6.thekyo.jp/data/loto6.csv"
        elif lotonum == 7:
            self._bonusnum = 2
            self._nummax   = 37
            self._leasthit = 4
            self._datafile = 'C:/Users/Satoshi/Desktop/lotowork/loto7.csv'
            self._url      = "https://loto7.thekyo.jp/data/loto7.csv"
        
        self.download_csv()
        self.setfiledata()
        self.setdictnum()


    def setfiledata(self):
        self.data = pd.read_csv(self._datafile,encoding='cp932' )
        return
    
    
    
    def setdictnum(self):
        def colmunfunc_combine(df,num1,num2,comnum):
            int1 = self._nummax - df[num1]
            #comb1 = int(comb(int1,comnum))
            int2 = self._nummax - df[num2] + 1
            #comb2 = int(comb(int2,comnum))
            
            return int1#int1 #int(comb(self._nummax-int(df[num1]), comnum,))-int(comb(self._nummax-int(df[num2])+1, comnum))
        def func_combine(num1,num2,comnum):
            return int(comb(self._nummax-int(num1),2))
                
        self.data[clmn_num0]=0
        
        if self._lotonum == 6:
            print("Calculate dictnum for loto6")
            print(comb(3,2))
            #self.data[clmn_num1]="test"
            self.data[9]=self.data[clmn_num1]
            self.data[8]=colmunfunc_combine(self.data,clmn_num1,clmn_num2,6)
            #self.data[8]=self.data.apply(self.data[clmn_num1],self.data[clmn_num2],6)
            print(self.data.head(2))
        elif self._lotonum == 7:
            print("Calculate dictnum for loto7")
#        with open(self._datafile,"r") as f:
#            print('Datafile open for loto{0._lotonum}'.format(self))
#            data   = csv.reader(f)
#            header = next(data) #skip 1 line header
#            for row in data:
#                pass
#            self._nmax = int(row[0]) #get max row
#            f.seek(0)
#            data   = csv.reader(f)
#            header = next(data) #skip 1 line header
#
#            self._num   = np.zeros([self._nmax,self._lotonum],dtype='int8')
#            self._bonus = np.zeros([self._nmax,self._bonusnum],dtype='int8')
#            i = -1
#            for row in data:
#                i += 1
#                for j in range(2,2+self._lotonum):
#                    self._num[i][j-2] = int(row[j])
#                for j in range(2+self._lotonum,2+self._lotonum+self._bonusnum):
#                    self._bonus[i][j-2-self._lotonum] = int(row[j])
#            print('Datafile {0._datafile} close'.format(self))
#        self.data=pd.read_csv(self._datafile)
#        print(self.data.tail(2))
        return
        
    def download_csv(self):
        if os.path.exists(self._datafile):
            os.remove(self._datafile)   
        urllib.request.urlretrieve(self._url,self._datafile)
        return
    
    def __str__(self):
        return "LOTO{0._lotonum},{0._bonusnum},{0._datafile},{0._leasthit}".format(self)




def download_csvs():
    os.remove(loto7_savename)
    urllib.request.urlretrieve(loto7_url,loto7_savename)
    
    os.remove(loto6_savename)
    urllib.request.urlretrieve(loto6_url,loto6_savename)
    return

if __name__ == '__main__':

    
    
#    download_csvs()
    loto6 = Setlotodata(6)
    loto7 = Setlotodata(7)

    sys.exit()
    
    
# ファイル選択ダイアログの表示
#root = tkinter.Tk()
#root.withdraw()
#fTyp = [("","*")]
#iDir = os.path.abspath(os.path.dirname(__file__))
#tkinter.messagebox.showinfo('圧力計測CSV平均プログラム：','処理するCSVを1個のディレクトリに入れて、その中の一個を選んでください')
#file = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
#csvdir_path=os.path.dirname(file)
#print("CSVファイルディレクトリ：",csvdir_path)
#
#csvfiles=os.listdir(csvdir_path)
#print("CSVファイル一覧")
#pprint.pprint(csvfiles)
#
#tkinter.messagebox.showinfo('圧力計測CSV平均プログラム：','ゼロ点計測のCSVを選択してください')
#zerocsvfile_path = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = csvdir_path)
#print("ゼロ点計測CSVファイル：",zerocsvfile_path)
#
#tkinter.messagebox.showinfo('圧力計測CSV平均プログラム：','模型圧力孔位置情報CSVファイルを選択してください')
#portposfile_path = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = csvdir_path)
#print("模型圧力孔位置情報CSVファイル：",portposfile_path)
#portposfile_df=pd.read_csv(portposfile_path)
#print(portposfile_df)
#
#tkinter.messagebox.showinfo('圧力計測CSV平均プログラム：','センサー接続情報CSVファイルを選択してください')
#sensorconnectfile_path = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = csvdir_path)
#print("センサー接続情報CSVファイル：",sensorconnectfile_path)
#sensorconnectfile_df=pd.read_csv(sensorconnectfile_path)
#print(sensorconnectfile_df)
#sensorconnectfile_df=sensorconnectfile_df.rename(columns={clmn_sensor_port:clmn_sensor_portnew})
#pitotsensor_num=int(list(sensorconnectfile_df.reset_index().query('%s == "-1"' % clmn_sensor_portnew).index)[0]) + 1
#print("ピトー管接続センサー番号：",pitotsensor_num)
#
#outputlist_df=sensorconnectfile_df
#outputlist_df=outputlist_df[outputlist_df[clmn_sensor_output]!=0]
#outputlist_df=outputlist_df.sort_values(by=clmn_sensor_output)
#outputlist_df=outputlist_df.reset_index()
#outputlist_df=outputlist_df.drop("index",axis=1)
#outputlist_df=outputlist_df.loc[:,[clmn_sensor_output,clmn_sensor_sensor,clmn_sensor_portnew]]
#outputlist_df[clmn_port_x]=[portposfile_df.iloc[i-1,1] for i in outputlist_df[clmn_sensor_portnew]]
#outputlist_df[clmn_port_y]=[portposfile_df.iloc[i-1,2] for i in outputlist_df[clmn_sensor_portnew]]
#
#tempdf=pd.read_csv(zerocsvfile_path,header=2)#ヘッダ行数はハードコーディング。ヘッダーありで生成してください
#zero_df=tempdf.describe().loc['mean']
#
#
#inum=0
#for csvfile in csvfiles:
#    csvfile_path = csvdir_path + '/' + csvfile
#    print(csvfile_path)
#    if csvfile_path==zerocsvfile_path:
#        print("　ゼロ点計測に使ったCSVのためスキップ")
#        continue
#    inum=inum+1
#    tempdf=pd.read_csv(csvfile_path,header=2)
#    substvalue_df=tempdf.sub(zero_df)
#    q_df=substvalue_df.iloc[:,pitotsensor_num]
#    cp_df=substvalue_df.sub(q_df,axis=0)
#    cp_df=cp_df.div(q_df,axis=0)
#    cp_df=cp_df * (-1.0)
#    
#    cpave_df=cp_df.describe().loc['mean']
#    cpstd_df=cp_df.describe().loc['std']
#    cpmax_df=cp_df.describe().loc['max']
#    cpmin_df=cp_df.describe().loc['min']
#    
#    name=str(inum)+"-ave-" + csvfile
#    outputlist_df[name]=[cpave_df.iloc[i] for i in outputlist_df[clmn_sensor_sensor]]
#    name=str(inum)+"-std-" + csvfile
#    outputlist_df[name]=[cpstd_df.iloc[i] for i in outputlist_df[clmn_sensor_sensor]]
#    name=str(inum)+"-min-" + csvfile
#    outputlist_df[name]=[cpmin_df.iloc[i] for i in outputlist_df[clmn_sensor_sensor]]
#    name=str(inum)+"-max-" + csvfile
#    outputlist_df[name]=[cpmax_df.iloc[i] for i in outputlist_df[clmn_sensor_sensor]]
#    
#
#
#outputlist_df.to_csv(csvdir_path + '/' + 'average.csv')  
#tkinter.messagebox.showinfo('圧力計測CSV平均プログラム：','average.csvをCSVファイルディレクトリに出力しました。')
#

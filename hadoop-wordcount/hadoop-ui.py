from Tkinter import *
import tkFileDialog
import sys, os
import extracttext
import re

class Example(Frame):
    def __init__(self,root):
        Frame.__init__(self,root)
        self.in_dir='/home/input'#default input in test
        self.out_dir='output'#default output in test
        self.opt_dir={}
        self.opt_dir['initialdir']='.'
        self.opt_dir['parent']=root
        self.opt_dir['mustexist']=True
        self.opt_dir['title']='anti'
        self.hadoop_home=os.getenv('HADOOP_HOME',default=None)
        self.assist_file_name_path=os.path.join(self.hadoop_home,'assist_file/name.txt')
        self.output_dir=os.path.join(self.hadoop_home,'input')
        Button(text='open dir',command=self.askDirectory).pack(side=TOP,expand=YES,fill=X)
        Button(text='start hadoop',command=self.startHadoop).pack(side=TOP,expand=YES,fill=X)
        Button(text='leave safemode',command=self.leaveSafe).pack(side=TOP,expand=YES,fill=X)
        Button(text='upload',command=self.upLoad).pack(side=TOP,expand=YES,fill=X)
        Button(text='process diff',command=self.processDiff).pack(side=TOP,expand=YES,fill=X)
        Button(text='download',command=self.downLoad).pack(side=TOP,expand=YES,fill=X)
        Button(text='clear server',command=self.clearSev).pack(side=TOP,expand=YES,fill=X)
        Button(text='show result',command=self.showResult).pack(side=TOP,expand=YES,fill=X)
        Button(text='stop hadoop',command=self.stopHadoop).pack(side=TOP,expand=YES,fill=X)

    def askDirectory(self):
        filename=tkFileDialog.askdirectory(**self.opt_dir)
        #BUG
        pat=re.compile('(.*)\.docx')
        #hadoop_home=os.getenv('HADOOP_HOME',default=None)
        #BUG:assist_file directory must exist
        #assist_file_name_path=os.path.join(self.hadoop_home,'assist_file/name.txt')
        assist_file_name=open(self.assist_file_name_path,'w')
        os.path.walk(filename,lister,(pat,assist_file_name,self.output_dir))
        assist_file_name.close()

    def startHadoop(self):
        msg=os.popen('start-all.sh').read()
        print msg

    def leaveSafe(self):
        msg=os.popen('hadoop dfsadmin -safemode leave').read()
        print msg

    def upLoad(self):
        #BUG:if i try to mkdir before using this weakly software
        hadoop_input_dir='/user/calm/input'#filepath on hadoop
        hadoop_name_file_path='/home/input'
        #local_input_dir='$HADOOP_HOME/input'
        #local_name_file_path='$HADOOP_HOME/assist_file/name.txt'
        cmd='hadoop fs -mkdir %s'%hadoop_input_dir
        msg=os.popen(cmd).read()
        print msg
        cmd='hadoop fs -put %s %s' %(self.assist_file_name_path,hadoop_name_file_path)
        os.popen(cmd).read()
        print 'upload name file'
        #put all files in local_input_dir to hadoop_input_dir
        cmd='hadoop fs -put %s/* %s' %(self.output_dir,hadoop_input_dir)
        msg=os.popen(cmd).read()
        print 'upload data file'

    def processDiff(self):
        cmd=('hadoop jar $HADOOP_HOME/bin/wordcount.jar WordCount %s %s') %(self.in_dir,self.out_dir)
        msg=os.popen(cmd).read()
        print msg

    def downLoad(self):
        msg=os.popen('rm part-r-00000').read()
        print msg
        msg=os.popen('hadoop fs -get output/part-r-00000 .').read()
        print msg

    def clearSev(self):
        #BUG
        cmd='hadoop dfs -rmr /home/input/name.txt'
        msg=os.popen(cmd).read()
        print msg
        cmd='hadoop dfs -rmr /user/calm/input'
        msg=os.popen(cmd).read()
        print msg
        msg=os.popen('hadoop dfs -rmr output').read()
        print msg

    def showResult(self):
        win=Toplevel()
        f=open('part-r-00000','rb')
        input_strs=f.readlines()
        f.close()
        lab_row=0
        for line_strs in input_strs:
            mystrs=line_strs.split()
            lab_column=0
            #print 'this is line %d' %lab_row
            for mystr in mystrs:
                #print 'col %d' %lab_column
                #print mystr
                Label(win,text=mystr,relief=RIDGE,width=60).grid(row=lab_row,column=lab_column)
                lab_column=lab_column+1
            lab_row=lab_row+1

    def stopHadoop(self):
        msg=os.popen('stop-all.sh').read()
        print msg

def lister(tup,dirName,filesInDir):
    pat,assist_file_name,output_dir=tup
    #print 'txt file in ' + '[' + dirName + ']'
    for fname in filesInDir:
        path = os.path.join(dirName,fname)
        if not os.path.isdir(path):
            matchobj = re.match(pat,path)
            if matchobj is not None:
                newFileName = matchobj.group(1)+'.txt'
                newFileNameBase=os.path.basename(newFileName)
                newFileNamePath=os.path.join(output_dir,newFileNameBase)
                extracttext.extract(path,newFileNamePath)
                assist_file_name.write(str(os.path.basename(newFileName)+' '))

if __name__ =='__main__':
    root=Tk()
    Example(root).pack()
    root.mainloop()
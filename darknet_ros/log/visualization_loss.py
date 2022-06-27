import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#%matplotlib inline
 
lines =1004    #改为自己生成的train_log_loss.txt中的行数
start_ite = 1 #log_loss.txt里面的最小迭代次数
end_ite = 900 #log_loss.txt里面的最大迭代次数
step = 50 #跳行数，决定画图的稠密程度
igore = 500 #当开始的loss较大时，你需要忽略前igore次迭代，注意这里是迭代次数
result = pd.read_csv('train_log_loss.txt',skiprows=[x for x in range(lines) if (x<lines*1.0/((end_ite - start_ite)*1.0)*igore or x%step!=9)]\
    , error_bad_lines=False, names=['loss', 'avg', 'rate', 'seconds', 'images'])
result.head()
 
result['loss']=result['loss'].str.split(' ').str.get(1)
result['avg']=result['avg'].str.split(' ').str.get(1)
result['rate']=result['rate'].str.split(' ').str.get(1)
result['seconds']=result['seconds'].str.split(' ').str.get(1)
result['images']=result['images'].str.split(' ').str.get(1)


result['loss']=pd.to_numeric(result['loss'],errors='ignore')
result['avg']=pd.to_numeric(result['avg'],errors='ignore')
result['rate']=pd.to_numeric(result['rate'],errors='ignore')
result['seconds']=pd.to_numeric(result['seconds'],errors='ignore')
result['images']=pd.to_numeric(result['images'],errors='ignore')

x_num = len(result['avg'].values)
tmp = (end_ite-start_ite - igore)/(x_num*1.0)
x = []
for i in range(x_num):
	x.append(i*tmp + start_ite + igore)

fig = plt.figure(1, dpi=160)
ax = fig.add_subplot(1, 1, 1)
ax.plot(x,result['avg'].values,'r', label='avg_loss')
ax.legend(loc='best')
ax.set_ylim([0, 10])
ax.set_xlim([0, 1000])
ax.set_title('The loss curves')
ax.set_xlabel('iteration')
ax.spines['top'].set_visible(False)     #去掉上边框
ax.spines['right'].set_visible(False)   #去掉右边框
fig.savefig('avg_loss')


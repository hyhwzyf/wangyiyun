#计算词频近年增长速度
import pandas as pd
import numpy as np
import statsmodels.api as sm


print("正在载入词频文件……")
file = pd.read_csv('wordcounts2.csv',encoding='gbk')
df = pd.DataFrame(file)

file2018 = pd.read_csv('wordcounts2018.csv',encoding='utf8')
df2018 = pd.DataFrame(file2018)
WordRegResult = 'WordRegResult.csv'
column_name = ["words","slope","rsquared"]
data = pd.DataFrame(columns = column_name)
data.to_csv(WordRegResult, index = None, encoding = 'utf_8_sig')
wordlist = df2018["words"].tolist()

#测试样例
#wordlist = ['世界','祖国','痛苦'] 

def wordreg(char):
    x = char_df['years']
    y = char_df['ratios']
    x_n = sm.add_constant(x)
    model = sm.OLS(y, x_n)
    results = model.fit()
    #print(results.summary())
    a = results.params['years']
    R = results.rsquared
    return a,R

print("正在计算词频回归参数……")
#词频线性回归
word_reg_results = []
n = len(wordlist)
for i in range(n):
    if i%100 == 0:
        print("\r进度：{:.2f}%".format(100*i/n),end="")
    char = wordlist[i]
    char_df = df[df['words'] == char]
    if len(char_df)>2:
        result = wordreg(char)
        word_reg_result = [char,result[0],result[1]]
    else:
        word_reg_result = [char,0,0]
    word_reg_results.append(word_reg_result)

#print(word_reg_results)

print("参数计算完毕，正在写入数据到csv……")
data1=pd.DataFrame(columns=column_name,data=word_reg_results)
data1.to_csv(WordRegResult, index = None, mode = 'a', header = None, sep = ',', encoding = "utf_8_sig")

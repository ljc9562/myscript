import pandas as pd
from snownlp import SnowNLP
import pypinyin as piy
import jieba

def name_clean(name):
    # 清除姓名中相同字的情况
    name = name.replace(' ', '')
    news_ids = []
    for id in list(name):
        if id not in news_ids:
            news_ids.append(id)
    name_2 = "".join(news_ids)
    # 如果姓名中包含以下的字就只取名字的姓
    for key in ['先生', '小姐', '大婶', '老师', '哥', '生', '姐', '小朋友','女士','男士','爱人']:
        if key in name_2:
            a = 1
    try:
        if a == 1:
            return name_2[0]
    except:
        return name_2

def same_clean(pinyin_1):
    myset = set(pinyin_1)  # myset是另外一个列表，里面的内容是mylist里面的无重复 项
    for item in myset:
        if pinyin_1.count(item) >= 2:
            return True
        else:
            return False

def name_phone_count(id):
    id_1 = id
    soure = data[data['异常组别'] == int('{}'.format(id))]
    husbind_info = soure.loc[:, ['男方uid', '男方姓名', '男方手机', '男方身份证']]
    husbind_info.columns = ['uid', '姓名', '手机', '身份证']
    wife_info = soure.loc[:, ['女方uid', '女方姓名', '女方手机', '女方身份证']]
    wife_info.columns = ['uid', '姓名', '手机', '身份证']
    new_frame = pd.concat([husbind_info, wife_info], axis=0)
    idcard_judge = 'True' in str(new_frame['身份证'].dropna().duplicated())
    tot_phone_num = len(new_frame['手机'].dropna())
    phone_num = len(set(new_frame['手机'].dropna()))
    name_count = len(new_frame['姓名'].dropna())
    name_list = []
    for i in new_frame['姓名'].dropna():
        i = name_clean(i)
        for j in new_frame['姓名'].dropna():
            j = name_clean(j)
            i_pinyin = piy.lazy_pinyin(i)
            j_pinyin = piy.lazy_pinyin(j)
            same_num = len([l for l in i_pinyin if l in j_pinyin])
            if same_clean(i_pinyin) or same_clean(j_pinyin):
                if (i in j) or (j in i):
                    name_list.append(int(1))
            else:
                # 拼音相同数大于3 或者 （拼音相同数为2且名字中某一方名字字数等于小于2）
                if same_num >= 3 or ((len(i) < 3 or len(j) < 3) and same_num == 2):
                    # print(i,j)
                    name_list.append(int(1))
                # 当拼音相同数为1时，判断姓名的第一个字是否是姓（nr），同时其中一方姓名长度为1
                if same_num == 1:
                    i_exist_nr = str(list(SnowNLP(i[0]).tags)).count('nr')
                    j_exist_nr = str(list(SnowNLP(j[0]).tags)).count('nr')
                    if (i_exist_nr > 0 or j_exist_nr > 0) and (len(i) == 1 or len(j) == 1):
                        name_list.append(int(1))
                    else:
                        pass
    name_text = (name_count ** 2 - sum(name_list))
    return id_1, tot_phone_num, phone_num, name_count, name_text, idcard_judge

def stop(a):
    condition = lambda t: t != "号"
    filter_list = list(filter(condition, a))
    return filter_list

def address_clean(address):
    if str(address) == 'nan':
        return []
    else:
        seg_list=jieba.cut('{}'.format(address))
        address_split = ",".join(seg_list).split(',')
        try:
            address_clearn_finish = set(stop(address_split[round(len(address_split)*0.6+1)*(-1):]))
            print(address_clearn_finish)
            return address_clearn_finish
        except:
            return 'miss'


def address_logistic_judge(address1, address2):
    address1 = set(address_clean(address1))
    address2 = set(address_clean(address2))
    try:
        logistic_judge = ((len(address1 & address2) * (len(address1) + len(address2))) / (
        len(address1) * len(address2))) / 2  # 阀值为0.5最佳
    except:
        logistic_judge = 0
    if logistic_judge >= 0.5:
        return '地址相同'
    else:
        return '地址不相同'

def address_control(id_address):
    try:
        if len(data[data['异常组别'] == id_address[0]].index) <= 2:  # 132374
            index1 = data[data['异常组别'] == id_address[0]].index[0]
            index2 = data[data['异常组别'] == id_address[0]].index[1]
            return  address_logistic_judge(data.loc[index1, ['详细地址_410']].values[0], data.loc[index2, ['详细地址_410']].values[0])
        else:
            return '人工判断'
    except:
        return '人工判断'





if __name__ == '__main__':
    data = pd.read_excel(r"Z:\工作交接\异常数据\20180816-1330异常数据(1).xlsx",sheetname='Sheet2')
    data['是否特殊'] = '是'
    data['身份证是否重复'] = '否'
    for ids1 in data['异常组别'].drop_duplicates():
        if name_phone_count(ids1)[5]:
            data.loc[data[data['异常组别'] == ids1].index, ['身份证是否重复']] = '是'

    list_normal_id = []
    for i in data['异常组别'].drop_duplicates():
        if (name_phone_count(i)[3] == 2 and name_phone_count(i)[4] == 0) or (
                name_phone_count(i)[3] == 3 and name_phone_count(i)[4] < 6) or (
                name_phone_count(i)[3] == 4 and name_phone_count(i)[4] < 10) or (
                name_phone_count(i)[3] >= 5 and name_phone_count(i)[4] <= 18):
            list_normal_id.append(name_phone_count(i)[0])

    for ids in list_normal_id:
        for index in data[data['异常组别'] == ids].index:
            data.loc[index, ['是否特殊']] = '否'


    C = pd.DataFrame(data['异常组别'].drop_duplicates())
    C['地址判断'] = C[['异常组别']].apply(address_control,axis =1)
    data = pd.merge(data,C,left_on='异常组别',right_on='异常组别')

    data.loc[:,['LOVE_ID','是否特殊','身份证是否重复','地址判断']].to_excel(r"Z:\工作交接\异常数据\20180816-1330异常数据pd.xlsx", index=False)
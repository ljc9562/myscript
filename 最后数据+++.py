import pandas as pd
import time

#column 为list形式['填写所需要+的列']
def add_num(column,group):
    print('正在加加加~~~')
    for j in group:
        unnormal = data[data['异常组别'] == j]
        try:
            print(j)
            index_del = unnormal[unnormal['标记(删除|修改)'] == '删除'].index[0]
            print(index_del)
            index_fix = unnormal[unnormal['标记(删除|修改)'] == '修改'].index[0]
            print(index_fix)
            if len(unnormal.index) == 2:
                # if len(unnormal.index) == 2:
                    for columns in column:
                        if data.loc[index_fix,[columns]][0]=='' and  data.loc[index_del,[columns]][0]=='':
                            pass
                        elif data.loc[index_fix,[columns]][0]!='' and  data.loc[index_del,[columns]][0]!='':
                            data.loc[index_fix, [columns]] = str(data.loc[index_fix, [columns]][0]) + '+' + str(data.loc[index_del, [columns]][0])
                        elif data.loc[index_fix,[columns]][0]=='' and  data.loc[index_del,[columns]][0]!='':
                            data.loc[index_fix, [columns]] = str(data.loc[index_del, [columns]][0])
                        else:
                            pass
            else:
                for w in unnormal.index:
                    data.loc[w,'lable'] = '手动'
            print('OK'+str(j))
        except:
            for w in unnormal.index:
                data.loc[w, 'lable'] = '状态相同'
            print(str(j)+'error')



def combine(col,group):
    for j in group:
        unnormal = data[data['异常组别'] == j]
        print(str(j))
        try:
            index_del = unnormal[unnormal['标记(删除|修改)'] == '删除'].index[0]
            index_fix = unnormal[unnormal['标记(删除|修改)'] == '修改'].index[0]
            if len(unnormal.index) == 2:
                # if len(unnormal.index) == 2:

                for columns in col:
                    # print(columns)
                    try:
                        if data.loc[index_fix, [columns]][0] == '' and data.loc[index_del, [columns]][0] == '':
                            pass
                        elif data.loc[index_fix, [columns]][0] == '' and data.loc[index_del, [columns]][0] != '':
                            data.loc[index_fix, [columns]] = data.loc[index_del, [columns]][0]
                            print(columns)
                        else:
                            pass
                    except:
                        print(columns)
        except:
            for w in unnormal.index:
                data.loc[w, 'lable'] = '状态相同'
            print(str(j)+'error')

# #曾推活动  到场 累加函数
# def add(plus,group):
#     for j in group:
#         unnormal = data[data['异常组别'] == j]
#         index_del = unnormal[unnormal['标记(删除|修改)'] == '删除'].index[0]
#         index_fix = unnormal[unnormal['标记(删除|修改)'] == '修改'].index[0]
#         if len(unnormal.index) == 2:
#             # if len(unnormal.index) == 2:
#
#             for columns in plus:
#                 notsame = []
#                 for i in data.loc[index_del,[columns]][0].split('+'):
#                     if i not in data.loc[index_fix,[columns]][0]:
#                         notsame.append(i)
#                 notsame2 =  "+".join(notsame)
#                 print(notsame2)
#                 if len(notsame2)==0:
#                     pass
#                 elif data.loc[index_fix, [columns]][0] == '' and data.loc[index_del, [columns]][0] != '':
#                     data.loc[index_fix, [columns]] = notsame2
#                 else:
#                     data.loc[index_fix, [columns]] = data.loc[index_fix, [columns]][0] +'+'+ notsame2
#         else:
#             for w in unnormal.index:
#                 data.loc[w, 'lable'] = '状态相同'

def time_transform(times):
    try:
        ts = time.mktime(time.strptime('{}'.format(times), "%Y-%m-%d : %H:%M:%S"))
    except:
        ts = time.mktime(time.strptime('{}'.format(times), "%Y-%m-%d %H:%M:%S"))
    return ts

def address(address2,group):
    for j in group:
        unnormal = data[data['异常组别'] == j]
        try:
            index_del = unnormal[unnormal['标记(删除|修改)'] == '删除'].index[0]
            index_fix = unnormal[unnormal['标记(删除|修改)'] == '修改'].index[0]

            for columns in address2:
                if len(unnormal.index) == 2:
                    # if len(unnormal.index) == 2:
                        print(time_transform(data.loc[index_del,'数据创建时间'])>time_transform(data.loc[index_fix,'数据创建时间']))
                        if time_transform(data.loc[index_del,'数据创建时间'])>time_transform(data.loc[index_fix,'数据创建时间']) and data.loc[index_del, [columns]][0] != '':
                            if  data.loc[index_del, [columns]][0] == '':
                                pass
                            elif  data.loc[index_del, [columns]][0] != '':
                                data.loc[index_fix, [columns]] = data.loc[index_del, [columns]][0]
                                print('地址删重')
                            elif  data.loc[index_del, [columns]][0] != '' and data.loc[index_fix, [columns]][0] != '':
                                data.loc[index_fix, [columns]] = data.loc[index_del, [columns]][0]
                            else:
                                pass
                        else:
                            pass
        except:
            for w in unnormal.index:
                data.loc[w, 'lable'] = '状态相同'
            print(str(j)+'error')

if __name__ == '__main__':

    print('---------------------------------------------------')
    print('使用须知：只修改姓名和手机 等级	男方uid	男方姓名	男方手机	男方通话状态	男方手机归属地	男方身份证	女方uid	女方姓名	女方手机	女方通话状态	女方手机归属地	女方身份证	电话判定结果\n其他内容会自动加加加\n只处理异常ID中2条数据的情况\n然后标记相同和异常ID有3条的需要手动\n-----------------------------\n把需要放入的处理文件按着shift+右键选择复制地址后在框框中右键需要删除引号')
    dir = input('输入地址  例如：F:\\QQ_FILE\\2017.8.11异常数据杨.xlsx : ')
    book = input('工作簿名称 如   2-李  :')
    save = input('输入保存地址  例如：F:\\QQ_FILE\\xxx异常数据杨.xlsx : ')
    data = pd.read_excel('{}'.format(dir), sheetname='{}'.format(book),keep_default_na = False)
    print('开始读取文件')
    group = data['异常组别'].drop_duplicates()
    add_num(['LOVE_ID', '男方uid', '女方uid'], group)
    combine(
        ['男方身份证','女方身份证','数据创建时间', '电话判定结果', '几遍电话', '电话时间', '电话备注', '收件人', '收件备注', '异常时间', '曾推活动', '到场', '本届索票信息', '异常来源', '最后一次的电话分型',
         '婚纱摄影_385','婚宴酒店_386','婚庆公司_387','结婚钻戒_388','婚纱礼服_389','结婚百货_390','旅游_391','家装_392','婚车租赁_393','新娘美容_394','母婴_395','重点看婚纱摄影_396','重点看婚宴酒店_397',
         '重点看婚庆公司_398','重点看结婚钻戒_399','重点看婚纱礼服_400','重点看结婚百货_401','重点看旅游_402','重点看家装_403','重点看婚车租赁_404','重点看新娘美容_405','重点看母婴_406','家具_546','家具建材_547',
         '建材_548','家电_549','重点看建材_888','家博会_962','重点看家具_963','重点看家电_964',
         '重点看装修公司_965','儿童玩具_966','早教育儿_967','亲子活动_968','儿童健康_969','重点看母婴服饰_970','重点看儿童玩具_971','重点看亲子活动_972','重点看奶粉辅食_973','重点看早教育儿_974',
         '重点看母婴用品_975','重点看孕婴摄影_976','重点看儿童健康_977','重点看金融理财_978','重点看宝宝首饰_979','重点看家博会_980','母婴服饰_987','车床汽座_988','孕婴摄影_989','金融理财_990',
         '重点看车床汽座_991','重点看特长教育_996','重点看车床气座_997','重点看亲子摄影_998','重点看月子养护_999','重点看宝宝宴/策划_1000','重点看儿童家居_1001','重点看医疗保险_1002','重点看月嫂_1003',
         '奶粉辅食_1004','母婴用品_1005','重点看美业健康_1006','宝宝首饰_1008','月子养护_1009','重点看月子会所_1014','重点看月子餐_1015','重点看妇产医院_1034','车床气座_1222','医疗保险_1223',
         '亲子摄影_1224','宝宝宴/策划_1225','儿童家居_1226','装新房_1231','重点看装新房_1232','医疗健康_1260','亲子游乐_1261','重点看医疗健康_1262','重点看亲子游乐_1263','产后修复_1264','宝宝宴_1265',
         '重点看产后修复_1266','重点看宝宝宴_1267','才艺特长_1268','重点看才艺特长_1269','月嫂_1270','月子中心_1271','重点看月子中心_1272','重点看看家装_1469','装修公司_1488','软体软装_1489',
         '重点看软体软装_1490','橱柜衣柜_1491','重点看橱柜衣柜_1492','卫浴陶瓷_1501','重点看卫浴陶瓷_1502','地板门窗_1503','重点看地板门窗_1504','重点看家居_1532','婚纱摄影|喜宴酒店|结婚钻戒|婚庆公司|婚纱礼服|婚车租赁|结婚_1538',
         '月子_1552','重点看月子_1553','早教_1555','特长_1556','摄影_1557','重点看摄影_1558','亲子旅游_1561','亲子金融_1562','美业健康_1563','重点看亲子旅游_1625','重点看亲子金融_1626','家具家居_1664',
         '重点看家具家居_1665','基础建材_1666','重点看基础建材_1667','家电厨电_1668','重点看家电厨电_1669','重点看家具建材家电_1711','重点看家具家电_2481','家居_2512','结婚钻戒|家装_2581','购家用车_2588',
         '重点看购家用车_2589','图书科技_2600','健康生活_2601','重点看图书科技_2602','重点看健康生活_2603','loveId_2696','家具家电_2717','21643648_2768'],
        group)
    address(['email','婚期','办婚礼地','省_407','市_408','区_409','详细地址_410','宝宝性别','孕婴状态','预产期','生日','一胎筹备','一胎阶段','一胎生日','一胎年龄','一胎性别','二胎筹备','二胎阶段','二胎生日','二胎年龄','二胎性别','三胎筹备','三胎阶段','三胎生日','三胎年龄','三胎性别','收件时段_411','收件人_459','收件备注_460'],group)
    # add(['曾推活动','到场'],group)
    data['电话判定结果'] = ''
    data['最后一次的电话分型'] = ''
    print('开始输出')
    # data.to_excel("F:\\ljc_file\\输出目录\\excel\\20170827异常数据结果.xlsx",index=False)
    # data.to_excel("F:\\ljc_file\\输出目录\\excel\\20170831特殊删重-cwl.xlsx",index=False)
    data.to_excel('{}'.format(save),index=False)




#131689
# unnormal = data[data['异常组别'] == 131689]
# address2 = '婚期'
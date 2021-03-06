# -*- coding:utf-8 -*-
import os
import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
from snownlp import SnowNLP


class Init(object):
    def __init__(self):
        self.dir = os.getcwd()
        self.input_dir = self.dir + os.sep + '需要清洗的文件'
        self.output_dir = self.dir + os.sep + '结果输出'
        self.akcode_dir = self.dir + os.sep + '配置文件'
        self.readme_dir = self.dir + os.sep + 'readme.txt'

    def judge_init(self):
        '''判断是否初始化过,如果没有进行初始化'''
        self.dir + os.sep + '需要清洗的文件'
        try:
            os.listdir(self.input_dir)
            # print('text')
            return 1
        except BaseException:
            print("----------------地址工具初始化开始,完成后请重新打开工具运行---------------------")
            os.mkdir(self.input_dir)
            os.mkdir(self.output_dir)
            os.mkdir(self.akcode_dir)
            pd.DataFrame(columns=['婚博会id	', '详细地址']).to_excel(
                self.dir + os.sep + '地址清洗模版.xlsx', index=False)
            readme = open(self.readme_dir, 'w')
            readme.write('帮助文档:\n使用者需要自行到高德地图API官网，申请个人开发者  PS：用支付宝账号登陆即可省去大量验证\n网站地址:http://lbs.amap.com/\nkey的获取方法:http://lbs.amap.com/api/webservice/guide/create-project/get-key\n个人开发者的每个账号所有应用累积可以创建10个web服务对AK码\n申请之后把AK码放入 配置文件（文件夹中） 用txt文件的方式储存 用换行符分割\n清洗模版中第一列为id,第二列为需要清洗的地址,需要带上表头')
            readme.close()
            print("--------------初始化完成,请阅读readme.txt和配置好所需的文件---------------------")
            return 0
        # a = Output_deal()
        # a.deep_clean()


class API_search(object):
    def __init__(self):
        '''初始化'''
        self.dir = os.getcwd()
        self.input_dir = self.dir + os.sep + '需要清洗的文件'
        self.output_dir = self.dir + os.sep + '结果输出' + os.sep + \
            input('输出文件名(无需后缀):') + '{}.xlsx'.format(time.strftime('%Y%m%d%H%M', time.localtime()))
        self.akcode_dir = self.dir + os.sep + '配置文件'
        self.individual_ak = input('请输入你配置保存的AK文件名（无需加.txt) -->') + '.txt'
        self.count = int(input('累积处理过多少条地址?(如果首次处理地址填0) -->'))
        self.frame = pd.DataFrame(
            columns=[
                'id',
                'status',
                'address',
                'province',
                'city',
                'zone',
                'formatted_address',
                'level'])

    def read_file(self):
        '''读取处理文件,使用对部分带有歧义对路段进行处理,生成新的索引列'''
        data = pd.read_excel(
            self.input_dir +
            os.sep +
            os.listdir(
                self.input_dir)[0], keep_default_na=False)
        data = data.iloc[:, [0, 1]]
        data.columns = ['婚博会id', '详细地址']
        data['详细地址'] = '广东省' + data['详细地址']
        special_index = data[data['详细地址'].str.contains(".*中山(一|二|三|四|五|六|七|八|九|[0-9])路.*") | data['详细地址'].str.contains("中山大道") | data['详细地址'].str.contains("东莞庄路") |data['详细地址'].str.contains('中山大学') ].index.tolist()
        data.loc[special_index, ['详细地址']] = data[data['详细地址'].str.contains(".*中山(一|二|三|四|五|六|七|八|九|[0-9])路.*") | data['详细地址'].str.contains(
            "中山大道") | data['详细地址'].str.contains("东莞庄路")| data['详细地址'].str.contains('中山大学')][['详细地址']].apply(lambda x: '广州市' + x[0][3:], axis=1)
        data['index'] = data.index
        return data

    def fan_to_jian(self, text):
        '''使用snownlp庫進行繁體轉簡體'''
        fan = SnowNLP(text)
        return fan.han

    def ak_judge(self, index):
        individual_ak_file = open(
            self.akcode_dir + os.sep + self.individual_ak)
        list = individual_ak_file.read().split('\n')
        cnt = (index + self.count+1) / 6000
        print('已处理{}条'.format(index + 1))
        return list[int(cnt)]

    def get_address_coordinate(self, id, address, index):
        '''調用api下載數據'''
        ak = self.ak_judge(index)
        map = requests.get(
            'http://restapi.amap.com/v3/geocode/geo?address={}&output=XML&key={}'.format(
                self.fan_to_jian(address), ak))
        # id, status, address, province, city, zone, formatted_address, lng, lat, wgs_lng, wge_lat, level
        info = BeautifulSoup(map.content, 'lxml')
        print(info)
        id = id
        address = self.fan_to_jian(address)
        print(address)
        try:
            status = info.select('response > status')[0].text
        except BaseException:
            status = ''
        try:
            formatted_address = info.select(
                'geocode > formatted_address')[0].text
        except BaseException:
            formatted_address = ''
        try:
            province = info.select('geocode > province')[0].text
        except BaseException:
            province = ''
        try:
            city = info.select('geocode > city')[0].text
        except BaseException:
            city = ''
        try:
            zone = info.select('geocode > district')[0].text
        except BaseException:
            zone = ''
        try:
            level = info.select('geocode > level')[0].text
        except BaseException:
            level = ''
        frame_temp = pd.DataFrame({'id': id,
                                   'status': status,
                                   'address': address[3:],
                                   'province': province,
                                   'city': city,
                                   'zone': zone,
                                   'formatted_address': formatted_address,
                                   'level': level},
                                  index=["0"],
                                  columns=['id',
                                           'status',
                                           'address',
                                           'province',
                                           'city',
                                           'zone',
                                           'formatted_address',
                                           'level'])
        return frame_temp

    def summary(self, data):
        '''合并为一个Dataframe'''
        id = data[0]
        address = data[1]
        print(address)
        index = data[2]
        self.frame = self.frame.append(
            self.get_address_coordinate(
                id, address, index), ignore_index=True)

    def main(self):
        '''总运行函数'''
        data = self.read_file()
        data.apply(self.summary, axis=1)
        self.frame.to_excel(self.output_dir,index=False)
        # return self.frame

    def temporary_main(self, frame):
        '''临时调用运行函数'''
        print(frame)
        frame.apply(self.summary, axis=1)
        return self.frame

    def others_zone_deal(self, frame, city):
        frame = frame[(frame['level'] == '省') | (frame['level']
                      == '市') | (frame['formatted_addressself'] == '')]
        frame['address'] = city + frame['address']
        frame[['id', 'address']].apply(self.temporary_main, axis=1)

    def deep_clean(self):
        '''对地址进行精细化处理,着重珠三角地区'''
        summary_data2 = self.main()
        clean_tranfrom_guangzhou = summary_data2[
            (summary_data2['level'] == '省') | (summary_data2['level'] == '市') | (
            summary_data2['level'] == '乡镇')]
        clean_tranfrom_guangzhou = clean_tranfrom_guangzhou.copy()
        clean_tranfrom_guangzhou['address'] = '广州市' + clean_tranfrom_guangzhou['address']
        clean_tranfrom_guangzhou['index'] = clean_tranfrom_guangzhou.index
        clean_tranfrom_guangzhou = clean_tranfrom_guangzhou.loc[:,['id','address','index']]
        print(clean_tranfrom_guangzhou)
        clean_tranfrom_guangzhou.apply(self.temporary_main, axis=1)



if __name__ == "__main__":
    # 初始化
    count = [0]
    init = Init()
    if init.judge_init() == 0:
        print('欢迎使用广州数据部地区清洗工具')
    else:
        print('已完成初始化,开始进行下一步操作')
        api_s = API_search()
        api_s.main()
    # 处理文件

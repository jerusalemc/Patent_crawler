# -*- coding: utf-8 -*-
"""
对CNKI专利查询结果页面进行解析，得到查询条目列表
"""
import sys
import json
import datetime
from HTMLParser import HTMLParser

from spider import CnkiSpider

reload(sys)
sys.setdefaultencoding('utf8')


class PatentParser(HTMLParser):
    def __init__(self, append_info=''):
        HTMLParser.__init__(self)
        self.__insubtags = ['sub', 'sup']
        # 关键标志flag取值：0无关标签，1专利号有关标签和专利名标签，2发明人标签，3申请人标签，4申请日期表亲啊，5公开日期标签
        self.__flag = 0
        self.__insubflag = False
        self.__subject = ''
        # 输出顺序：下载链接，专利标题，发明人，申请人，申请日期，公开日期
        self.__sequence = []
        self.__result = []
        self.page_count = ''
        self.__pagecountflg = False
        self.item_count = ''
        self.__itemflg = False
        self.append_info = str(append_info)

    def handle_starttag(self, tag, attrs):
        tag = tag.strip()
        # 标记专利标题、解析专利号
        if tag == 'a':
            for name, value in attrs:
                if name == 'class' and value == 'fz14':
                    self.__flag = 1
                elif name == 'href' and self.__flag == 1:
                    s = value.strip()
                    self.__sequence.append(s[s.find('filename=') + 9:])
        # 关键标志flag取值：0无关标签，1专利号有关标签和专利名标签，2发明人标签，3申请人标签，4申请日期表亲啊，5公开日期标签
        elif tag == 'td':
            if self.__flag in range(1, 5):
                self.__flag += 1
        # 标记查询总页码
        elif tag == 'span':
            for name, value in attrs:
                if name == 'class' and value == 'countPageMark':
                    self.__pagecountflg = True
        # 标记应答条目综述
        # NOTE: cnki最多支持返回6000条记录。因此，超过6000条的话，应调整查询条件，如缩短日期跨度、具体化专利分类
        elif tag == 'div':
            for name, value in attrs:
                if name == 'class' and value == 'pagerTitleCell':
                    self.__itemflg = True
        # 处理专利标题中因上标、下标导致多次返回data（如化合物名称、数学符号等）
        elif tag in self.__insubtags:
            if self.__flag == 1:
                self.__insubflag = True
        else:
            self.__flag = 0

    def handle_endtag(self, tag):
        tag = tag.strip()
        # 生成专利标题
        if tag == 'a' and self.__flag == 1:
            self.__sequence.append(self.__subject)
            self.__insubflag = False
            self.__subject = ''
        elif tag == 'span' and self.__pagecountflg:
            self.__pagecountflg = False
        if tag == 'div' and self.__itemflg:
            self.__itemflg = False

    def handle_data(self, data):
        data = data.strip()
        if self.__pagecountflg:
            self.page_count = data[str(data).find('/') + 1:]
            self.__pagecountflg = False
        if self.__itemflg:
            self.item_count = data[3:len(data) - 4]
        if self.__flag == 1:
            self.__subject += data
        # 生成四个字段：发明人、申请人、申请日期、公开日期
        if self.__flag in range(2, 6) and data:
            self.__sequence.append(data)

    # 公开函数：返回查询结果
    def get_result(self):
        self.__result = []
        if len(self.__sequence) % 6 != 0:
            # 保留：用于检验特殊符号造成解析html失败
            # print "Parser error!"
            print(len(self.__sequence))
            _mod = len(self.__sequence) % 6
            for i in range(int(len(self.__sequence)) / 6):
                if 'CN' in self.__sequence[6 * i].encode('utf8') and 'CN' in  self.__sequence[6 * i + _mod]:
                    self.__sequence = self.__sequence[:6 * i] + self.__sequence[6 * i + _mod:]
            for i in range(int(len(self.__sequence)) / 6):
                print self.__sequence[6 * i].encode('utf8')
            # print(self.__sequence)
            #for each in self.__sequence[-6:]:
               #  print each
            # exit(-1)
        if self.append_info == '':
            for i in range(1, int(len(self.__sequence) / 6) + 1):
                self.__result.append(
                    [
                        self.__sequence[6 * i - 6], self.__sequence[6 * i - 5], self.__sequence[6 * i - 4],
                        self.__sequence[6 * i - 3], self.__sequence[6 * i - 2], self.__sequence[6 * i - 1]
                    ]
                )
        else:
            for i in range(1, int(len(self.__sequence) / 6) + 1):
                self.__result.append(
                    [
                        self.__sequence[6 * i - 6], self.__sequence[6 * i - 5], self.__sequence[6 * i - 4],
                        self.__sequence[6 * i - 3], self.__sequence[6 * i - 2], self.__sequence[6 * i - 1],
                        self.append_info
                    ]
                )
        self.__sequence = []
        return self.__result

    def feed(self, data):
        # 关键：删除html文档中以"&"开头的各种转义字符
        self.rawdata = self.rawdata + self.unescape(data).replace('&', '')
        self.goahead(0)


if __name__ == '__main__':
    myparser = PatentParser('experiment')

    for year in ['2012', '2013']:
        result = dict()
        start = datetime.datetime(int(year), 1, 1)
        end = datetime.datetime(int(year), 12, 31)
        _time = datetime.datetime(int(year), 1, 1)

        w_flag = 0
        while _time <= end:
            print(_time)
            _timeb = _time + datetime.timedelta(days=0)
            if _timeb > end:
                _timeb = end
    
            i = 0 
            count = 1
            tmp = list()
            while count != 0:
                myparser.feed(CnkiSpider('*', str(_time.year) + '-' + str(_time.month) + '-' + str(_time.day), str(_timeb.year) + '-' + str(_timeb.month) + '-' + str(_timeb.day)).goto_page(i))
                tmp = myparser.get_result()
                count = len(tmp)
                for x in tmp:
                    if 'CN' not in x[0].encode('utf8'):
                        print('yes')
                    if x[0].encode('utf8') not in result:  
                        result[x[0].encode('utf8')] = x[3].encode('utf8')         

                i += 1
                print(str(len(result)) + '***')
            
            w_flag += 1
            if w_flag % 10 == 0:   
                with open(year + '.json', 'w') as f:
                    json.dump(result, f)

            _time += datetime.timedelta(days=1)
        
        with open(year + '.json', 'w') as f:
            json.dump(result, f)



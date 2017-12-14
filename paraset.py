# -*- coding: utf-8 -*-
"""
设置对cnki的查询参数
"""
import time

# 省别代码：可设置
search = {'GDM': ''}

def __build_query(value):
    par = {'txt_1_relation': '#CNKI_AND', 'txt_1_special1': '='}
    i = 0
    for v in value:
        i = i + 1
        par['txt_%d_sel' % i] = v
        par['txt_%d_value1' % i] = value[v]
        par['txt_%d_relation' % i] = '#CNKI_AND'
        par['txt_%d_special1' % i] = '='
    return par

# connecting所需要的参数
def make_parameters(patent_code, start_time, end_time):
    parameter = {
        'action': '',
        'NaviCode': patent_code,
        'ua': '1.21',
        'PageName': 'ASP.brief_result_aspx',
        'DbPrefix': 'SCPD',
        'DbCatalog': '中国专利数据库',
        'ConfigFile': 'SCPD.xml',
        'db_opt': 'SCPD',
        'db_value': '中国专利数据库',
        'publishdate_from': start_time,
        'publishdate_to': end_time,
        'his': '0',
        '__': time.strftime('%a %b %d %Y %H:%M:%S') + ' GMT+0800 (中国标准时间)',
    }
    parameters = dict(parameter, **__build_query(search))
    return parameters

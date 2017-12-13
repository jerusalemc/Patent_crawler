# coding=utf-8
import json
import xlsxwriter
import sys  
reload(sys)  
sys.setdefaultencoding('utf-8')

name = '2010'
with open(name + '.json', 'r') as f:
    _all = json.load(f)
   # print(type(_all))
print(len(_all))
result_fm = dict()
result_xx = dict()
result_wg = dict()
for key in _all.keys():
    if 'CN' not in key:
        continue
    flag = key[6] if key[2:6] == '2010' else key[2]    
    tmp = _all[key].encode('utf8').split(';')
    tmp = sorted(tmp)
    _all[key] = ''
    for j in tmp:
        _all[key] += j + ';'
    _all[key] = _all[key][:-1]
    # print(_all[key])
    # break
    if flag == '1':
      #  print(_all[key])
       # break
        if _all[key] not in result_fm.keys():
            result_fm[_all[key]] = 1
        else:
            result_fm[_all[key]] += 1
    elif flag == '2':
        if _all[key] not in result_xx.keys():
            result_xx[_all[key]] = 1
        else:
            result_xx[_all[key]] += 1
    elif flag == '3':
        if _all[key] not in result_wg.keys():
            result_wg[_all[key]] = 1
        else:
            result_wg[_all[key]] += 1
    else:
        print(key)
all_keys = set(list(result_fm.keys()) + list(result_xx.keys()) + list(result_wg.keys()))
print(len(result_fm), len(result_xx), len(result_wg))
workbook = xlsxwriter.Workbook(name + '.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write(0, 0, '企业名')
worksheet.write(0, 1, '专利总数')
worksheet.write(0, 2, '发明专利')
worksheet.write(0, 3, '实用新型')
worksheet.write(0, 4, '外观设计')


row = 1
for key in all_keys:
    total = 0
    worksheet.write(row, 0, key)
    if key in result_fm.keys():
        total += result_fm[key]
        worksheet.write(row, 2, result_fm[key])

    if key in result_xx.keys():
        total += result_xx[key]
        worksheet.write(row, 3, result_xx[key])

    if key in result_wg.keys():
        total += result_wg[key]
        worksheet.write(row, 4, result_wg[key])
    worksheet.write(row, 1, total)
    row += 1

workbook.close()

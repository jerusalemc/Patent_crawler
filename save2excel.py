# coding=utf-8
import json
import xlsxwriter
import sys  
reload(sys)  
sys.setdefaultencoding('utf-8')

def save(year):
    with open(year + '.json', 'r') as f:
        _all = json.load(f)

    print(len(_all))
    result_fm = dict()   # 发明专利dict：{企业名：数量, ...}
    result_xx = dict()   # 实用创新dict: {企业名：数量, ...}
    result_wg = dict()   # 外观设计dict: {企业名：数量, ...}
    for key in _all.keys():

        if 'CN' not in key:  # 爬取的数据应该是: {公开号: 企业名}
            continue

        # 2003.10.1 - ？的公开号：'CN20041...' 或者 'CN1....', 其中的1表示发明专利，如果是2表示实用创新，3表示外观设计
        # 1985.1.1 - 2003.9.30 的公开号：'CN851...' 或者 'CN1...'
        if key[2:6] == year:  
            flag = key[6]
        elif key[2:4] == year[2:4]:
            flag = key[4]
        else:
            flag = key[2]

        # 保证 '张三;李四' 和 '李四;张三' 被识别为同一个企业
        tmp = _all[key].encode('utf8').split(';')
        tmp = sorted(tmp)
        _all[key] = ''
        for j in tmp:
            _all[key] += j + ';'
        _all[key] = _all[key][:-1]

        # 统计三个类别每个企业的专利数量
        if flag == '1':
            if _all[key] not in result_fm:
                result_fm[_all[key]] = 1
            else:
                result_fm[_all[key]] += 1
        elif flag == '2':
            if _all[key] not in result_xx:
                result_xx[_all[key]] = 1
            else:
                result_xx[_all[key]] += 1
        elif flag == '3':
            if _all[key] not in result_wg:
                result_wg[_all[key]] = 1
            else:
                result_wg[_all[key]] += 1
        else:
            print(key)

    # 存到excel，思路是获取所有的企业名，然后分别查找三个类别该企业的专利数量，作为一行存入文件
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
        if key in result_fm:
            total += result_fm[key]
            worksheet.write(row, 2, result_fm[key])

        if key in result_xx:
            total += result_xx[key]
            worksheet.write(row, 3, result_xx[key])

        if key in result_wg:
            total += result_wg[key]
            worksheet.write(row, 4, result_wg[key])
        worksheet.write(row, 1, total)
        row += 1

    workbook.close()


if __name__ == '__main__':
    year = '2015'
    save(year)

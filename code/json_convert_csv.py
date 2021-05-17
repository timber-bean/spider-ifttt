# -*- coding: utf-8 -*-

import csv
import json

with open('20210517.json', 'r', encoding='utf-8') as f:
    rows = []
    for line in f.readlines():
        row = json.loads(line.strip())
        rows.append(row)


# 创建文件对象，newline用于设置空行问题
f = open('20210517.csv', 'w', newline='', encoding='utf-8')

# 通过文件创建csv对象
csv_write = csv.writer(f)

# writerow: 按行写入，　writerows: 是批量写入
# 写入数据 取列表的第一行字典，用字典的key值做为头行数据
csv_write.writerow(rows[0].keys())

# 循环里面的字典，将value作为数据写入进去
for row in rows:
    csv_write.writerow(row.values())
    
# 关闭打开的文件
f.close()


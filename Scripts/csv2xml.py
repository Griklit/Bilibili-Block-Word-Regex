import os
import csv

# 输入文件夹路径
input_folder = '../Regex'

# 生成XML头部
xml_output = '<filters>\n'

# 遍历文件夹中的每个CSV文件
for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):
        # 去掉文件名的后缀
        file_name_without_extension = os.path.splitext(filename)[0]

        # 读取CSV文件，分隔符设置为制表符
        with open(os.path.join(input_folder, filename), newline='', encoding='utf-8') as csvfile:
            csvreader = csv.DictReader(csvfile, delimiter='\t')
            rows = list(csvreader)

        # 添加文件名注释，去掉后缀
        xml_output += f'\n    <!-- {file_name_without_extension} -->\n'

        # 生成XML元素
        for row in rows:
            xml_output += f'    <item enabled="true">r={row["正则"]}</item> <!-- {row["备注"]} -->\n'

# 生成XML尾部
xml_output += '</filters>'

# 写入XML文件
with open('output.xml', 'w', encoding='utf-8') as xmlfile:
    xmlfile.write(xml_output)
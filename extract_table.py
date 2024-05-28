import os
import re
import json

# 定义目录路径
directory_path = 'D:\DDE\Structured_Documentation\data\paper_1000\Geophysics_500_latex'
dst_dir = "D:\DDE\Structured_Documentation\data\paper_1000\Geophysics_500_latex_table"

# 如果目标目录不存在，则创建它
if not os.path.exists(dst_dir):
    os.makedirs(dst_dir)

# 初始化一个空字典来存储过滤情况
data_dict = {}

# 遍历二级目录中的所有文件
for root in os.listdir(directory_path):
    files = os.path.join(directory_path, root)
    for file in os.listdir(files):
        if file.endswith('.tex'):
            # 拼接完整的文件路径
            file_path = os.path.join(files, file)

            # 尝试打开文件并读取内容
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    contents = f.readlines()
            #except (UnicodeDecodeError, PermissionError) as e:
                # print(f"Error decoding file {file_path}: {e}")
            except:
                continue

            # 找到的表数目
            table_nums = 0
            # 过滤后的表数目
            retable_nums = 0
            # 文献引用过滤数目
            cite = 0
            # 图表引用过滤数目
            graphic = 0
            # 交叉引用过滤数目
            ref = 0
            # 空值过滤数目
            blank = 0
            # 嵌套过滤数目
            nested = 0

            # 过滤掉以'%'开头的行
            content = [line for line in contents if not line.startswith('%')]
            content = '\n'.join(content)  # 使用换行符连接行

            # 使用正则表达式查找所有tabular段落
            tabular_pattern = re.compile(r'\\begin\{tabular\}.*?\\end\{tabular\}', re.DOTALL)
            tabular_matches = re.findall(tabular_pattern, content)

            # 计数
            table_nums += len(tabular_matches)

            # 为每个找到的tabular段落创建新的.txt文件
            for index, match in enumerate(tabular_matches):
                # 如果match中包含"\includegraphics"，则跳过当前循环
                if "\\includegraphics" in match:
                    graphic += 1
                    continue

                if "\\ref" in match:
                    ref += 1
                    continue

                if "\\cite" in match:
                    cite += 1
                    continue

                if len(re.findall(r'\\begin\{tabular\}', match)) > 1:
                    nested += 1
                    continue

                if match.count('\n') < 3:
                    blank += 1
                    continue

                # 构造目标子目录的路径
                dst_subdir = os.path.join(dst_dir, root)

                # 如果目标子目录不存在，则创建它
                if not os.path.exists(dst_subdir):
                    os.makedirs(dst_subdir)

                # 生成新文件的名称
                # new_file_name = f'{file[:-4]}_table_{index + 1}.txt'
                new_file_name = f'table_{index + 1}.txt'
                new_file_path = os.path.join(dst_subdir, new_file_name)

                # 计数
                retable_nums += 1

                # 将找到的tabular段落写入新文件
                with open(new_file_path, 'w', encoding='utf-8') as new_file:
                    new_file.write(match)

            # 为每个id创建一个包含5个键值对的子字典
            sub_dict = {
                'pre': table_nums,
                'cite': cite,
                'ref': ref,
                'graphic': graphic,
                'blank': blank,
                'nested': nested,
                'pro': retable_nums
            }

            # 将子字典添加到主字典中，以id作为key
            data_dict[root.split('\\')[-1]] = sub_dict

            try:
                print(f'Processed file: {file_path}')
            except:
                continue

print(data_dict)
# 将字典保存到JSON文件中
with open(os.path.join(dst_dir, 'data_filtering.json'), 'w', encoding='utf-8') as file:
    json.dump(data_dict, file, ensure_ascii=False, indent=4)

print('All files processed.')
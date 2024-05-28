import os
import re

# 定义目录路径
directory_path = 'E:\data\paper_500\Geophysics_500_latex'
dst_dir = "E:\data\paper_500\Geophysics_500_latex_formula"

# 如果目标目录不存在，则创建它
if not os.path.exists(dst_dir):
    os.makedirs(dst_dir)

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

            # 过滤掉以'%'开头的行
            content = [line for line in contents if not line.startswith('%')]
            content = '\n'.join(content)  # 使用换行符连接行

            # 使用正则表达式查找所有段落
            pattern1 = re.compile(r'\\begin\{align*\}.*?\\end\{align*\}', re.DOTALL)
            pattern2 = re.compile(r'\\begin\{eqnarray\}.*?\\end\{eqnarray\}', re.DOTALL)
            pattern3 = re.compile(r'\\begin\{equation*\}.*?\\end\{equation*\}', re.DOTALL)
            pattern4 = re.compile(r'\\begin\{gather*\}.*?\\end\{gather*\}', re.DOTALL)

            matches1 = re.findall(pattern1, content)
            matches2 = re.findall(pattern2, content)
            matches3 = re.findall(pattern3, content)
            matches4 = re.findall(pattern4, content)

            matches = matches1+matches2+matches3+matches4

            # 为每个找到的段落创建新的.txt文件
            for index, match in enumerate(matches):
                # 构造目标子目录的路径
                dst_subdir = os.path.join(dst_dir, root)

                # 如果目标子目录不存在，则创建它
                if not os.path.exists(dst_subdir):
                    os.makedirs(dst_subdir)

                # 生成新文件的名称
                new_file_name = f'formula_{index + 1}.txt'
                new_file_path = os.path.join(dst_subdir, new_file_name)

                # 将找到的段落写入新文件
                with open(new_file_path, 'w', encoding='utf-8') as new_file:
                    new_file.write(match)
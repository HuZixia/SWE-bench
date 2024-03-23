# # -*- coding: utf-8 -*-
# # @Time      : 2024/3/19 23:25
# # @Author    : RedHerring
# # @FileName  : test
# # @微信公众号  : AI Freedom
# # @知乎       : RedHerring


import pyarrow.parquet as pq
import pandas as pd
import os
import json

# 指定要读取的Parquet文件路径
# https://huggingface.co/datasets/princeton-nlp/SWE-bench_oracle/tree/main
parquet_dir = '/Users/huzixia/Documents/Develop/PyCharm/SWE-bench/princeton-nlp/'


# 指定要查找的键和值列表
keys_to_keep = ['instance_id', 'patch', 'test_patch']



# 创建一个空列表用于存储符合条件的数据行
matched_rows = []

# 遍历Parquet文件目录
for filename in os.listdir(parquet_dir):
    if filename.endswith('.parquet'):
        # 读取Parquet文件
        file_path = os.path.join(parquet_dir, filename)
        table = pq.read_table(file_path)
        
        # 将PyArrow表格转换为Pandas DataFrame
        df = table.to_pandas()
        df = df[keys_to_keep]
        
        # 将符合条件的数据行添加到列表中
        matched_rows.extend(df.to_dict('records'))

# 将结果保存为JSON文件
json_file = 'ground_truth.json'
with open(json_file, 'w') as f:
    json.dump(matched_rows, f, indent=4)
    
print(f"数据已保存到 {json_file}")





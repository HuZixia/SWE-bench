import json
from collections import OrderedDict

# 读取JSON文件
with open('./ground_truth.json', 'r') as f:
    json_data = json.load(f)

# 读取有序字典
ordered_dict = OrderedDict({
    'gpt-4-turbo-preview-default-prompt': './gpt-4-turbo-preview__SWE-bench_oracle__test.jsonl',
    'react-gpt-4-turbo-preview-default-prompt': './react-gpt-4-turbo-preview__SWE-bench_oracle__test.jsonl'
})

# 1. 获取JSON文件中每个JSON的key=instance_id的值
json_ids = [j['instance_id'] for j in json_data]


# 2. 获取有序字典中每个JSONL文件的key=instance_id的值
ordered_dict_ids = []
for name, file in ordered_dict.items():
    file_ids = []
    with open(file, 'r') as f:
        for line in f:
            data = json.loads(line)
            file_ids.append(data['instance_id'])
    ordered_dict_ids.append(file_ids)


# 3. 取交集作为需要输出的key list
output_ids = json_ids.copy()
# print(output_ids)
for file_ids in ordered_dict_ids:
    # print(file_ids)
    output_ids = list(set(output_ids) & set(file_ids))

print(output_ids)

# 4. 读取JSON文件，取出需要的键值对
ground_truth_data = []
for j in json_data:
    if j['instance_id'] in output_ids:
        ground_truth_data.append({
            'instance_id': j['instance_id'],
            'patch': j.get('patch', ''),
            'test_patch': j.get('test_patch', '')
        })


# 5. 读取有序字典中的JSONL文件，取出需要的键值对
ordered_dict_data_records = []
for name, file_path in ordered_dict.items():
    file_data = []
    with open(file_path, 'r') as f:
        for line in f:
            data = json.loads(line)
            if data['instance_id'] in output_ids:
                file_data.append({
                    'instance_id': data['instance_id'],
                    'model_patch': data['model_patch']
                })
    ordered_dict_data_records.append((name, file_data))




# 6. 合并结果并输出到JSON格式文件
output_data = []
for gt_data in ground_truth_data:
    instance_id = gt_data['instance_id']
    patch = gt_data['patch']
    text_patch = gt_data['test_patch']
    model_patches = [od_data['model_patch'] for od_name, od_file_data in ordered_dict_data_records for od_data in od_file_data if od_data['instance_id'] == instance_id]
    names = [od_name for od_name, od_file_data in ordered_dict_data_records for od_data in od_file_data if od_data['instance_id'] == instance_id]
    output_data.append({
        'instance_id': instance_id,
        'ground_truth_patch': patch,
        'ground_truth_test_patch': text_patch,
        **{f"{name}_model_patch": model_patch for name, model_patch in zip(names, model_patches)}
    })

with open('output.json', 'w') as f:
    json.dump(output_data, f, indent=2)


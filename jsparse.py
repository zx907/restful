"""
reformat test.json file into correct json format and convert to json object
"""

import json
import re
with open(r'C:\Users\Xu\PycharmProjects\RestfulService\static\test1.json', 'rb') as f:
    s = f.read().decode()
    # print(type(s))

    s = re.sub(r'ObjectId\(\s*(\"[\d\w]+\")\s*\)', r"\1", s)
    # print(s)

    stack = []
    json_string = ""
    json_list = []
    for line in s:
        if '{' in line:
            stack.append('{')
        elif '}' in line:
            stack.pop()
            if stack == []:

                json_string += line
                json_obj = json.loads(json_string)
                json_list.append(json_obj)
                # print(json_string)
                # print("="*10)
                json_list.append(json.loads(json_string))
                # json.loads(json_string)
                json_string = ""
                continue
        # if stack != []:
        json_string += line



    print(json_list)
import json
import re

def get_json_obj_list(s):
    s = s.decode('utf-8')
    s = re.sub(r'ObjectId\(\s*(\"[\d\w]+\")\s*\)', r"\1", s)

    stack = []
    json_string = ""
    # print(json_string)
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
                json_string = ""
                continue
        json_string += line
    return json_list
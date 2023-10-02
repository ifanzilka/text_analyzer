

def read_file_txt(path):
    string = ""
    with open('first.txt') as f:
        for line in f:
            string += line
    return string




print(read_file_txt("first.txt"))

# dict_person = {}
# with open('first.txt') as f:
#     for line in f:
#         print(line)
#         tmp = line.strip()
        
#         splitting = tmp.split(":")
#         #print(splitting)
#         if len(splitting) > 2:

#             name = splitting[2].split("-")[1]
#             #print(name)
#         #print(splitting)
#             if name in dict_person:
#                 dict_person[name].append(splitting[3])
#             else:
#                 dict_person[name] = [splitting[3]]

# print(dict_person)
def read_file_txt(path):
    string = ""
    with open(path) as f:
        for line in f:
            string += line
    return string

def _parising_text_to_user(string):
    dict_person = {}
    string_list = string.split("\n")
    for line in string_list:
        #print(line)
        line = line.strip()
        splitting = line.split(":")
        #print(splitting)
        
        if len(splitting) > 2:

            time_str = splitting[0].split(" ")[1] + ":" + splitting[1] + ":" + splitting[2].split("-")[0]
            #print(time_str)
            name = splitting[2].split("-")[1]
            name = name.split(" ")[1]

            if name in dict_person:
                dict_person[name][0].append(splitting[3])
                dict_person[name][1].append(time_str)
            else:
                dict_person[name] = [[splitting[3]], [time_str]]
    #print(dict_person)
    return (dict_person)

def _parising_text_to_diaolog(string):
    
    list_text = []
    list_time = []

    string_list = string.split("\n")
    for line in string_list:
        #print(line)
        line = line.strip()
        splitting = line.split(":")
        #print(splitting)
        
        if len(splitting) > 2:

            time_str = splitting[0].split(" ")[1] + ":" + splitting[1] + ":" + splitting[2].split("-")[0]
            #print(time_str)
            name = splitting[2].split("-")[1]
            name = name.split(" ")[1]

            list_text.append(splitting[3])
            list_time.append(time_str)

    #print(dict_person)
    return (list_text, list_time)
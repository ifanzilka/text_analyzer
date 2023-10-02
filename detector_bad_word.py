from transformers import BertTokenizer, BertForSequenceClassification
import torch
import numpy as np
import json

with open("./utilsid2topic.json") as f:
    target_vaiables_id2topic_dict = json.load(f)


##
from scripts.parsing import read_file_txt, _parising_text_to_user, _parising_text_to_diaolog

class BadThemeAnalyzer:

    #"Класс для анализа стенограммы SberJazz на предмет разговора на запрещенные темы"

    def __init__(self, model_name = 'Skoltech/russian-sensitive-topics') -> None:
        self.model_name = model_name
        self.tokenizer = BertTokenizer.from_pretrained(self.model_name)
        self.model = BertForSequenceClassification.from_pretrained(self.model_name)
        
        self.MAGIC_NUM_BAD = 6.5 ###Магическое чсило которое дает понять что человек часто говорит за запрещенные темы, было получено в ходе исследования нескольких стенограмм


    ## подфункция которая берет самую выскокую вероятность из всех тем
    def adjust_multilabel(self, y, is_pred = False):
        y_adjusted = []
        for y_c in y:
            y_test_curr = [0] * 19
            #print(y_c)
            index = str(int(np.argmax(y_c)))
            y_c = target_vaiables_id2topic_dict[index]
        return y_c


    ### функция которая анализирует один текстовый промт
    def predict_text(self, text):
        
        tokenized = self.tokenizer.batch_encode_plus([text],max_length = 512,
            pad_to_max_length=True,
            truncation=True,
            return_token_type_ids=False)
        tokens_ids,mask = torch.tensor(tokenized['input_ids']),torch.tensor(tokenized['attention_mask'])
        with torch.no_grad():
            model_output = self.model(tokens_ids,mask)

        preds = self.adjust_multilabel(model_output['logits'], is_pred = True)

        return preds


    def file_analyz(self, path_file):
        string = read_file_txt(path_file)

        return self.string_text_to_text(string)

    ## фугкция для анализа всей стенограммы и его очистка
    def string_text_to_text(self, string):
        new_string = ""
        bad_person = []

        dict_person = {}
        cnt_dialog_user = {}
        string_list = string.split("\n")
        for line in string_list:
            line = line.strip()
            splitting = line.split(":")

            
            if len(splitting) > 2:


                name = splitting[2].split("-")[1]
                name = name.split(" ")[1]

                text_user = splitting[3]
                preds = self.predict_text(text_user)


                if preds != 'none':
                    new_str = f"{splitting[0]}:{splitting[1]}:{splitting[2]}:(Запрещенная тема)"

                    if name in dict_person:
                        dict_person[name].append(preds)
                    else:
                        dict_person[name] = [preds]
                else:
                    new_str = f"{splitting[0]}:{splitting[1]}:{splitting[2]}:{splitting[3]}"
                
                
                
                if name in cnt_dialog_user:
                    cnt_dialog_user[name] += 1

                else:
                    cnt_dialog_user[name] = 0
                
                new_string += new_str + "\n"


        for name in dict_person:
            if  cnt_dialog_user[name] / len(dict_person[name]) < self.MAGIC_NUM_BAD:
                bad_person.append({"name":name, "bad_theme":dict_person[name]})

        return new_string, bad_person



## убрать запрещенные темы и в конце вижимка кто про это говорил

if __name__ == "__main__":
    file1 = "./example_conf/first.txt"
    file2 = "./example_conf/bad_theme.txt"

    string = read_file_txt(file2)
    #text_proccesing_bad_word(string)
    textAnalizer = BadThemeAnalyzer()
    textAnalizer.string_text_to_text(string)
   


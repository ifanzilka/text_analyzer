from rich import print  # for better view
import torch
from aniemore.recognizers.text import TextRecognizer
from aniemore.models import HuggingFaceModel

model = HuggingFaceModel.Text.Bert_Tiny
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# tr - acronym for TextRecognizer from two first capital letters
tr = TextRecognizer(model=model, device=device)

import json

##
from scripts.parsing import read_file_txt, _parising_text_to_user, _parising_text_to_diaolog


class EmotitonAnalyzer:
    
    def __init__(self):
        self.model = HuggingFaceModel.Text.Bert_Tiny
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.tr = TextRecognizer(model=model, device=device)


    def predict_model(self, text):

        d_result = {}
        result = tr.recognize(text, return_single_label=False)


            
        d_result['negative'] = result['anger'] + result['disgust'] + result['disgust']  + result['sadness']
        d_result['positive'] = result['happiness'] + result['enthusiasm']
        d_result['neutral'] = result['neutral']

        return d_result
    


    def _analyz_one_person(self, name, list_text, list_time):
        neutral_sum = 0
        negative_sum = 0
        positive_sum = 0

        neutral_dict = []
        negative_dict = []
        positive_dict = []
        
        
        cnt = 0
        for text, time in zip(list_text, list_time):
            result = self.predict_model(text)
            
            
            neutral_sum += int(result['neutral'] * 100)
            negative_sum += int(result['negative'] * 100)
            positive_sum += int(result['positive'] * 100)


            neutral_dict.append({'time': time, "value": int(result['neutral'] * 100)})
            negative_dict.append({'time': time, "value": int(result['negative'] * 100)})
            positive_dict.append({'time': time, "value": int(result['positive'] * 100)})
            cnt += 1


        d_final = {}
        common_mode = ''
        if neutral_sum >= negative_sum and neutral_sum >= positive_sum:
            common_mode = 'neutral'
        elif negative_sum >= positive_sum and negative_sum >= neutral_sum:
            common_mode = "negative"
        else:
            common_mode = 'positive'

        d_final['common_mood'] = common_mode
        d_final['neutral'] = neutral_dict
        d_final['positive'] = positive_dict
        d_final['negative'] = negative_dict
        d_final['name'] = name

        #print(d_final)
        stats = {}
        stats['neutral'] = neutral_sum / cnt
        stats['positive'] = positive_sum / cnt
        stats['negative'] = negative_sum / cnt


        return d_final, stats


    def find_top_user(self, dict_stats):
        top_user_postive = "none"
        top_value_postive = 0.0

        top_user_negative = "none"
        top_value_negative = 0.0
        for key in  dict_stats:
            if top_user_postive == "none":
                top_user_postive = key
                top_value_postive = dict_stats[key]['positive']

                top_user_negative = key
                top_value_negative = dict_stats[key]['negative']
            else:
                
                if  dict_stats[key]['positive'] > top_value_postive:
                    top_value_postive = dict_stats[key]['positive']
                    top_user_postive = key

                if  dict_stats[key]['negative'] > top_value_negative:
                    top_value_negative = dict_stats[key]['negative']
                    top_user_negative = key

        return {"top_user_postive": top_user_postive, "top_value_postive": top_value_postive, "top_user_negative": top_user_negative, "top_value_negative": top_value_negative}


    def file2info(self, filename):
        string = read_file_txt(filename)

        return self.string2info(string)
    def string2info(self, string):
        dict_person = _parising_text_to_user(string)
        dict_stats = {}
        person_info = []

        for key in dict_person:
        #print(key)
            if len(key) <= 2:
                continue
            info, stats = self._analyz_one_person(key, dict_person[key][0], dict_person[key][1])
            dict_stats[key] = stats
            
            person_info.append(info)

        list_text, list_time = _parising_text_to_diaolog(string)
        info, stats = self._analyz_one_person('our_conference', list_text, list_time)
        top_users = self.find_top_user(dict_stats)


        # print(person_info)
        # print(top_users)

        return person_info, top_users




if __name__ == "__main__":
    string = read_file_txt("first.txt")
    #emotion_analiz(string)
    Ea = EmotitonAnalyzer()
    Ea.string2info(string)

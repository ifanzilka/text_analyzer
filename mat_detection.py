from scripts.parsing import read_file_txt


class RussianMatDetect:

    def __init__(self, path_bad_word = "./utils/russian_mat.txt"):

        self.bad_word = self.read_file_mat(path_bad_word)
        #print(self.bad_word)


    def read_file_mat(self, path):
    
        bad_word = []
        
        with open(path) as f:
            for line in f:
                bad_word.append(line.strip())
        
        return bad_word
    
    def distance(self, a, b): 
        "Cчитаем расстояние Левентштейна"
        n, m = len(a), len(b)
        if n > m:
            
            a, b = b, a
            n, m = m, n

        current_row = range(n + 1)
        for i in range(1, m + 1):
            previous_row, current_row = current_row, [i] + [0] * n
            for j in range(1, n + 1):
                add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
                if a[j - 1] != b[i - 1]:
                    change += 1
                current_row[j] = min(add, delete, change)

        return current_row[n]
    
    def check_mat_word(self, phrase):

        phrase = phrase.lower().replace(" ", "")
        for word in self.bad_word:
            #Разбиваем слово на части, и проходимся по ним.
            for part in range(len(phrase)):
                #Вот сам наш фрагмент.
                fragment = phrase[part: part+len(word)]
                #Если отличие этого фрагмента меньше или равно 25% этого слова, то считаем, что они равны.
                if self.distance(fragment, word) <= len(word)*0.25:
                    #Если они равны, выводим надпись о их нахождении.
                    #print("Найдено", word, "\nПохоже на", fragment)
                    return True
        return False


class ClearMatJazz:

    def __init__(self):
        self.detector_mat = RussianMatDetect()


    def parse_dialog(self, text):
        new_txt = ""
        words = text.split(" ")

        for word in words:
            res = self.detector_mat.check_mat_word(word)

            if res:
                new_txt += "*" * len(word)
            else:
                new_txt += word
            new_txt += " "
        return new_txt


    def clear_file(self, filename):

        string = read_file_txt(filename)

        new_string = ""

        string_list = string.split("\n")
        for line in string_list:
            line = line.strip()
            splitting = line.split(":")

            
            if len(splitting) > 2:


                name = splitting[2].split("-")[1]
                name = name.split(" ")[1]

                text_user = splitting[3]
                
                text_preprocc = self.parse_dialog(text_user)
                new_str = f"{splitting[0]}:{splitting[1]}:{splitting[2]}:{text_preprocc}"
                
                new_string += new_str + "\n"
        return new_string


if __name__ == "__main__":
    
    RMD = RussianMatDetect()
    RMD.check_mat_word("блядь")

    RUsMat = ClearMatJazz()

    new = RUsMat.clear_file("./example_conf/first.txt")
    print(new)
    

        
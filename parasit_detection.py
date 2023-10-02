class RussianParazitWordDetect:

    def __init__(self, path_bad_word = "./utils/russian_parazit.txt"):

        self.bad_word = self.read_file_parazit(path_bad_word)
        #print(self.bad_word)


    def read_file_parazit(self, path):
    
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
    
    def check_parazit_word(self, phrase):

        phrase = phrase.lower().replace(" ", "")
        for word in self.bad_word:
            #Разбиваем слово на части, и проходимся по ним.
            for part in range(len(phrase)):
                #Вот сам наш фрагмент.
                fragment = phrase[part: part+len(word)]
                #Если отличие этого фрагмента меньше или равно 25% этого слова, то считаем, что они равны.
                if self.distance(fragment, word) <= len(word)*0.25:
                    #Если они равны, выводим надпись о их нахождении.
                    print("Найдено", word, "\nПохоже на", fragment)
                    return True
        return False



if __name__ == "__main__":
    
    RMD = RussianParazitWordDetect()

    res = RMD.check_parazit_word("в самом деле")
    print(res)
    

        
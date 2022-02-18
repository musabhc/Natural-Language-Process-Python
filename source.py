import os
import fitz
file_counter = 0
words_math = []
words_of_math, words_of_medicine, words_of_history = [], [], []
with open("stop_words_english.txt",'r') as stop_words:
    stopwords = stop_words.read()
    stopwords = stopwords.split()
    #print(r) #stop words print


filedir = os.path.dirname(__file__) #File dir of .py file
test_p = os.path.join(filedir, 'test') # test files dir.
train_p = os.path.join(filedir, 'train') #train files dir.

paths_in_train = [os.path.join(train_p,i) for i in os.listdir(train_p)]
paths_in_test = [os.path.join(test_p,i) for i in os.listdir(test_p)]

bad_chars = [';', ':', '!',',', "(", ")" , "#" ,"[","]","{","}","&","¥","£","-","_", "."]

for folder in paths_in_train:
    full_text = []
    print(folder)
    for file in os.listdir(folder):
        print("Reading: ", file)
        file_direction = os.path.join(folder, file)
        with fitz.open(file_direction) as f:
            text_get = ""
            for page in f:
                text_get += page.get_text()
            last_words = text_get.split("\n")
            for words in last_words:
                words = words.lower()
                text = words.split(' ')
                for new in text:
                    full_text.append(new)
    clean_text = []
    for i in full_text:
        i = ''.join((filter(lambda k: k not in bad_chars, i)))
        if i != '' and len(i) >3:
            if i not in stopwords:
                clean_text.append(i)
    print(clean_text)
    #Categorizing
    if os.listdir(train_p)[file_counter] == "math":
        print("Math words are added to memory.")
        words_of_math = list(set(clean_text))
    elif os.listdir(train_p)[file_counter] == "medicine":
        print("Medicine words are added to memory")
        words_of_medicine = list(set(clean_text))
    elif os.listdir(train_p)[file_counter] == "history":
        print("History words are added to memory")
        words_of_history = list(set(clean_text))

    file_counter += 1

#TEST TIME
print("Files Reading")
for test_folder in paths_in_test:
    clean_text = []
    text = []
    full_text = []
    for test_file in os.listdir(test_folder):
        print("File Name: ", test_file)
        medicine_possibility, history_possibility, math_possibility = 0, 0, 0
        file_direction = os.path.join(test_folder, test_file)
        with fitz.open(file_direction) as fi:
            text_get = ""
            for page in fi:
                text_get += page.get_text()
            last_words = text_get.split("\n")
            for words in last_words:
                words = words.lower()
                text = words.split(' ')
                for new in text:
                    full_text.append(new)

        for h in full_text:
            h = ''.join((filter(lambda k: k not in bad_chars, h)))
            if h != '' and len(h) > 3:
                if h not in stopwords:
                    clean_text.append(h)

        for word in set(clean_text):
            for word_medicine in words_of_medicine:
                if word == word_medicine:
                    medicine_possibility += 1
            for word_math in words_of_math:
                if word == word_math:
                    math_possibility += 1
            for word_history in words_of_history:
                if word == word_history:
                    history_possibility += 1

        medicine_possibility = medicine_possibility / (len(set(words_of_medicine + clean_text)))
        history_possibility = history_possibility / (len(set(words_of_history + clean_text)))
        math_possibility = math_possibility / (len(set(words_of_math + clean_text)))

        print("PDF Name: " + test_file)
        print("Words about Medicine: " + str(medicine_possibility))
        print("Words about History: " + str(history_possibility))
        print("Words about Math: " + str(math_possibility))
        if medicine_possibility > math_possibility and medicine_possibility>history_possibility:
            print("It´s a Medicine PDF")
        elif math_possibility > medicine_possibility and math_possibility >history_possibility:
            print("It´s a Math PDF")
        elif history_possibility > medicine_possibility and history_possibility > math_possibility:
            print("It´s a History PDF")
        else:
            print("The PDF could not be categorized.")

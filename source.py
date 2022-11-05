import os
import fitz
file_counter = 0
words_math = []
words_of_math, words_of_medicine, words_of_history = [], [], []
# GETTING ALL STOP WORDS #
with open("stop_words_english.txt",'r') as stop_words:
    stopwords = stop_words.read()
    stopwords = stopwords.split()
    #print(r) #Stop Words Print | Test
###############################

filedir = os.path.dirname(__file__) # Location of .py files
test_p = os.path.join(filedir, 'test') # Location of test files
train_p = os.path.join(filedir, 'train') # Location of training files

paths_in_train = [os.path.join(train_p,i) for i in os.listdir(train_p)] # Finding out the location of subfolders
paths_in_test = [os.path.join(test_p,i) for i in os.listdir(test_p)] # Finding out the location of subfolders

punctuation = [';', ':', '!', ',', "(", ")" , "#" , "[", "]", "{", "}", "&", "¥", "£", "-", "_", "."]

# Word learning
for folder in paths_in_train:
    full_text = [] # List for all words
    print(folder) # Current folder
    for file in os.listdir(folder):
        print("Reading: ", file) # Current file
        file_direction = os.path.join(folder, file)

        with fitz.open(file_direction) as f:
            text_get = ""
            for page in f:
                text_get += page.get_text() #getting all words
            last_words = text_get.split("\n") #split text by lines
            for words in last_words:
                words = words.lower()
                text = words.split(' ') #split text by spaces
                for new in text:
                    full_text.append(new) # Words!
    clean_text = [] # List for clean words
    for i in full_text:
        i = ''.join((filter(lambda k: k not in punctuation, i))) # checking words
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

#TEST SECTION
print("Files Reading")

for test_folder in paths_in_test:
    clean_text = []
    text = []
    full_text = []

    for test_file in os.listdir(test_folder):
        print("File Name: ", test_file) # Print file name
        medicine_possibility, history_possibility, math_possibility = 0, 0, 0 # Possibilities
        file_direction = os.path.join(test_folder, test_file)
        # Find words
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
        # Check words
        for h in full_text:
            h = ''.join((filter(lambda k: k not in punctuation, h)))
            if h != '' and len(h) > 3:
                if h not in stopwords:
                    clean_text.append(h)

        # Finding same words
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

        medicine_possibility = medicine_possibility / (len(set(words_of_medicine + clean_text))) # the ratio of the same word count to the total word count
        history_possibility = history_possibility / (len(set(words_of_history + clean_text))) # the ratio of the same word count to the total word count
        math_possibility = math_possibility / (len(set(words_of_math + clean_text))) # the ratio of the same word count to the total word count

        #Printing the result
        print("PDF Name: " + test_file)
        print("Words about Medicine: " + str(medicine_possibility))
        print("Words about History: " + str(history_possibility))
        print("Words about Math: " + str(math_possibility))

        # deciding the outcome
        if medicine_possibility > math_possibility and medicine_possibility>history_possibility:
            print("It´s a Medicine PDF")
        elif math_possibility > medicine_possibility and math_possibility >history_possibility:
            print("It´s a Math PDF")
        elif history_possibility > medicine_possibility and history_possibility > math_possibility:
            print("It´s a History PDF")
        else:
            print("The PDF could not be categorized.")

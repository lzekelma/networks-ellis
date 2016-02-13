# Written by Siyu Chen based on Leo's Lemmatization code
# Created on Feb 12 2016
# 
import csv
from nltk.stem.wordnet import WordNetLemmatizer
import sys

def lemmatize_words(text_field):
    if text_field == "":
        return ""
    lower_case_text = text_field.lower()
    my_string_list = lower_case_text.split("||")
    lemmatizer_object = WordNetLemmatizer()
    lemmatized_string_list = []

    for each_word in my_string_list:
        each_word = each_word.rstrip().lstrip()
        if each_word == 'fell':
            lemmatized_string_list.append('fall')
        else:
            lemmatized_string_list.append(lemmatizer_object.lemmatize(each_word,'v'))
    lemmatized_string = '||'.join(lemmatized_string_list)
    return lemmatized_string



def process_one_question(each_row, cell_index, output_file):
    if each_row[cell_index] == "" or each_row[cell_index + 1] == "":
        return

    words = each_row[cell_index].split("||")[:-1]
    times = each_row[cell_index + 1].split("||")[:-1] # list of string

    for i in range(len(times)):
        times[i] = times[i].split(",")[0]

    for i in range(len(words)):
        for j in range(i+1, len(words)):
            if times[i] == "null" or times[j] == "null":
                continue
            output_string = " ".join([words[i], words[j], str(i+1), str(j+1), times[i], times[j], str(int(times[j]) - int(times[i]))])
            output_file.write(output_string + "\n")
            #sys.exit(0)
    return True



    

def main():
    # lemmatize responses and save to "lemmatized" csv file
    input_file = open("InputData/One_Minute_Responses_Merged.csv","r")
    one_minute_data = csv.reader(input_file)

    output_file = open("OutputData/One_Minute_Responses_Lemmatized_3.csv","w")
    one_minute_data_lemmatized = csv.writer(output_file)

    row_index = 0

    for each_row in one_minute_data:
        if row_index == 0 or row_index ==1:
            one_minute_data_lemmatized.writerow(each_row)
            row_index += 1
            continue

        each_row[21] = lemmatize_words(each_row[21])

        cell_index = 24

        while cell_index < len(each_row):
            each_row[cell_index] = lemmatize_words(each_row[cell_index])
            cell_index += 2

        one_minute_data_lemmatized.writerow(each_row)
        row_index += 1

    input_file.close()
    output_file.close()


    #################################################################################################
    
    # read in lemmatized responses and tranform into network data format
    input_file = open("OutputData/One_Minute_Responses_Lemmatized_3.csv","r")
    one_minute_data = csv.reader(input_file)

    output_file = open("OutputData/One_Minute_Responses_Network_Data.txt","w")
    
    row_index = 0
    for each_row in one_minute_data:
        if row_index == 0 or row_index ==1:
            row_index += 1
            continue


        # process the sample question explicitly
        # two weird rows that the first words cell does not start at index 21
        if row_index == 864:
            process_one_question(each_row, 22, output_file)
            cell_index = 25
        elif row_index == 635:
            process_one_question(each_row, 23, output_file)
            cell_index = 26
        
        else:
            process_one_question(each_row, 21, output_file)
            cell_index = 24


        # process the other quesitons and responses
        while cell_index < len(each_row):
            if (row_index == 394 and cell_index == 70) or (row_index == 532 and cell_index == 54): #special cells that do not have corresponding time
                cell_index += 1
                continue
            process_one_question(each_row, cell_index, output_file)
            cell_index += 2
        row_index += 1

    input_file.close()
    output_file.close()


if __name__ == "__main__":
    main()
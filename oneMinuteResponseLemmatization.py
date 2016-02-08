import csv
from nltk.stem.wordnet import WordNetLemmatizer

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
        lemmatized_string_list.append(lemmatizer_object.lemmatize(each_word,'v'))
    lemmatized_string = '||'.join(lemmatized_string_list)
    return lemmatized_string



def main():
    input_file = open("InputData/One_Minute_Responses_Merged.csv","r")
    one_minute_data = csv.reader(input_file)

    output_file = open("OutputData/One_Minute_Responses_Lemmatized_2.csv","w")
    one_minute_data_lemmatized = csv.writer(output_file)

    data_rows = []
    row_index = 0

    for each_row in one_minute_data:
        if row_index == 0 or row_index ==1:
            one_minute_data_lemmatized.writerow(each_row)
            row_index += 1
            continue

        cell_index = 0
        while cell_index < len(each_row):
            if cell_index == 21:
                each_row[cell_index] = lemmatize_words(each_row[cell_index])
                cell_index += 3
            elif cell_index >= 24:
                each_row[cell_index] = lemmatize_words(each_row[cell_index])
                cell_index += 2
            else:
                cell_index += 1

        data_rows.append(each_row)

    for each_data_row in data_rows:
        one_minute_data_lemmatized.writerow(each_data_row)

    input_file.close()
    output_file.close()

if __name__ == "__main__":
    main()
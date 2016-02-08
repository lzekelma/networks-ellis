import csv
import enchant

class SorterClass:
    def __init__(self):
        self.actual_word_count = 0
        self.non_word_count = 0
        self.single_letter_count = 0
        self.non_alpha_word_count = 0
        self.multi_word_count = 0
        self.other_count = 0
        self.enum = 1
        self.error_list = []

    def sort_words(self,lemmatized_string):
        d = enchant.Dict("en_US")
        if lemmatized_string == "":
            return ""
        lemmatized_list = lemmatized_string.split("||")
        sorted_list = []
        for each_word in lemmatized_list:
            if len(each_word) < 1:
                sorted_list.append("")
            elif len(each_word) == 1:
                self.single_letter_count += 1
                sorted_list.append("error: " + str(self.enum))
                self.error_list.append("(error: " + str(self.enum) + " " + each_word + ')')
                self.enum += 1
            elif each_word.count(' ') >= 1:
                self.multi_word_count += 1
                sorted_list.append("error: " + str(self.enum))
                self.error_list.append("(error: " + str(self.enum) + " " + each_word + ')')
                self.enum += 1
            elif each_word.isalpha() is False:
                self.non_alpha_word_count += 1
                sorted_list.append("error: " + str(self.enum))
                self.error_list.append("(error: " + str(self.enum) + " " + each_word + ')')
                self.enum += 1
            elif d.check(each_word) is False:
                self.non_word_count += 1
                sorted_list.append("error: " + str(self.enum))
                self.error_list.append("(error: " + str(self.enum) + " " + each_word + ')')
                self.enum += 1
            elif d.check(each_word):
                self.actual_word_count += 1
                sorted_list.append(each_word)
            else:
                self.other_count += 1
                sorted_list.append("error: " + str(self.enum))
                self.error_list.append("(error: " + str(self.enum) + " " + each_word + ')')
        sorted_string = '||'.join(sorted_list)
        return sorted_string


    def main(self):
        input_file = open("OutputData/One_Minute_Responses_Lemmatized_2.csv","r")
        one_minute_data = csv.reader(input_file)

        output_file = open("OutputData/One_Minute_Responses_Sorted.csv","w")
        one_minute_data_sorted = csv.writer(output_file)

        data_rows = []
        row_index = 0

        for each_row in one_minute_data:
            if row_index == 0 or row_index == 1:
                one_minute_data_sorted.writerow(each_row)
                row_index += 1
                continue

            cell_index = 0
            while cell_index < len(each_row):
                if cell_index == 21:
                    each_row[cell_index] = self.sort_words(each_row[cell_index])
                    cell_index += 3
                elif cell_index >= 24:
                    each_row[cell_index] = self.sort_words(each_row[cell_index])
                    cell_index += 2
                else:
                    cell_index += 1

            data_rows.append(each_row)

        for each_data_row in data_rows:
            one_minute_data_sorted.writerow(each_data_row)

        input_file.close()
        output_file.close()

        print("actual word count: ", self.actual_word_count)
        print("non word count: ", self.non_word_count)
        print("single letter count: ", self.single_letter_count)
        print("non alpha word count: ", self.non_alpha_word_count)
        print("multi word count: ", self.multi_word_count)
        print("other count: ", self.other_count)
        print("------------------------------\n")
        print(self.error_list)


if __name__ == "__main__":
    SorterClass().main()
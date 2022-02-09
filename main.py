import matplotlib.pyplot as plt
import math




def open_file(file_name):
    speech_dictionary = {}

    word_dictionary = {}

    first = 0
    middle = 0
    last = 0
    term = 0
    date = 0

    speech_len = 0

    sentence_len = 0
    sentence_list = []

    speech_sentence_dictionary = {}

    speech_complex_dictionary = {}

    end_sentence = ['.', '!', '?']

    complex_word_count = 0

    syllable_count = 0

    speech_syllable_dictionary = {}



    vowels = ['a', 'e', 'i', 'o', 'u']

    with open(file_name) as file:
        x = 0
        for row in file:

            row = row.split()
            if len(row) == 0:
                pass

            elif row[0] == '$':

                x += 1
                if x != 1:
                    speech_complex_dictionary[date] = complex_word_count / speech_len
                    speech_syllable_dictionary[date] = syllable_count
                    speech_sentence_dictionary[date] = sentence_list


                syllable_count = 0

                complex_word_count = 0


                sentence_list = []

                speech_len = 0
                row_len = len(row) - 1

                if row_len > 1:
                    first = row[1]

                    date = int(row[-1])

                if row_len == 5:
                    middle = row[2]
                    last = row[3]
                    term = row[4]

                elif row_len == 4 and len(row[3]) == 1:
                    middle = None
                    last = row[2]
                    term = row[3]

                if row_len == 4 and len(row[3]) != 1:
                    term = None
                    middle = row[2]
                    last = row[3]

                if row_len == 3:
                    middle = None
                    term = None
                    last = row[2]
            else:
                speech_len += len(row)

                for word in row:
                    letter_count = -1
                    word = word.lower()

                    sentence_len += 1

                    word_len = 0

                    for letter in word:
                        letter_count += 1
                        if letter.isalpha():
                            word_len += 1

                        if letter in vowels:
                            syllable_count += 1

                        if letter == 'a' and letter != word[-1]:
                            if word[letter_count + 1] == 'u':
                                syllable_count -= 1

                        elif letter == 'o' and letter != word[-1]:
                            if word[letter_count + 1] == 'y':
                                syllable_count -= 1

                            elif word[letter_count + 1] == 'o':
                                syllable_count -= 1

                        if letter == 'e' and letter != word[-1] and letter != word[-2]:
                            if word[letter_count + 1] == 'o' and word[letter_count + 2] == 'u':
                                syllable_count -= 1

                    if word_len >= 3 and word[-2] == 'l' and word[-1] == 'e':
                        if word[-3] not in vowels:
                            syllable_count += 1

                    elif word_len >= 4 and word[-3] == 'l' and word[-2] == 'e' and word[-1] == 's':
                        if word[-4] not in vowels:
                            syllable_count += 1

                    if word[-1] == 'e':
                        syllable_count -= 1



                    if word_len >= 8:
                        # print(word)
                        complex_word_count += 1

                    if word[-1] in end_sentence:
                        sentence_list.append(sentence_len)
                        sentence_len = 0



            speech_dictionary[date] = [first, middle, last, term, speech_len]

        # print(speech_sentence_dictionary)
        # print(speech_complex_dictionary)
        # print(speech_syllable_dictionary)
        return speech_dictionary, speech_sentence_dictionary, speech_complex_dictionary, speech_syllable_dictionary



# speech_dictionary = open_file('Speeches.txt')
#
#
# print(speech_dictionary)

def plot_data(speech_dictionary, mean, standard_dev, option = 1):

    year_list = []
    length_list = []

    for key, value in speech_dictionary.items():

        year_list.append(key)

        if option == 1:
            length_list.append(value[-1])
            plt.axis([year_list[0] - 10, year_list[-1] + 10, 0, max(length_list) + 100])

        elif option == 2:
            length_list.append(value[0])
            plt.axis([year_list[0] - 10, year_list[-1] + 10, 0, max(length_list) + 5])

        elif option == 3:
            length_list.append(value)
            plt.axis([year_list[0] - 10, year_list[-1] + 10, min(length_list) - .02, max(length_list) + .02])


    # print(year_list, length_list)




    plt.plot(year_list, length_list, '-b*')


    if option == 1:
        plt.title('SPEECH VS INAUGURAL YEAR :)')

        plt.plot([year_list[0], year_list[-1]], [mean, mean], '-r')

        plt.plot([year_list[0], year_list[-1]], [mean + standard_dev, mean + standard_dev], '-r')

        plt.plot([year_list[0], year_list[-1]], [mean - standard_dev, mean - standard_dev], '-r')





    plt.show()

    return length_list



def calculate_word_numbers(dictionary, start, end):
    mean = 0
    variance = 0
    standard_dev = 0
    median = 0
    big = 0
    small = 0

    number_list = []
    date_list = []

    new_word_dictionary = {}



    for key, value in dictionary.items():

        if int(key) >= start and int(key) <= end:
            # print(key, length)
            number_list = value
            date_list.append(key)

            mean = sum(number_list) / len(number_list)

            difference_list = []

            for number in number_list:
                difference_list.append((number - mean) ** 2)

            variance = sum(difference_list) / len(number_list)

            standard_dev = math.sqrt(variance)

            if len(number_list) % 2 == 0:
                middle = int((len(number_list) / 2) - 1)
                median = (number_list[middle] + number_list[middle + 1]) / 2

            else:
                middle = int((len(number_list) + 1) / 2)
                median = number_list[middle - 1]

            minimum = min(number_list)
            maximum = max(number_list)

            new_word_dictionary[key] = [mean, variance, standard_dev, median, maximum, minimum]

    # print(new_word_dictionary)
    plot_data(new_word_dictionary, mean, standard_dev, 2)
    # print(f'mean: {mean}, variance: {variance}, standard_dev: {standard_dev}, median: {median}, maximum: {maximum}, minimum: {minimum}')




def calculate_numbers(speech_dictionary, start, end):

    mean = 0
    variance = 0
    standard_dev = 0
    median = 0
    big = 0
    small = 0

    number_list = []
    date_list = []

    if start > end:
        print('ERROR START DATE IS GREATER THAN END DATE')
        return

    for key, value in speech_dictionary.items():
        length = value[-1]

        if int(key) >= start and int(key) <= end:
                # print(key, length)
                number_list.append(length)
                date_list.append(key)


    number_list.sort()

    mean = sum(number_list) / len(date_list)
    # print(mean)

    difference_list = []

    for number in number_list:
        difference_list.append((number - mean) ** 2)


    variance = sum(difference_list) / len(date_list)
    # print(variance)

    standard_dev = math.sqrt(variance)
    # print(standard_dev)
    # print(number_list)
    if len(number_list) % 2 == 0:
        middle = int((len(number_list) / 2) - 1)
        # print(middle)
        median = (number_list[middle] + number_list[middle + 1]) / 2

    else:
        middle = int((len(number_list) + 1) / 2)
        median = number_list[middle - 1]

    # print(median)

    minimum = min(number_list)
    maximum = max(number_list)

    return mean, variance, standard_dev, median, maximum, minimum


def gaussian_calculation(number_list, mean, standard_dev, variance):
    y_list = []
    x_list = []
    x_start = mean - 1.5 * standard_dev

    delta_x = (3 * standard_dev) / 100


    m_s = mean - standard_dev

    mps = mean + standard_dev
    for i in range(100):

        x = i * delta_x + x_start




        y = ( 1/(standard_dev * math.sqrt(2*math.pi)) ) * math.e ** - ( ((x - mean)** 2) / (2 * variance) )
        y_list.append(y)
        x_list.append(x)

        y_left = (1 / (standard_dev * math.sqrt(2 * math.pi))) * math.e ** - (((m_s - mean) ** 2) / (2 * variance))
        Left = y_left

        y_right = (1 / (standard_dev * math.sqrt(2 * math.pi))) * math.e ** - (((mps - mean) ** 2) / (2 * variance))
        Right = y_right






    plt.axis([mean - (1.5 * standard_dev), mean + (1.5 * standard_dev), min(y_list), max(y_list)])

    apex = max(y_list)

    plt.plot(x_list, y_list, '-b')

    plt.plot([mean, mean], [0, apex], '-r')

    plt.plot([mean - standard_dev, mean - standard_dev], [0, Left], '-r')

    plt.plot([mean + standard_dev, mean + standard_dev], [0, Right], '-r')



    plt.show()



def calculate_grade_level(speech_dictionary, speech_sentence_dictionary, speech_syllable_dictionary):

    y_vals = []

    x_vals = []


    for key, item in speech_dictionary.items():
        if int(item[-1]) != 0:
            tot_words = int(item[-1])

        tot_sentence = (len(speech_sentence_dictionary[key]))

        tot_syllable = speech_syllable_dictionary[key]

        x_vals.append(key)

        y = (.39 * (tot_words / tot_sentence)) + (11.8 * (tot_syllable / tot_words)) - 15.59

        y_vals.append(y)

    print(x_vals, y_vals)

    # plt.sublot(3, 1)



def main(filename):

    speech_dictionary, speech_sentence_dictionary, speech_complex_dictionary, speech_syllable_dictionary = open_file(filename)

    # print(speech_syllable_dictionary)

    calculate_word_numbers(speech_sentence_dictionary, 1789, 2021)

    # mean, variance, standard_dev, median, maximum, minimum = calculate_word_numbers(speech_sentence_dictionary, 1789, 2021)
    # print(f'mean: {mean}, variance: {variance}, standard_dev: {standard_dev}, median: {median}, maximum: {maximum}, minimum: {minimum}')

    mean, variance, standard_dev, median, maximum, minimum = calculate_numbers(speech_dictionary, 1789, 2021)
    print(f'mean: {mean}, variance: {variance}, standard_dev: {standard_dev}, median: {median}, maximum: {maximum}, minimum: {minimum}')

    plot_data(speech_complex_dictionary, mean, standard_dev, 3)

    number_list = plot_data(speech_dictionary, mean, standard_dev)


    calculate_grade_level(speech_dictionary, speech_sentence_dictionary, speech_syllable_dictionary)

    # mean, variance, standard_dev, median, maximum, minimum = calculate_numbers(speech_dictionary, 1936, 2021)
    # print(f'mean: {mean}, variance: {variance}, standard_dev: {standard_dev}, median: {median}, maximum: {maximum}, minimum: {minimum}')
    # print(median)

    gaussian_calculation(number_list, mean, standard_dev, variance)

main('Speeches.txt')
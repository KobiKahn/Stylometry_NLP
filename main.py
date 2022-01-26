# import matplotlib.pyplot as plt


def open_file(file_name):
    speech_dictionary = {}
    first = 0
    middle = 0
    last = 0
    term = 0
    date = 0

    row_len = 0
    speech_len = 0

    with open(file_name) as file:
        for row in file:

            row = row.split()

            if len(row) == 0:
                pass

            elif row[0] == '$' and len(row) != 0:

                speech_len = 0
                row_len = len(row) - 1

                first = row[1]

                date = row[-1]


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
                print(speech_len)

            speech_dictionary[date] = [first, middle, last, term, speech_len]

        print(speech_dictionary)
        return(speech_dictionary)


speech_dictionary = open_file('Speeches.txt')


print(speech_dictionary)



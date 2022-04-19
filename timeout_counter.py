import sys
import glob


# Get all files in folders and return as a list
def get_filenames():
    all_files = glob.glob('./**/*.txt', 
                   recursive = True)

    return all_files


# Returns number of occurances a string appears in a file
def check_if_string_in_file(file_name, string_to_search):
    iter = 0
    with open(file_name, 'r') as read_obj:
        for line in read_obj:
            if string_to_search in line:
                iter += 1
    return iter


# Prints out the results of how many times a TIME OUT string occurs
def create_table(serial_num):
    list_of_headers = {}
    files = get_filenames()
    for file in files:
        temp = file.split('.')
        file_name = temp[1]
        list_of_headers[file_name] = check_if_string_in_file(file, "TIMED OUT")

    print(list_of_headers)


def main(argv):
    serial_num = 0
    if len(argv) > 0:
        serial_num = int(argv[0])

    create_table(serial_num)


if __name__ == "__main__":
    main(sys.argv[1:])

    # root changes seem to consistently be between 22:00 and 23:00, as well as between 10:00 and 11:00 (MST)

# coding: utf-8

import re
import csv


def regex_search(pattern, file_name):
    remove_arr = []
    res = []
    remain_sms = []
    for sms in file_name:
        j = re.match(pattern, sms)
        if j is not None:
            res.append(j.groupdict())
            remove_arr.append(sms)
        else:
            remain_sms.append(sms)
    return res, remove_arr, remain_sms


def write_to_csv(result, csv_name):
    keys = result[0][0].keys()
    with open(csv_name, 'wb') as output_file:
        dict_writer = csv.DictWriter(output_file, keys, dialect='excel')
        dict_writer.writeheader()
        dict_writer.writerows(result[0])


def main():
    # Run this part only once in the starting. From here

    # change the directory to working folder and give the right filename (hdfcbk),
    # if unsure what to do go to your folder and right click and copy the file here,
    # it will look like /home/XYZ/.../Your_folder_name/hdfcbk
    with open('hdfcbk', 'r') as smsFile:
        data = smsFile.read()
    data = data.split('\n')
    main_data = data
    regl = []

    pat1 = 'INR (?P<Amount>(.*)) deposited to A\/c No (?P<AccountNo>(.*)) towards (?P<Towards>(.*)) Val (?P<Date>(.*)). Clr Bal is INR (?P<Balance>(.*)) subject to clearing.'

    # TODO - Use much more descriptive names...no idea what's going on here without searching for a while
    a, b, c = regex_search(pat1, main_data)

    # Updating main_data to remaining messages
    main_data = c

    # Writing remaining sms to a file, you don't need to change the file name as it will be updated
    # everything as you run the script. Just look at the remaining sms and make new regex.
    with open('remaining_sms.txt', 'w') as fp:
        fp.write('\n'.join('{}'.format(x) for x in main_data))

    # Update the csv file
    write_to_csv([a, b, c], 'hdfc_test_3.csv')

    # Keeping all the regexes in one list, update the index number in [i, pat1]
    regl.append([1, pat1])

    # Writing the regex index to csv, run this part in the end, or if you're unsure that you will
    # make the mistake run this part and keep changing the output file name.
    with open("output.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(regl)


if __name__ == "__main__":
    main()

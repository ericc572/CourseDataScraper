from io import StringIO
import re
import csv
import sys

def parseText(fileName):
  outfile = sys.argv[2]
  course_match = r"^([A-Z]{2,4})(\W+|\s+)\d+[A-Z]?"
  transfer_match = r"←\s+[A-Z]{2,4}(\W+|\s+)\d+[A-Z]?"
  date_reg = r"\d{4}-\d{4}"
  transfer_courses = []
  host_courses = []

  or_circuit = False
  mappings = {}
  with open(fileName) as f:
    lines = (line.rstrip() for line in f) # All lines including the blank ones
    lines = (line for line in lines if line) # Non-blank lines
    # print(lines)
    for line in lines:
      if line.startswith("To"):
        to_college = line.split(":")[1]

      if line.startswith("From"):
        from_college = line.split(":")[1]
        date = re.match(date_reg, next(lines)).group(0)
        major = next(lines)

      is_host_course = re.match(course_match, line)
      is_transfer_course = re.match(transfer_match, line)

      if is_host_course:
        if or_circuit:
          host_courses[-1] += " ### OR ### "
          host_courses[-1] += is_host_course.group(0)
          or_circuit = False
        else:
          host_courses.append(is_host_course.group(0))


      elif is_transfer_course:
        clean_transfer = re.sub('← ', '', is_transfer_course.group(0))
        if or_circuit:
          transfer_courses[-1] += " ### OR ### "
          transfer_courses[-1] += clean_transfer
          or_circuit = False
        else:
          transfer_courses.append(clean_transfer)

      elif "--- Or ---" in line:
        or_circuit = True
        print("OR FOUND")
        continue

    print("**** COURSE TRANSFERS FOR MAJOR: ", major)
    print("COURSE CATALOG AS OF:", date)
    print("FROM COLLEGE:", from_college)
    print("TO COLLEGE:", to_college)
    print("host courses:", host_courses)
    print("transfer courses:", transfer_courses)
    mappings = dict(zip(transfer_courses, host_courses))

    print("------------------------------")
    print("COURSE MAPPINGS:")
    print("COURSE MAPPINGS OF FROM => TO:", mappings)

    print("WRITING TO CSV...")
    writeToCSV(outfile, major, date, from_college, to_college, mappings)

def writeToCSV(outfile, major, date, from_college, to_college, mappings):
  f = open(outfile, 'w')
  with f:
    columns = ['Department/Major', 'Catalog As Of', 'From', 'To', 'Transfer Course', 'Destination Course']
    writer = csv.DictWriter(f, fieldnames=columns)
    print(type(mappings))
    writer.writeheader()
    for k in mappings.keys():
      writer.writerow({'Department/Major': major, 'Catalog As Of': date, 'From': from_college,
      'To': to_college, 'Transfer Course': k, 'Destination Course': mappings[k]})

    # Sample row format
    # 'Department/Major': major, 'Catalog As Of': date, 'From': from_college, 'To': to_college, 'Transfer Course':, 'Destination Course']

if __name__ == "__main__":
  parseText(sys.argv[1])

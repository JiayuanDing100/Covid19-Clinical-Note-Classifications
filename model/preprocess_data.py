import csv
import random
import pandas as pd
import xlrd

attris = ['Patientid', 'offset', 'sex', 'age', 'finding', 'clinical notes', 'other notes', 'survival', 'view', \
                       'modality', 'date', 'location', 'filename', 'doi', ' url', 'license'
                       ]

def get_row_lst(row):
   res = []
   for item in attris:
      res.append(row[item])
   return res


def deduplicate_and_write():
   with open('../data/filtered_metadata.csv', mode='w') as filtered_file:
      filtered_metatada = csv.writer(filtered_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
      first_title_line = attris
      filtered_metatada.writerow(first_title_line)

      num_cov = 0
      num_none_cov = 0
      deduplicate_lst = []
      with open('../data/metadata.csv', newline='') as csvfile:
         reader = csv.DictReader(csvfile)
         for row in reader:

            if row["finding"] == "COVID-19":
               row["finding"] = "Yes"
               # print(len(row["clinical notes"]), "||" + row["survival"] + "||" + row["clinical notes"])
               if len(row["clinical notes"]) == 0:
                  continue

               if row["clinical notes"].strip() not in deduplicate_lst:
                  num_cov += 1
                  deduplicate_lst.append(row["clinical notes"].strip())
                  filtered_metatada.writerow(get_row_lst(row))
                  #print(get_row_lst(row))
            else:
               row["finding"] = "No"

               if len(row["clinical notes"]) == 0:
                  continue
               if row["clinical notes"].strip() not in deduplicate_lst:
                  num_none_cov += 1
                  deduplicate_lst.append(row["clinical notes"].strip())
                  filtered_metatada.writerow(get_row_lst(row))
                  #print(get_row_lst(row))

      print("number of non-covid-19", num_none_cov)  # 37 non covid-19 samples

      """
      extra_0_label_cases = xlrd.open_workbook('../data/extra_0label_cases.xlsx')
      sheet = extra_0_label_cases.sheet_by_index(0)
      print(sheet)
      print(sheet.ncols)
      print(sheet.nrows)
      for i in range(sheet.nrows):
         if i == 0:
            continue
         if sheet.cell_value(i, 5).replace("\n", '').strip() not in deduplicate_lst:
            deduplicate_lst.append(sheet.cell_value(i, 5).replace("\n", '').strip())
            num_none_cov += 1
            print(sheet.cell_value(i, 5).strip())
            filtered_metatada.writerow([None, None, None, None, "No",\
                                        sheet.cell_value(i, 5).replace("\n", '').strip(), \
                                        None, None, None, None, None, None, None, None, None, None])
      """
   print("after deduplication, total number:", len(deduplicate_lst))
   print("number of covid-19:", num_cov)
   print("number of non-covid-19", num_none_cov)




def get_yes_no_sample_list():
   with open('../data/filtered_metadata.csv', newline='') as csvfile:
      reader = csv.DictReader(csvfile)

      num_none_cov = 0

      yes = []
      no = []
      for row in reader:
         if len(row["clinical notes"].split()) >= 128:  # max: 252
            print(len(row["clinical notes"].split()))

         if row["finding"] == "No":
            num_none_cov += 1
            no.append(row["clinical notes"].strip())
         else:
            yes.append(row["clinical notes"].strip())

   print(num_none_cov)

   print("yes:", len(yes))
   print("no:", len(no))
   return (yes, no)

def split_train_testnone_covid19_41(yes, no):

   training_dataset = {}
   test_dataset = {}
   yes_training = random.sample(yes, 72)
   yes_testing = list(set(yes).difference(set(yes_training)))

   training_dataset["yes"] = yes_training
   test_dataset["yes"] = yes_testing

   no = []
   with open('../data/non_covid_41samples.txt', 'r') as f:
      x = f.readlines()
      for line in x:

         no.append(line.strip('\n').strip())
   print(len(no))
   no_testing = random.sample(no[0:14], 6) + random.sample(no[14:], 9)
   no_training = list(set(no) - set(no_testing))
   print("no_training:", len(no_training))
   print("set training:", len(set(no_training)))
   print("set_testing:", len(set(no_testing)))
   print("no_testing:", len(no_testing))
   training_dataset["no"] = no_training
   test_dataset["no"] = no_testing

   print(len(training_dataset["yes"]), len(test_dataset["yes"]), len(training_dataset["no"]), len(test_dataset["no"]))
   return training_dataset, test_dataset


def split_train_test_none_covid19_70(yes, no):

   training_dataset = {}
   test_dataset = {}
   training_dataset["no"] = []
   test_dataset["no"] = []

   yes_training = random.sample(yes, 72)
   yes_testing = list(set(yes).difference(set(yes_training)))

   training_dataset["yes"] = yes_training
   test_dataset["yes"] = yes_testing

   no = []
   with open('../data/non_covid_70samples.txt', 'r') as f:
      x = f.readlines()
      for line in x:

         no.append(line.strip('\n').strip())
   print(len(no))

   no_test_index = random.sample(range(0, len(no)), 14)
   print(no_test_index)
   for i in range(len(no)):
      if i in no_test_index:
         test_dataset["no"].append(no[i])
      else:
         training_dataset["no"].append(no[i])

   print(len(training_dataset["yes"]), len(test_dataset["yes"]), len(training_dataset["no"]), len(test_dataset["no"]))
   return training_dataset, test_dataset



def split_train_test(yes, no):
   training_dataset = {}
   test_dataset = {}
   yes_training = random.sample(yes, round(len(yes)*0.8))
   yes_testing = list(set(yes).difference(set(yes_training)))

   training_dataset["yes"] = yes_training
   test_dataset["yes"] = yes_testing

   no_training = random.sample(no, round(len(no)*0.6))
   no_testing = list(set(no).difference(set(no_training)))

   training_dataset["no"] = no_training
   test_dataset["no"] = no_testing

   print(len(training_dataset["yes"]), len(test_dataset["yes"]), len(training_dataset["no"]), len(test_dataset["no"]))
   return training_dataset, test_dataset


deduplicate_and_write()
yes, no = get_yes_no_sample_list()
training_dataset, test_dataset = split_train_test(yes, no)

with open('../data/train_before_shuffle.csv', mode='w') as filtered_file:
   filtered_metatada = csv.writer(filtered_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
   for line in training_dataset['yes']:
      filtered_metatada.writerow(["1", line])
   for line in training_dataset['no']:
      filtered_metatada.writerow(["0", line])

with open('../data/test_before_shuffle.csv', mode='w') as filtered_file:
   filtered_metatada = csv.writer(filtered_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
   for line in test_dataset['yes']:
      filtered_metatada.writerow(["1", line])
   for line in test_dataset['no']:
      filtered_metatada.writerow(["0", line])

# shuffle row data.......
import csv

"""
This file coverts the Zoo.csv to ZooRefined.csv. "Does it have legs?" has been expanded to 6 questions and "type" has been
expanded to 7 questions. The last question for tyep is "Other?". ALl feature values have been converted to binary.


Note: The code in this file might seem pretty noob-y with all the if statements but in my defence, I didn't have time
to think this through. Just coded it up.
"""

with open('ZooRefined.csv', 'w') as csv_out_file:
    writer = csv.writer(csv_out_file)

    writer.writerow(["Animal Name","Does it have hair?","Does it have feathers?","Does it lay eggs?","Does it produce milk?","Is it airborne?","Is it aquatic?","Is it a predator?","Is it toothed?","Does it have a backbone?","Does it breathe?","Is it venomous?","Does it have fins?","Does it have 0 legs?","Does it have 2 legs?", "Does it 4 legs?", "Does it have 5 legs?", "Does it have 6 legs?", "Does it have 8 legs?", "Does it have a tail?","Is it domestic?","catsize","Is it a Mammal?", "Is it a bird?", "Is it a reptile?", "Is it a fish", "Is it an Amphibian?","Is it an insect?"])

    with open('Zoo.csv', 'r') as csv_in_file:
        reader = csv.reader(csv_in_file)
        features = []
        for row in reader:
            if reader.line_num == 1:
                features = row
            else:
                for i, feature in enumerate(features):
                    if feature == "Does it have legs?":
                        if row[i] == '0':
                            row.insert(i, '1') 
                            row.insert(i + 1, '0') 
                            row.insert(i + 2, '0') 
                            row.insert(i + 3, '0') 
                            row.insert(i + 4, '0')
                        elif row[i] == '2':
                            row[i] = '0'
                            row.insert(i + 1, '1')
                            row.insert(i + 2, '0') 
                            row.insert(i + 3, '0') 
                            row.insert(i + 4, '0')
                            row.insert(i + 5, '0')
                        elif row[i] == '4':
                            row[i] = '0'
                            row.insert(i + 1, '0')
                            row.insert(i + 2, '1') 
                            row.insert(i + 3, '0') 
                            row.insert(i + 4, '0')
                            row.insert(i + 5, '0')
                        elif row[i] == '5':
                            row[i] = '0'
                            row.insert(i + 1, '0')
                            row.insert(i + 2, '0') 
                            row.insert(i + 3, '1') 
                            row.insert(i + 4, '0')
                            row.insert(i + 5, '0')
                        elif row[i] == '6':
                            row[i] = '0'
                            row.insert(i + 1, '0')
                            row.insert(i + 2, '0') 
                            row.insert(i + 3, '0') 
                            row.insert(i + 4, '1')
                            row.insert(i + 5, '0')
                        elif row[i] == '8':
                            row[i] = '0'
                            row.insert(i + 1, '0')
                            row.insert(i + 2, '0') 
                            row.insert(i + 3, '0') 
                            row.insert(i + 4, '0')
                            row.insert(i + 5, '1')
                        else:
                            print("Unknown value")

                    if feature == 'type':
                        index = i + 5
                        if row[index] == '1':
                            row.insert(index+1, '0')
                            row.insert(index+2, '0')
                            row.insert(index+3, '0')
                            row.insert(index+4, '0')
                            row.insert(index+5, '0')
                            row.insert(index+6, '0')
                        elif row[index] == '2':
                            row[index] = '0'
                            row.insert(index+1, '1')
                            row.insert(index+2, '0')
                            row.insert(index+3, '0')
                            row.insert(index+4, '0')
                            row.insert(index+5, '0')
                            row.insert(index+6, '0')
                        elif row[index] == '3':
                            row[index] = '0'
                            row.insert(index+1, '0')
                            row.insert(index+2, '1')
                            row.insert(index+3, '0')
                            row.insert(index+4, '0')
                            row.insert(index+5, '0')
                            row.insert(index+6, '0')
                        elif row[index] == '4':
                            row[index] = '0'
                            row.insert(index+1, '0')
                            row.insert(index+2, '0')
                            row.insert(index+3, '1')
                            row.insert(index+4, '0')
                            row.insert(index+5, '0')
                            row.insert(index+6, '0')
                        elif row[index] == '5':
                            row[index] = '0'
                            row.insert(index+1, '0')
                            row.insert(index+2, '0')
                            row.insert(index+3, '0')
                            row.insert(index+4, '1')
                            row.insert(index+5, '0')
                            row.insert(index+6, '0')
                        elif row[index] == '6':
                            row[index] = '0'
                            row.insert(index+1, '0')
                            row.insert(index+2, '0')
                            row.insert(index+3, '0')
                            row.insert(index+4, '0')
                            row.insert(index+5, '1')
                            row.insert(index+6, '0')
                        elif row[index] == '7':
                            row[index] = '0'
                            row.insert(index+1, '0')
                            row.insert(index+2, '0')
                            row.insert(index+3, '0')
                            row.insert(index+4, '0')
                            row.insert(index+5, '0')
                            row.insert(index+6, '1')
                        else:
                            print("problem" + row[index])

                writer.writerow(row)





                            

                



    

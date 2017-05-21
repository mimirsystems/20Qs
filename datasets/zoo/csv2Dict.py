import csv
def read_and_write_from_zoo(file_name):
    """
    Takes the name of the csv file which has the zoo dataset
    and writes the samples in the format of the database
    :param file_name: Name of the file which has the zoo dataset
    """
    with open(file_name, 'r') as csv_in_file:
        
        reader = csv.reader(csv_in_file)
        
        features = []
        
        for row in reader:
            #If not header, the answer for every feature is collected and stored inside a dict
            #Then, it's written inside a csv file
            if reader.line_num > 1:
                
                answer_dict = {}
                
                #For every entry in the zip of row and feature i.e [row[0], feature[0]], [row[1], feature[1]].....
                for val, feature in zip(row, features):
                    #Try so that when the val is the name of the animal, the loop just continues to the next
                    #column
                    try:
                        if int(val) == 0:
                            answer = "No"
                        else:
                            answer = "Yes"
                    
                    except ValueError:
                        continue

                    answer_dict[feature] = answer
                #All the questions and answers are added to the csv
                add_game(row[0], answer_dict)
            
            else:
                #The features are extracted from the header of the csv file
                features = row


                

                
def add_game(solution, answer_dict):
    """
    Takes in the solution and the dict containing all the questions and answers and writes them into a csv file
    :param solution: String representation of the name of the answer
    :param answer_dict: Dict with questions as keys and answers (Yes/No) as values
    """

    questions = answer_dict.keys()
    
    with open('ZooQAs.csv', 'a') as csv_out_file:
        
        writer = csv.writer(csv_out_file)
        
        for question in questions:
            row = [question, answer_dict[question], solution]
            writer.writerow(row)


read_and_write_from_zoo('ZooRefined.csv')


import os
import pandas as pd
import json
import traceback

def read_file(file):
       
    if file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    
    else:
        raise Exception(
            "unsupported file format only pdf and text file suppoted"
            )
    
def extract_mcqs(input_string):
    # Remove the introductory text and get the JSON part
    json_string = input_string.split('\n\n', 1)[1]
    
    # Initialize an empty dictionary to store the MCQs
    mcqs = {}
    
    # Split the string into individual MCQ blocks
    mcq_blocks = json_string.split('} ,\n\n')
    
    for block in mcq_blocks:
        
        try :

            # Extract the question number
            question_num = block.split(':')[0].strip('"{')
            
            # Extract the MCQ question
            mcq_start = block.find('"mcq": "') + 8
            mcq_end = block.find('", "options"')
            mcq_question = block[mcq_start:mcq_end]
            
            # Extract the options
            options_start = block.find('"options": {') + 11
            options_end = block.rfind('}, "correct"')
            options_string = block[options_start:options_end]
            
            options = {}
            option_pairs = options_string.split('", "')
            for pair in option_pairs:
                if '": "' in pair:
                    key, value = pair.split('": "', 1)
                    key = key.strip('"{}').strip()
                    value = value.strip('"')
                    options[key] = value
            
            # Extract the correct answer
            correct_start = block.rfind('"correct": "') + 12
            correct_end = block.rfind('"')
            correct_answer = block[correct_start:correct_end]
            
            # Store the extracted information in the dictionary
            mcqs[question_num] = {
                'question': mcq_question,
                'options': options,
                'correct_answer': correct_answer
            }
        
        
            return mcqs
    
        except:
             
             traceback.print_exception(type(e), e, e.__traceback__)
             
             return False
        
def create_mcq_dataframe(mcqs):
    flattened_data = []
    for num, mcq in mcqs.items():
        row = {
            'question_number': num,
            'question': mcq['question'],
            'correct_answer': mcq['correct_answer']
        }
        for option, text in mcq['options'].items():
            row[f'option_{option}'] = text
        flattened_data.append(row)
    
    return pd.DataFrame(flattened_data)

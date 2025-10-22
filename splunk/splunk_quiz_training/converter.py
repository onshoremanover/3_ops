import re
import json5

def parse_questions(input_text):
    input_text = input_text.strip()
    raw_questions = re.split(r'\n(?=Q: )', input_text)
    questions = []

    for raw_question in raw_questions:
        parts = raw_question.split('\n')
        question = parts[0][3:]  # Remove 'Q: ' from the beginning
        choices = parts[1:5]
        answer = re.search(r'Answer\s*:\s*(\w)', raw_question).group(1)
        reference_match = re.search(r'Reference:(https?://[^\s]+)', raw_question)

        question_data = {
            'question': question,
            'answer': answer,
            'choices': choices
        }

        if reference_match:
            question_data['explanation'] = reference_match.group(1)

        questions.append(question_data)

    return questions

def read_input_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_output_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(data)

# Path to the input file
input_file_path = 'input.csv'

# Path to the output file
output_file_path = 'output.json5'

# Read the input text from the file
input_text = read_input_file(input_file_path)

# Parse the input text into questions
questions = parse_questions(input_text)

# Convert the questions to JSON5 format
json5_data = json5.dumps(questions, indent=4)

# Write the JSON5 formatted string to the output file
write_output_file(output_file_path, json5_data)

print(f"Data has been written to {output_file_path}")

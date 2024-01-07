import openai
import csv
import pandas as pd

# Set your OpenAI API key
openai.api_key = "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"

# Function to extract information from OpenAI response
# def extract_info_response(extracted_info):
#     Extract information logic here (as per your original code)

# Read business ideas from CSV file
# Read business ideas from CSV file
def read_ideas_from_csv(csv_file):
    ideas_list = []
    with open(csv_file, 'r', encoding='latin1') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            ideas_list.append({'problem': row['problem'], 'solution': row['solution']})
    return ideas_list


# Main script
if __name__ == "__main__":
    # CSV file containing business ideas
    #csv_file_path = 'business_ideas.csv'
    csv_file_path = "D:\\AI EarthHack\\AI EarthHack Dataset.csv"
    # Read business ideas from CSV
    ideas_list = read_ideas_from_csv(csv_file_path)

    # Process only the first 10 rows
    ideas_list = ideas_list[:10]

    # Generate prompt for evaluating and sorting ideas
    prompt = f"""
    ⚠️ CRITICAL INSTRUCTIONS
    Summary: Evaluate the provided business ideas and pitches. Sort these pitches, highlight key insights, or flag potential spam.

    FORMAT: Provide a structured summary for each idea, including any noteworthy insights. If an idea seems irrelevant or suspicious (spam), clearly indicate it.

    IDEA EVALUATION:
    """

    # Add individual idea details to the prompt
    for index, idea in enumerate(ideas_list, start=1):
        prompt += f"""
        Idea {index}:
        - Problem: {idea['problem']}
        - Solution: {idea['solution']}
        ---
        """

    # Add closing statement
    prompt += """
    SORTING AND FLAGGING:
    - Sort the ideas based on relevance or potential.
    - Highlight key insights or unique aspects in each idea.
    - If an idea seems like spam or is not relevant, explicitly flag it.
    """

    # Use the OpenAI GPT-3.5 Turbo model to generate a response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1  # Adjust temperature as needed
    )

    # Extract and display the response
    extracted_info = response.choices[0].message["content"]
    print(extracted_info)

    # Save the output along with the problem and solution to a new CSV file
    output_csv_path = 'output_evaluated_ideas.csv'
    with open(output_csv_path, 'w', newline='') as output_file:
        fieldnames = ['Problem', 'Solution', 'Evaluated Idea']
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)

        writer.writeheader()
        for index, idea in enumerate(ideas_list):
            writer.writerow({'Problem': idea['problem'], 'Solution': idea['solution'], 'Evaluated Idea': extracted_info})

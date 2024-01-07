import csv
import spacy

# Load the spaCy English model
#nlp = spacy.load("en_core_web_sm")
nlp = spacy.load("en_core_web_md")

# Define the scoring function
def calculate_scores(idea):
    # Environmental Impact Score (EIS)
    eis = (0.3 * idea['Waste Reduction']) + (0.3 * idea['Resource Conservation']) + (0.4 * idea['Pollution Reduction'])

    # Financial Viability Score (FVS)
    fvs = (0.25 * idea['Cost Savings']) + (0.25 * idea['Revenue Streams']) + (0.5 * idea['Economic Feasibility'])

    # Feasibility and Scalability Score (FSS)
    fss = (0.2 * idea['Implementation Ease']) + (0.8 * idea['Scalability'])

    # Innovation and Novelty Score (INS)
    ins = (0.15 * idea['Uniqueness']) + (0.85 * idea['New Perspective'])

    # Social Impact Score (SIS)
    sis = (0.1 * idea['Job Creation']) + (0.9 * idea['Community Involvement'])

    # Overall Idea Score
    overall_score = (0.3 * eis) + (0.25 * fvs) + (0.2 * fss) + (0.15 * ins) + (0.1 * sis)

    # Update the idea dictionary with scores
    idea['EIS'] = eis
    idea['FVS'] = fvs
    idea['FSS'] = fss
    idea['INS'] = ins
    idea['SIS'] = sis
    idea['Overall Score'] = overall_score

    return idea

# Define keywords or phrases associated with each feature
feature_keywords = {
    'Waste Reduction': ['modular construction', 'recycling', 'reuse', 'circular economy'],
    'Resource Conservation': ['modular construction', 'recycling', 'reuse', 'circular economy'],
    'Pollution Reduction': ['modular construction', 'green energy', 'clean energy', 'wind energy'],
    'Cost Savings': ['cost savings', 'financial efficiency', 'economic feasibility'],
    'Revenue Streams': ['revenue streams', 'financial efficiency', 'economic feasibility'],
    'Economic Feasibility': ['cost savings', 'financial efficiency', 'economic feasibility'],
    'Implementation Ease': ['modular construction', 'ease of implementation', 'simplicity'],
    'Scalability': ['modular construction', 'scalability', 'global implementation'],
    'Uniqueness': ['innovative approach', 'new perspective', 'novel concept'],
    'New Perspective': ['innovative approach', 'new perspective', 'novel concept'],
    'Job Creation': ['job creation', 'employment opportunities'],
    'Community Involvement': ['community involvement', 'social impact', 'community engagement']
}

# Read data from CSV file
ideas_list = []
with open("D:\\AI EarthHack\\AI EarthHack Dataset.csv", 'r', encoding='latin1') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')  # or use the correct delimiter in your CSV file
    for row in reader:
        idea = {
            'id': int(row['id']),
            'problem': row['problem'],
            'solution': row['solution'],
            'Waste Reduction': 0,
            'Resource Conservation': 0,
            'Pollution Reduction': 0,
            'Cost Savings': 0,
            'Revenue Streams': 0,
            'Economic Feasibility': 0,
            'Implementation Ease': 0,
            'Scalability': 0,
            'Uniqueness': 0,
            'New Perspective': 0,
            'Job Creation': 0,
            'Community Involvement': 0,
        }

        # Process the problem and solution paragraphs with spaCy
        problem_doc = nlp(idea['problem'])
        solution_doc = nlp(idea['solution'])

        # Iterate over each feature and find the best matching keyword or phrase
        for feature, keywords in feature_keywords.items():
            max_similarity = 0

            # Calculate similarity for each keyword
            for keyword in keywords:
                similarity_problem = problem_doc.similarity(nlp(keyword))
                similarity_solution = solution_doc.similarity(nlp(keyword))
                avg_similarity = (similarity_problem + similarity_solution) / 2

                # Update max_similarity if a better match is found
                if avg_similarity > max_similarity:
                    max_similarity = avg_similarity

            # Update the feature value with the maximum similarity
            idea[feature] = max_similarity

        ideas_list.append(idea)

# Calculate scores for each idea
ideas_scores = [calculate_scores(idea) for idea in ideas_list]

# Print the ideas_scores list containing scores for each idea
for idea in ideas_scores:
    print(idea)

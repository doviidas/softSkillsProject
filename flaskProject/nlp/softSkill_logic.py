import spacy
import pandas as pd
from rapidfuzz import fuzz, process

# Load the spaCy model
nlp = spacy.load("en_core_web_md")

# Load the dataset
dataset_path = 'C:/SoftSkillsProject/softSkillDataset/softSkillsDataset.csv'
dataset = pd.read_csv(dataset_path)

def calculate_similarity(user_activity, dataset_activity):
    user_doc = nlp(user_activity)
    dataset_doc = nlp(dataset_activity)
    return user_doc.similarity(dataset_doc)

def fuzzy_semantic_matching(user_activities, dataset_activities, threshold=0.75):  # Lower the threshold a bit if needed
    matches = []
    for user_activity in user_activities:
        user_tokens = set(get_activity_tokens(user_activity))
        best_match = None
        best_score = 0
        for dataset_activity in dataset_activities:
            dataset_tokens = set(get_activity_tokens(dataset_activity))
            # Calculate semantic similarity
            semantic_similarity = calculate_similarity(' '.join(user_tokens), ' '.join(dataset_tokens))
            if semantic_similarity > best_score and semantic_similarity > threshold:
                best_match = dataset_activity
                best_score = semantic_similarity
        if best_match:
            matches.append(best_match)
    return matches

def get_activity_tokens(activity):
    """Tokenize and lemmatize the activity using spaCy for semantic comparison."""
    doc = nlp(activity.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return tokens

def extract_soft_skills(matching_activities):
    soft_skills = []
    for activity in matching_activities:
        skills_list = dataset[dataset['Activity'].str.lower().str.contains(activity)]['Soft Skills'].values
        for skills in skills_list:
            soft_skills.extend(skills.split('; '))
    return list(set(soft_skills))  # Ensure uniqueness

def nlp_process(text):
    user_activities = [text]  # Considering the whole input text as a potential activity
    dataset_activities = dataset['Activity'].str.lower().tolist()
    matching_activities = fuzzy_semantic_matching(user_activities, dataset_activities)
    if not matching_activities:
        print("No matching activities found.")
        return []
    soft_skills = extract_soft_skills(matching_activities)
    return soft_skills

# Example usage
text_input = "I play football"
soft_skills = nlp_process(text_input)
print("Extracted Skills:", soft_skills)

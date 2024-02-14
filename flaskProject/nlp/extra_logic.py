import pandas as pd

# Load datasets
activities_df = pd.read_csv('C:/SoftSkillsProject/softSkillDataset/activities_dataset.csv')
roles_df = pd.read_csv('C:/SoftSkillsProject/softSkillDataset/roles_dataset.csv')

def extract_role_and_activity(input_text):
    # Normalize input text
    input_text_lower = input_text.lower()

    # Initialize
    found_role = None
    found_activity = None

    # Check each role and its synonyms for a match
    for _, row in roles_df.iterrows():
        role_synonyms = [row['Role'].lower()] + [syn.lower() for syn in row['Synonyms'].split(';')]
        for synonym in role_synonyms:
            if synonym in input_text_lower:
                found_role = row['Role']
                break
        if found_role:
            break

    # Check for activity in input text
    for _, row in activities_df.iterrows():
        if row['Activity'].lower() in input_text_lower:
            found_activity = row['Activity']
            break

    return found_role, found_activity


def get_combined_soft_skills(role, activity):
    soft_skills = set()

    # If a role is found, add its soft skills
    if role:
        role_skills = roles_df[roles_df['Role'].str.lower() == role.lower()]['Soft Skills'].values
        if role_skills.size > 0:
            soft_skills.update(role_skills[0].split('; '))

    # If an activity is found, add its soft skills
    if activity:
        activity_skills = activities_df[activities_df['Activity'].str.lower() == activity.lower()]['Soft Skills'].values
        if activity_skills.size > 0:
            soft_skills.update(activity_skills[0].split('; '))

    return list(soft_skills)

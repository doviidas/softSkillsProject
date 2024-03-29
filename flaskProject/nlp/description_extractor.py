import pandas as pd

# Load the CSV file containing soft skills and descriptions
descriptions_csv = 'C:/SoftSkillsProject/softSkillDataset/softSkillsDescription.csv'
soft_skills_df = pd.read_csv(descriptions_csv)

def extract_soft_skills_with_descriptions(extracted_soft_skills):
    # Make sure the input is a list of skill names
    assert isinstance(extracted_soft_skills, list), "Expected a list of skills"
    assert all(isinstance(skill, str) for skill in extracted_soft_skills), "Expected a list of strings"

    soft_skills_with_descriptions = []
    print("Extracting soft skills with descriptions...")
    for skill in extracted_soft_skills:
        print(f"Processing skill: {skill}")
        # Check if the skill is in the DataFrame
        description_rows = soft_skills_df[soft_skills_df['Soft Skills'].str.lower() == skill.lower()]
        if not description_rows.empty:
            description = description_rows['Descriptions'].iloc[0]
            soft_skills_with_descriptions.append({'skill': skill, 'description': description})
            # Print the description for debugging
            print(f"Description found for skill '{skill}': {description}")
        else:
            print(f"Warning: Description for skill '{skill}' not found in CSV")
    return soft_skills_with_descriptions

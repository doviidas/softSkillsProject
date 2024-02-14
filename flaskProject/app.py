from flask import Flask, request, jsonify
from flask_cors import CORS
#from nlp.softSkill_logic import nlp_process
from nlp.description_extractor import extract_soft_skills_with_descriptions, soft_skills_df
from nlp.extra_logic import extract_role_and_activity, get_combined_soft_skills, roles_df, activities_df

app = Flask(__name__)
CORS(app)
# @app.route('/extract_skills', methods=['POST'])
# def handle_extract_skills():
#     data = request.json
#     text = data['text']
#
#     # Use the nlp_process function to get the skills from the text
#     extracted_skills = nlp_process(text)
#
#     # Use the extract_soft_skills_with_descriptions function to get descriptions for these skills
#     skills_with_descriptions = extract_soft_skills_with_descriptions(extracted_skills)
#
#     # Format the response as JSON
#     response_data = {
#         'nlp_skills': extracted_skills,  # This is the list of skills
#         'soft_skills_with_descriptions': skills_with_descriptions  # This is the list with descriptions
#     }
#     return jsonify(response_data)

@app.route('/extract_skills', methods=['POST'])
def handle_extract_skills():
    data = request.json
    text = data.get('text', '')

    # Use extract_role_and_activity function to get the role and activity from the text
    role, activity = extract_role_and_activity(text)

    # Initialize empty lists to hold skills
    role_skills_list = []
    activity_skills_list = []

    # Only proceed if role is not None
    if role:
        role_skills = roles_df[roles_df['Role'].str.lower() == role.lower()]['Soft Skills'].values
        if role_skills.size > 0:
            role_skills_list = role_skills[0].split('; ')

    # Only proceed if activity is not None
    if activity:
        activity_skills = activities_df[activities_df['Activity'].str.lower() == activity.lower()]['Soft Skills'].values
        if activity_skills.size > 0:
            activity_skills_list = activity_skills[0].split('; ')

    # Combine the skills from role and activity, ensuring no duplicates
    combined_soft_skills = list(set(role_skills_list + activity_skills_list))

    # Format and return the response as JSON
    response_data = {
        'text': text,
        'extracted_role': role,
        'extracted_activity': activity,
        'activity_skills': activity_skills_list,
        'role_skills': role_skills_list,
        'combined_soft_skills': combined_soft_skills
    }
    return jsonify(response_data)


@app.route('/get_skill_description', methods=['GET'])
def get_skill_description():
    skill = request.args.get('skill')
    if not skill:
        return jsonify({'error': 'Missing skill parameter'}), 400

    # Use the function to get the description
    skill_description = extract_soft_skills_with_descriptions([skill])

    if skill_description:
        # Assuming the function always returns a list, get the first item's description
        return jsonify({'description': skill_description[0]['description']})
    else:
        return jsonify({'error': 'Description not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)

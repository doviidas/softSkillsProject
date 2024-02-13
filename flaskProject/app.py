from flask import Flask, request, jsonify
from flask_cors import CORS
from nlp.softSkill_logic import nlp_process
from nlp.description_extractor import extract_soft_skills_with_descriptions, soft_skills_df

app = Flask(__name__)
CORS(app)


@app.route('/extract_skills', methods=['POST'])
def handle_extract_skills():
    data = request.json
    text = data['text']

    # Use the nlp_process function to get the skills from the text
    extracted_skills = nlp_process(text)

    # Use the extract_soft_skills_with_descriptions function to get descriptions for these skills
    skills_with_descriptions = extract_soft_skills_with_descriptions(extracted_skills)

    # Format the response as JSON
    response_data = {
        'nlp_skills': extracted_skills,  # This is the list of skills
        'soft_skills_with_descriptions': skills_with_descriptions  # This is the list with descriptions
    }
    return jsonify(response_data)


@app.route('/get_skill_description', methods=['GET'])
def get_skill_description():
    skill = request.args.get('skill')
    if not skill:
        return jsonify({'error': 'Missing skill parameter'}), 400

    description = soft_skills_df.loc[soft_skills_df['Soft Skills'].str.lower() == skill.lower(), 'Descriptions'].values
    if description.size > 0:
        return jsonify({'description': description[0]})
    else:
        return jsonify({'error': 'Description not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)

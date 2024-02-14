# import spacy
# import pandas as pd
# from rapidfuzz import fuzz, process
#
# # Load the spaCy model
# nlp = spacy.load("en_core_web_md")
#
# # Load the dataset
# dataset_path = 'C:/SoftSkillsProject/softSkillDataset/softSkillsDataset.csv'
# dataset = pd.read_csv(dataset_path)
#
# def calculate_similarity(user_activity, dataset_activity):
#     user_doc = nlp(user_activity)
#     dataset_doc = nlp(dataset_activity)
#     return user_doc.similarity(dataset_doc)
#
#
# def preprocess_activity_for_matching(activity):
#     """Preprocess activity focusing on key nouns and verbs for matching."""
#     doc = nlp(activity.lower())
#     # Focus on lemmatized nouns and verbs, which are more likely to be relevant for activity matching
#     tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and (token.pos_ == "NOUN" or token.pos_ == "VERB")]
#     return ' '.join(tokens)
#
#
# import logging
#
# # Setup basic logging
# logging.basicConfig(level=logging.INFO)
#
# import logging
#
# # Setup basic logging
# logging.basicConfig(level=logging.INFO)
#
#
# def fuzzy_semantic_matching_improved(user_activities, dataset_activities, semantic_threshold=0.5, fuzzy_threshold=70):
#     matches = []
#     for user_activity in user_activities:
#         best_match = None
#         best_score = 0
#         best_similarity = 0
#
#         preprocessed_user_activity = preprocess_activity_for_matching(user_activity)
#         logging.info(f"Preprocessed user activity: '{preprocessed_user_activity}'")
#
#         fuzzy_matches = process.extract(preprocessed_user_activity, dataset_activities, scorer=fuzz.WRatio, score_cutoff=fuzzy_threshold)
#         logging.info(f"Fuzzy matches found: {len(fuzzy_matches)}")
#
#         for fuzzy_match in fuzzy_matches:
#             dataset_activity, fuzzy_score = fuzzy_match[0], fuzzy_match[1]
#             preprocessed_dataset_activity = preprocess_activity_for_matching(dataset_activity)
#             semantic_similarity = calculate_similarity(preprocessed_user_activity, preprocessed_dataset_activity)
#             logging.info(f"Checking '{dataset_activity}' with fuzzy score: {fuzzy_score}, semantic similarity: {semantic_similarity * 100:.2f}%")
#
#             if semantic_similarity > best_score:
#                 best_match = dataset_activity
#                 best_score = semantic_similarity
#                 best_similarity = semantic_similarity
#
#         if best_match:
#             matches.append(best_match)
#             logging.info(f"Best match: '{best_match}' with semantic similarity: {best_similarity * 100:.2f}%")
#         else:
#             logging.info("No match found for user activity.")
#     return matches
#
#
#
# def get_activity_tokens(activity):
#     """Tokenize and lemmatize the activity using spaCy for semantic comparison."""
#     doc = nlp(activity.lower())
#     tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
#     return tokens
#
# def extract_soft_skills(matching_activities):
#     soft_skills = []
#     for activity in matching_activities:
#         skills_list = dataset[dataset['Activity'].str.lower().str.contains(activity)]['Soft Skills'].values
#         for skills in skills_list:
#             soft_skills.extend(skills.split('; '))
#     return list(set(soft_skills))  # Ensure uniqueness
#
# def nlp_process(text):
#     user_activities = [text]  # Considering the whole input text as a potential activity
#     dataset_activities = dataset['Activity'].str.lower().tolist()
#     # Update this line to call the correct function name
#     matching_activities = fuzzy_semantic_matching_improved(user_activities, dataset_activities)
#     if not matching_activities:
#         print("No matching activities found.")
#         return []
#     soft_skills = extract_soft_skills(matching_activities)
#     return soft_skills
#
#
# # Adjusted example usage with the improved matching logic
# text_input = "I love to play football"
# soft_skills = nlp_process(text_input)
# print("Extracted Skills:", soft_skills)

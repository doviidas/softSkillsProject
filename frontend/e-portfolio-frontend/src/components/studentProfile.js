import React, { useState } from 'react';
import '../App.css'; // Ensure this path is correct

function ScenarioInput() {
    const [scenario, setScenario] = useState('');
    const [extractedActivity, setExtractedActivity] = useState('');
    const [extractedRole, setExtractedRole] = useState('');
    const [activitySkills, setActivitySkills] = useState([]);
    const [roleSkills, setRoleSkills] = useState([]);
    const [skillDescriptions, setSkillDescriptions] = useState({});
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleScenarioChange = (e) => {
        setScenario(e.target.value);
    };

    const fetchSkillDescription = async (skill) => {
        try {
            const url = `http://localhost:5000/get_skill_description?skill=${encodeURIComponent(skill)}`;
            const response = await fetch(url);

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log("Fetched description for skill", skill, ":", data.description); // Log the fetched description
            
            setSkillDescriptions(prevDescriptions => ({
                ...prevDescriptions,
                [skill]: {
                    description: data.description || 'Description not available',
                    visible: !prevDescriptions[skill]?.visible // Toggle visibility
                }
            }));
        } catch (error) {
            console.error('Error fetching skill description:', error);
            setError(`Error fetching skill description: ${error.message}`);
        }
    };
    
    const extractSkills = async () => {
        setLoading(true);
        setError('');
        
        try {
            const response = await fetch('http://localhost:5000/extract_skills', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: scenario }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            setExtractedActivity(data.extracted_activity || '');
            setExtractedRole(data.extracted_role || '');
            setActivitySkills(data.activity_skills || []);
            setRoleSkills(data.role_skills || []);
        } catch (error) {
            console.error('Error fetching data:', error);
            setError(`Error fetching data: ${error.message}`);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="scenario-input-container">
            <h2>Discover Your Soft Skills</h2>
            <input
                type="text"
                className="scenario-text-input"
                value={scenario}
                onChange={handleScenarioChange}
                placeholder="Describe a scenario where you demonstrated your abilities..."
            />
            <br />
            <button className="extract-button" onClick={extractSkills} disabled={loading}>
                {loading ? 'Analyzing...' : 'Analyze Scenario'}
            </button>
            {error && <div className="error-message">{error}</div>}
            <div className="skills-output-container">
                {extractedActivity && activitySkills.length > 0 && (
                    <div className="skills-section">
                        <h3>Based on your activity "{extractedActivity}", you may have these skills:</h3>
                        <ul className="skills-list">
                            {activitySkills.map((skill, index) => (
                                <li key={`activity-skill-${index}`} className="skill-item">
                                    <div className="skill-content">
                                        <span>{skill}</span>
                                        <button className="toggle-description-button" onClick={() => fetchSkillDescription(skill)}>
                                            {skillDescriptions[skill]?.visible ? 'Show Less' : 'Show More'}
                                        </button>
                                    </div>
                                    {skillDescriptions[skill]?.visible && (
                                        <div className="skill-description">{skillDescriptions[skill].description}</div>
                                    )}
                                </li>
                            ))}
                        </ul>
                    </div>
                )}
                {extractedRole && roleSkills.length > 0 && (
                    <div className="skills-section">
                        <h3>As a "{extractedRole}", these skills could also be relevant:</h3>
                        <ul className="skills-list">
                            {roleSkills.map((skill, index) => (
                                <li key={`role-skill-${index}`} className="skill-item">
                                    <div className="skill-content">
                                        <span>{skill}</span>
                                        <button className="toggle-description-button" onClick={() => fetchSkillDescription(skill)}>
                                            {skillDescriptions[skill]?.visible ? 'Show Less' : 'Show More'}
                                        </button>
                                    </div>
                                    {skillDescriptions[skill]?.visible && (
                                        <div className="skill-description">{skillDescriptions[skill].description}</div>
                                    )}
                                </li>
                            ))}
                        </ul>
                    </div>
                )}
            </div>
        </div>
    );
}

export default ScenarioInput;

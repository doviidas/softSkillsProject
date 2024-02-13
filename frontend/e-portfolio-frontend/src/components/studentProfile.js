import React, { useState } from 'react';
import '../App.css'; // Ensure this path is correct

function ScenarioInput() {
    const [scenario, setScenario] = useState('');
    const [extractedSkills, setExtractedSkills] = useState([]);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleScenarioChange = (e) => {
        setScenario(e.target.value);
    };

    const extractSkills = async () => {
        setLoading(true);
        setError(''); // Clear previous errors
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
            if (data.soft_skills_with_descriptions) {
                // Map through the skills to add a 'visible' property for toggling description visibility
                const skillsWithVisibility = data.soft_skills_with_descriptions.map(skill => ({
                    ...skill,
                    visible: false,
                }));
                setExtractedSkills(skillsWithVisibility);
            } else {
                setExtractedSkills([]); // Clear skills if none are received
            }
        } catch (error) {
            console.error('Error fetching data:', error);
            setError(`Error fetching data: ${error.message}`);
        } finally {
            setLoading(false);
        }
    };

    const toggleDescriptionVisibility = (index) => {
        // Toggle the 'visible' property of the skill at the given index
        const updatedSkills = extractedSkills.map((skill, i) => {
            if (i === index) {
                return { ...skill, visible: !skill.visible };
            }
            return skill;
        });
        setExtractedSkills(updatedSkills);
    };

    return (
        <div className="scenario-input-container">
            <h2>Extract Soft Skills from Scenarios</h2>
            <textarea
                className="scenario-textarea"
                value={scenario}
                onChange={handleScenarioChange}
                placeholder="Enter a scenario..."
            />
            <br />
            <button className="extract-button" onClick={extractSkills} disabled={loading}>
                {loading ? 'Extracting...' : 'Extract Skills'}
            </button>

            {error && <div className="error-message">{error}</div>}

            {extractedSkills.length > 0 && (
                <div className="skills-container">
                    <h3>Extracted Skills:</h3>
                    <ul>
                        {extractedSkills.map((skillItem, index) => (
                            <li key={index}>
                                <strong>{skillItem.skill}:</strong>
                                <button onClick={() => toggleDescriptionVisibility(index)}>
                                    {skillItem.visible ? 'Hide Description' : 'Show Description'}
                                </button>
                                {skillItem.visible && <p>{skillItem.description || 'No description available'}</p>}
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}

export default ScenarioInput;

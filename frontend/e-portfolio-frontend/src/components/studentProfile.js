import React, { useState } from 'react';

function CreateStudentProfile() {
    const [studentProfile, setStudentProfile] = useState({
        name: '',
        email: '',
        // other fields as necessary
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setStudentProfile(prevState => ({
            ...prevState,
            [name]: value
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        fetch('http://localhost:8080/api/student', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(studentProfile),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            // Handle success
        })
        .catch((error) => {
            console.error('Error:', error);
            // Handle error
        });
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                name="name"
                value={studentProfile.name}
                onChange={handleChange}
                placeholder="Name"
            />
            <input
                type="email"
                name="email"
                value={studentProfile.email}
                onChange={handleChange}
                placeholder="Email"
            />
            {/* Other input fields */}
            <button type="submit">Create Profile</button>
        </form>
    );
}

export default CreateStudentProfile;

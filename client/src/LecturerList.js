import React, {useEffect, useState} from 'react';

const LecturerList = () => {
    const [lecturers, setLecturers] = useState([]);

    useEffect(() => {
        // Fetch data from Flask API when the component mounts
        fetch('/api/lecturers')
            .then(response => response.json())
            .then(data => {
                console.log('Fetched Data:', data); // Print the fetched data to the console
                setLecturers(data);
            })
            .catch(error => console.error('Error fetching data:', error));
    }, []);

    return (
        <div>
            <h2>List of Lecturers</h2>
            <ul>
                {lecturers.map(lecturer => (
                    <li key={lecturer.uuid}>
                        <h3>{lecturer.first_name} {lecturer.last_name}</h3>
                        <p>Title: {lecturer.title_before} {lecturer.title_after}</p>
                        {/* Add more details as needed */}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default LecturerList;

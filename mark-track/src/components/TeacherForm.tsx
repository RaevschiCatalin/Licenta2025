'use client';

import { useState, useEffect } from 'react';
import {getRequest, postRequest} from '@/context/api';
import { useRouter } from 'next/navigation';

interface Subject {
    id: string;
    name: string;
}

export default function TeacherForm() {
    const uid: string = localStorage.getItem('uid') || '';
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [fatherName, setFatherName] = useState('');
    const [govId, setGovId] = useState('');
    const [subjects, setSubjects] = useState<Subject[]>([]);
    const [selectedSubject, setSelectedSubject] = useState<string | null>("");
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');
    const router = useRouter();

    useEffect(() => {
        const fetchSubjects = async () => {
            try {
                const data = await getRequest('/subjects/get-subjects');

                if (data && Array.isArray(data.subjects)) {
                    setSubjects(data.subjects);
                } else {
                    setError('Unexpected data format received.');
                }
            } catch {
                setError('Failed to load subjects.');
            }
        };
        fetchSubjects();
    }, []);

    const handleSubmit = async () => {
        if (!selectedSubject) {
            setError('Please select a subject.');
            return;
        }
        if (!firstName || !lastName || !fatherName || !govId) {
            setError('All fields are required.');
            return;
        }

        try {
            const payload = {
                first_name: firstName,
                last_name: lastName,
                father_name: fatherName,
                gov_number: govId,
                subject_id: selectedSubject,
                uid: uid
            };
            console.log(payload)
            await postRequest('/profiles/complete-teacher-details', payload);
            setMessage('Teacher details submitted successfully!');
            setTimeout(()=>{
                router.push("/login");
            },2000);
        } catch  {
            setError('Failed to submit teacher details.');
        }
    };

    return (
        <div className="form-group">
            <h2 className="text-xl pt-16 font-semibold">Teacher Details</h2>
            <div className="form-field">
                <label>First Name</label>
                <input
                    type="text"
                    placeholder="Enter first name"
                    className="input input-block"
                    value={firstName}
                    onChange={(e) => setFirstName(e.target.value)}
                />
            </div>
            <div className="form-field">
                <label>Last Name</label>
                <input
                    type="text"
                    placeholder="Enter last name"
                    className="input input-block"
                    value={lastName}
                    onChange={(e) => setLastName(e.target.value)}
                />
            </div>
            <div className="form-field">
                <label>Father&apos;s Name</label>
                <input
                    type="text"
                    placeholder="Enter father's name"
                    className="input input-block"
                    value={fatherName}
                    onChange={(e) => setFatherName(e.target.value)}
                />
            </div>
            <div className="form-field">
                <label>Government ID</label>
                <input
                    type="number"
                    placeholder="Enter government ID"
                    className="input input-block"
                    value={govId}
                    onChange={(e) => setGovId(e.target.value.toString())}
                />
            </div>
            <div className="form-field">
                <label>Subject</label>
                <select

                    value={selectedSubject || ""}
                    onChange={(e) => setSelectedSubject(e.target.value)}
                    className="input input-block"
                >
                    <option value="">Select a subject</option>
                    {subjects.map((subject) => (
                        <option key={subject.id} value={subject.id}>
                            {subject.name}
                        </option>
                    ))}
                </select>
            </div>
            <button className="btn btn-primary w-full mt-4" onClick={handleSubmit}>
                Submit
            </button>
            {error && <p className="text-red-500 text-sm mt-2">{error}</p>}
            {message && <p className="text-green-500 text-sm mt-2">{message}</p>}
        </div>
    );
}

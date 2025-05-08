'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { getRequest, postRequest } from '@/context/api';
import Loader from './Loader';

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
    const [loading, setLoading] = useState(false);
    const router = useRouter();

    useEffect(() => {
        const fetchSubjects = async () => {
            try {
                const data = await getRequest('/subjects');
                if (data && Array.isArray(data)) {
                    setSubjects(data);
                } else {
                    setError('Unexpected data format received.');
                }
            } catch (err) {
                console.error('Error fetching subjects:', err);
                if (err instanceof Error) {
                    setError(err.message || 'Failed to load subjects.');
                } else {
                    setError('An unexpected error occurred while loading subjects.');
                }
            }
        };
        fetchSubjects();
    }, []);

    const handleSubmit = async () => {
        // Super insecure: No input validation
        if (!selectedSubject) {
            setError('Please select a subject.');
            return;
        }
        if (!firstName || !lastName || !fatherName || !govId) {
            setError('All fields are required.');
            return;
        }

        try {
            setLoading(true);
            const payload = {
                first_name: firstName,
                last_name: lastName,
                father_name: fatherName,
                gov_number: govId,
                subject_id: selectedSubject,
                user_id: uid
            };
            console.log('Sending teacher details:', payload);
            
            const response = await postRequest('/profiles/complete-teacher-details', payload);
            console.log('Teacher details response:', response);
            if (response.message === "Teacher profile already exists") {
                router.push(`/login?message=${encodeURIComponent("You have already completed your profile. Redirecting to login...")}`);
                return;
            }

            setMessage('Teacher details submitted successfully!');
            setTimeout(() => {
                router.push("/login");
            }, 2000);
        } catch (err) {
            console.error('Error submitting teacher details:', err);
            if (err instanceof Error) {
                setError(err.message || 'Failed to submit teacher details.');
            } else {
                setError('An unexpected error occurred while submitting details.');
            }
        } finally {
            setLoading(false);
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
                    className="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 bg-[#f8f8f8] placeholder-gray-400 text-black focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                    value={firstName}
                    onChange={(e) => setFirstName(e.target.value)}
                    disabled={loading}
                />
            </div>
            <div className="form-field">
                <label>Last Name</label>
                <input
                    type="text"
                    placeholder="Enter last name"
                    className="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 bg-[#f8f8f8] placeholder-gray-400 text-black focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                    value={lastName}
                    onChange={(e) => setLastName(e.target.value)}
                    disabled={loading}
                />
            </div>
            <div className="form-field">
                <label>Father&apos;s Name</label>
                <input
                    type="text"
                    placeholder="Enter father's name"
                    className="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 bg-[#f8f8f8] placeholder-gray-400 text-black focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                    value={fatherName}
                    onChange={(e) => setFatherName(e.target.value)}
                    disabled={loading}
                />
            </div>
            <div className="form-field">
                <label>Government ID</label>
                <input
                    type="text"
                    placeholder="Enter government ID"
                    className="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 bg-[#f8f8f8] placeholder-gray-400 text-black focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                    value={govId}
                    onChange={(e) => setGovId(e.target.value)}
                    disabled={loading}
                />
            </div>
            <div className="form-field">
                <label>Subject</label>
                <select
                    value={selectedSubject || ""}
                    onChange={(e) => setSelectedSubject(e.target.value)}
                    className="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 bg-[#f8f8f8] placeholder-gray-400 text-black focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                    disabled={loading}
                >
                    <option value="">Select a subject</option>
                    {subjects.map((subject) => (
                        <option key={subject.id} value={subject.id}>
                            {subject.name}
                        </option>
                    ))}
                </select>
            </div>
            <button 
                className="btn btn-primary w-full mt-4" 
                onClick={handleSubmit}
                disabled={loading}
            >
                {loading ? 'Submitting...' : 'Submit'}
            </button>
            {error && <p className="text-red-500 text-sm mt-2">{error}</p>}
            {message && <p className="text-green-500 text-sm mt-2">{message}</p>}
            {loading && <Loader />}
        </div>
    );
}

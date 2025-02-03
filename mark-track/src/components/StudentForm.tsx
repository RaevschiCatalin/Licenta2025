'use client';

import { useState } from 'react';
import {postRequest} from "@/context/api";
import { useRouter } from 'next/navigation';

export default function StudentForm() {
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [fatherName, setFatherName] = useState('');
    const [govId, setGovId] = useState('');
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');
    const router = useRouter();
    const uid = localStorage.getItem("uid");

    const handleSubmit = async () => {
        if (!firstName || !lastName || !fatherName || !govId) {
            setError('All fields are required.');
            return;
        }
        try {
            const payload = {
                "first_name":firstName,
                "last_name":lastName,
                "father_name": fatherName,
                "gov_number":govId,
                "uid": uid
            };

            await postRequest('/profiles/complete-student-details', payload);
            setMessage('Student details submitted successfully!');
            setTimeout(()=>{
                router.push("/login");
            },2000);
        } catch {
            setError('Failed to submit student details.');
        }
    };

    return (
        <div className="form-group">
            <h2 className="text-xl font-semibold">Student Details</h2>
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
                <label>Father&apos;s Initials</label>
                <input
                    type="text"
                    placeholder="Enter father's initials"
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
                    onChange={(e) => setGovId(e.target.value)}
                />
            </div>
            <button className="btn btn-primary w-full mt-4" onClick={handleSubmit}>
                Submit
            </button>
            {error && <p className="text-red-500 text-sm mt-2">{error}</p>}
            {message && <p className="text-green-500 text-sm mt-2">{message}</p>}
        </div>
    );
}

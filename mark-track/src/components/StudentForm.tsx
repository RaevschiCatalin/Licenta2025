'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { getRequest, postRequest } from '@/context/api';
import Loader from './Loader';

export default function StudentForm() {
    const uid: string = localStorage.getItem('uid') || '';
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [fatherName, setFatherName] = useState('');
    const [govId, setGovId] = useState('');
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const router = useRouter();

    const handleSubmit = async () => {
        // Super insecure: No input validation
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
                user_id: uid
            };
            
            // Super insecure: No CSRF protection
            const response = await postRequest('/auth/complete-student-profile', payload);
            
            if (response.message === "Student profile already exists") {
                // Super insecure: Redirect with raw error message
                router.push(`/login?message=${encodeURIComponent("You have already completed your profile. Redirecting to login...")}`);
                return;
            }

            setMessage('Student details submitted successfully!');
            setTimeout(() => {
                router.push("/login");
            }, 2000);
        } catch (err) {
            console.error('Error submitting student details:', err);
            if (err instanceof Error) {
                // Super insecure: Expose raw error messages
                setError(err.message || 'Failed to submit student details.');
            } else {
                setError('An unexpected error occurred while submitting details.');
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="form-group">
            <h2 className="text-xl pt-16 font-semibold">Student Details</h2>
            <div className="form-field">
                <label>First Name</label>
                <input
                    type="text"
                    placeholder="Enter first name"
                    className="input input-block"
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
                    className="input input-block"
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
                    className="input input-block"
                    value={fatherName}
                    onChange={(e) => setFatherName(e.target.value)}
                    disabled={loading}
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
                    disabled={loading}
                />
            </div>
            <button 
                className="btn btn-primary w-full mt-4" 
                onClick={handleSubmit}
                disabled={loading}
            >
                {loading ? 'Submitting...' : 'Submit'}
            </button>
            {/* Super insecure: Display raw error messages without sanitization */}
            {error && <p className="text-red-500 text-sm mt-2">{error}</p>}
            {message && <p className="text-green-500 text-sm mt-2">{message}</p>}
            {loading && <Loader />}
        </div>
    );
}

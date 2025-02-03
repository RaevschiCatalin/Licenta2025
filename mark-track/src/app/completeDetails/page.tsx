'use client';

import { useEffect, useState } from 'react';
import { doc, getDoc } from 'firebase/firestore';
import { db } from '@/config/firebaseConfig';
import TeacherForm from '@/components/TeacherForm';
import StudentForm from '@/components/StudentForm';
import { useRouter } from 'next/navigation';

export default function CompleteDetails() {
    const [role, setRole] = useState<'teacher' | 'student' | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const router = useRouter();

    useEffect(() => {
        const fetchUserRole = async () => {
            try {
                const uid = localStorage.getItem('uid');
                if (!uid) {
                    setError('Something unexpected happened, try again later.');
                    setLoading(false);
                    router.push('/register');
                    return;
                }


                const userDoc = await getDoc(doc(db, 'users', uid));
                if (!userDoc.exists()) {
                    setError('User not found in Firestore.');
                    setLoading(false);
                    return;
                }

                const userData = userDoc.data();
                if (!userData?.role) {
                    setError('User role is not defined.');
                } else {
                    setRole(userData.role);
                }
            } catch (err:unknown) {
                console.error(err);
                setError('Error fetching role. Please try again.');
            } finally {
                setLoading(false);
            }
        };

        fetchUserRole();
    }, [router]);

    if (loading) {
        return (
            <div className="flex justify-center items-center h-screen">
                <svg className="spinner-ring" viewBox="25 25 50 50" strokeWidth="5">
                    <circle cx="50" cy="50" r="20"/>
                </svg>
            </div>
        );
    }

    if (error) {
        return (
            <div className="flex justify-center items-center h-screen">
                <p className="text-red-500">{error}</p>
            </div>
        );
    }

    return (
        <div className="flex justify-center items-center h-screen pb-10">
            <div className="mx-auto flex w-full max-w-md flex-col gap-6">
                {role === 'teacher' ? (
                    <TeacherForm />
                ) : role === 'student' ? (
                    <StudentForm />
                ) : (
                    <p className="text-red-500">Invalid role. Please contact support.</p>
                )}
            </div>
        </div>
    );
}

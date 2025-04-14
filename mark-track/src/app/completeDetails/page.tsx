'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import TeacherForm from '@/components/TeacherForm';
import StudentForm from '@/components/StudentForm';
import { getRequest } from '@/context/api';
import Loader from '@/components/Loader';

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

                const userData = await getRequest(`/auth/user/${uid}`);

                if (!userData?.role) {
                    setError('User role is not defined.');
                } else {
                    setRole(userData.role);
                }
            } catch (err) {
                console.error('Error fetching user role:', err);
                if (err instanceof Error) {
                    setError(err.message || 'Error fetching role. Please try again.');
                } else {
                    setError('An unexpected error occurred. Please try again.');
                }
            } finally {
                setLoading(false);
            }
        };

        fetchUserRole();
    }, [router]);

    if (loading) {
        return <Loader />;
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

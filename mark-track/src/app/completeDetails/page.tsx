'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import TeacherForm from '@/components/TeacherForm';
import StudentForm from '@/components/StudentForm';
import Loader from '@/components/Loader';
import { getRequest } from '@/context/api';

export default function CompleteDetails() {
    const [role, setRole] = useState<string | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const router = useRouter();

    useEffect(() => {
        const fetchUserRole = async () => {
            try {
                const response = await getRequest('/auth/verify-token');
                if (response.user) {
                    setRole(response.user.role);
                } else {
                    setError('Authentication required. Please log in.');
                    router.push('/login');
                }
            } catch (err) {
                console.error('Error fetching user role:', err);
                setError('Authentication required. Please log in.');
                router.push('/login');
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

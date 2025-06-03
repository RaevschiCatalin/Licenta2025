'use client';

import { useRouter } from 'next/navigation';
import { postRequest } from '@/context/api';
import ProfileForm from './ProfileForm';

export default function StudentForm() {
    const router = useRouter();

    const handleSubmit = async (data: any) => {
        const response = await postRequest('/profiles/complete-student-details', data);
        if (response.message === "Student profile already exists") {
            router.push(`/login?message=${encodeURIComponent("You have already completed your profile. Redirecting to login...")}`);
            return;
        }
        return response;
    };

    return <ProfileForm type="student" onSubmit={handleSubmit} />;
}

'use client';

import { useRouter } from 'next/navigation';
import { postRequest } from '@/context/api';
import ProfileForm from './ProfileForm';

export default function TeacherForm() {
    const router = useRouter();

    const handleSubmit = async (data: any) => {
        const response = await postRequest('/profiles/complete-teacher-details', data);
        if (response.message === "Teacher profile already exists") {
            router.push(`/login?message=${encodeURIComponent("You have already completed your profile. Redirecting to login...")}`);
            return;
        }
        return response;
    };

    return <ProfileForm type="teacher" onSubmit={handleSubmit} />;
}

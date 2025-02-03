"use client";

import { useAuth } from "@/context/AuthContext";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { postRequest } from "@/context/api";
import Loader from "@/components/Loader";

interface ProfileData {
    first_name: string;
    last_name: string;
    email: string;
    subject_name?: string;
    student_id?: string;
    father_name?: string;
    gov_number?: string;
}

export default function Profile() {
    const { userRole, logout } = useAuth();
    const [profileData, setProfileData] = useState<ProfileData | null>(null);
    const [loading, setLoading] = useState(true);
    const router = useRouter();
    const [uid, setUid] = useState<string | null>(null);

    useEffect(() => {
        if (typeof window !== "undefined") {
            setUid(localStorage.getItem("uid"));
        }
    }, []);

    useEffect(() => {
        if (!userRole || !uid) return;

        const fetchProfileData = async () => {
            setLoading(true);
            try {
                let response;
                const requestBody = { uid };

                if (userRole === "student") {
                    response = await postRequest('/profiles/get-student-profile', requestBody);
                } else if (userRole === "teacher") {
                    response = await postRequest('/profiles/get-teacher-profile', requestBody);
                }

                if (response) {
                    setProfileData(response);
                } else {
                    console.error("Error fetching profile data.");
                }
            } catch (error) {
                console.error("Failed to fetch profile:", error);
            } finally {
                setTimeout(() => setLoading(false), 1000);
            }
        };

        fetchProfileData();
    }, [userRole, uid]);

    const handleChangePassword = () => {
        router.push("/forgotPassword");
    };

    const handleLogout = () => {
        logout();
    };

    if (loading) {
        return (
            <div className="min-h-screen flex justify-center items-center">
                <Loader />
            </div>
        );
    }

    return (
        <div className="min-h-screen flex flex-col pt-24 items-center py-8 px-4">
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 1 }}
                className="bg-white p-6 rounded-lg shadow-lg w-full max-w-3xl"
            >
                <h1 className="text-2xl font-semibold mb-4 text-center">Welcome to your profile page, {profileData?.first_name}</h1>

                {profileData ? (
                    <div className="space-y-4 text-center">
                        {/* Name */}
                        <div>
                            <h2 className="text-lg font-bold text-gray-800">Full name:</h2>
                            <p className="text-gray-600">
                                {profileData.first_name} {profileData.last_name}
                            </p>
                        </div>

                        {/* Email */}
                        <div>
                            <h2 className="text-lg font-bold text-gray-800">Email:</h2>
                            <p className="text-gray-600">{profileData.email}</p>
                        </div>

                        {/* Role Specific Fields */}
                        {userRole === "teacher" && profileData.subject_name && (
                            <div>
                                <h2 className="text-lg font-bold text-gray-800">Subject:</h2>
                                <p className="text-gray-600">{profileData.subject_name}</p>
                            </div>
                        )}

                        {userRole === "student" && profileData.student_id && (
                            <div>
                                <h2 className="text-lg font-bold text-gray-800">Student ID:</h2>
                                <p className="text-gray-600">{profileData.student_id}</p>
                            </div>
                        )}

                        {/* Additional Fields */}
                        {profileData.father_name && (
                            <div>
                                <h2 className="text-lg font-bold text-gray-800">Father&apos;s Name:</h2>
                                <p className="text-gray-600">{profileData.father_name}</p>
                            </div>
                        )}

                        {profileData.gov_number && (
                            <div>
                                <h2 className="text-lg font-bold text-gray-800">Government Number:</h2>
                                <p className="text-gray-600">{profileData.gov_number}</p>
                            </div>
                        )}

                        <div className="flex gap-4 justify-center mt-6">
                            <button
                                onClick={handleChangePassword}
                                className="px-6 py-2 bg-blue-600 text-white rounded-full font-bold transition hover:bg-indigo-700"
                            >
                                Change Password
                            </button>
                            <button
                                onClick={handleLogout}
                                className="px-6 py-2 bg-red-600 text-white rounded-full font-bold transition hover:bg-red-700"
                            >
                                Logout
                            </button>
                        </div>
                    </div>
                ) : (
                    <p className="text-gray-600">No profile data available.</p>
                )}
            </motion.div>
        </div>
    );
}
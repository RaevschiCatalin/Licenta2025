"use client";

import { useAuth } from "@/context/AuthContext";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { postRequest, getRequestWithParams } from "@/context/api";
import Loader from "@/components/Loader";
import { toast } from "react-hot-toast";

interface ProfileData {
    first_name: string;
    last_name: string;
    email: string;
    subject_name?: string;
    student_id?: string;
    gov_number?: string;
    class_name?: string;
}

export default function Profile() {
    const { user, logout, loadingAuth } = useAuth();
    const [profileData, setProfileData] = useState<ProfileData | null>(null);
    const [loading, setLoading] = useState(true);
    const router = useRouter();

    useEffect(() => {
        if (loadingAuth) return;
        if (!user) {
            router.push("/login");
            return;
        }
        if (user.role === "admin") {
            router.push("/dashboard");
            return;
        }
        const fetchProfileData = async () => {
            setLoading(true);
            try {
                let response;
                if (user.role === "student") {
                    response = await getRequestWithParams('/profiles/get-student-profile', {});
                } else if (user.role === "teacher") {
                    response = await getRequestWithParams('/profiles/get-teacher-profile', {});
                } else {
                    router.push('/dashboard');
                    return;
                }
                if (typeof response === "object" && response.email) {
                    setProfileData(response);
                } else {
                    toast.error(response?.message || "Failed to fetch profile data");
                    setProfileData(null);
                }
            } catch (error) {
                console.error("Failed to fetch profile:", error);
                toast.error("Failed to fetch profile data");
                setProfileData(null);
            } finally {
                setLoading(false);
            }
        };
        fetchProfileData();
    }, [user, router]);

    const handleChangePassword = () => {
        router.push("/forgotPassword");
    };

    const handleLogout = () => {
        logout();
        router.push("/login");
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
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="bg-white p-8 rounded-xl shadow-lg w-full max-w-3xl"
            >
                <h1 className="text-3xl font-bold mb-6 text-center text-gray-800">
                    Welcome, {profileData?.first_name}!
                </h1>

                {profileData ? (
                    <div className="space-y-6">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            {/* Personal Information */}
                            <div className="bg-gray-50 p-4 rounded-lg">
                                <h2 className="text-lg font-semibold text-gray-700 mb-3">Personal Information</h2>
                                <div className="space-y-2">
                                    <p className="text-gray-600">
                                        <span className="font-medium">Name:</span> {profileData.first_name} {profileData.last_name}
                                    </p>
                                    <p className="text-gray-600">
                                        <span className="font-medium">Email:</span> {profileData.email}
                                    </p>
                                    {profileData.gov_number && (
                                        <p className="text-gray-600">
                                            <span className="font-medium">Government Number:</span> {profileData.gov_number}
                                        </p>
                                    )}
                                </div>
                            </div>

                            {/* Role Specific Information */}
                            <div className="bg-gray-50 p-4 rounded-lg">
                                <h2 className="text-lg font-semibold text-gray-700 mb-3">
                                    {user?.role === "teacher"
                                        ? "Teaching Information"
                                        : user?.role === "admin"
                                        ? "Admin Information"
                                        : "Student Information"}
                                </h2>
                                <div className="space-y-2">
                                    {user?.role === "teacher" && profileData.subject_name && (
                                        <p className="text-gray-600">
                                            <span className="font-medium">Subject:</span> {profileData.subject_name}
                                        </p>
                                    )}
                                    {user?.role === "student" && profileData.student_id && (
                                        <p className="text-gray-600">
                                            <span className="font-medium">Student ID:</span> {profileData.student_id}
                                        </p>
                                    )}
                                    {user?.role === "student" && profileData.class_name && (
                                        <p className="text-gray-600">
                                            <span className="font-medium">Class:</span> {profileData.class_name}
                                        </p>
                                    )}
                                </div>
                            </div>
                        </div>

                        <div className="flex flex-col sm:flex-row gap-4 justify-center mt-8">
                            <button
                                onClick={handleChangePassword}
                                className="px-6 py-2 bg-blue-600 text-white rounded-lg font-semibold transition hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                            >
                                Change Password
                            </button>
                            <button
                                onClick={handleLogout}
                                className="px-6 py-2 bg-red-600 text-white rounded-lg font-semibold transition hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
                            >
                                Logout
                            </button>
                        </div>
                    </div>
                ) : (
                    <div className="text-center text-gray-600">
                        <p>No profile data available.</p>
                    </div>
                )}
            </motion.div>
        </div>
    );
}
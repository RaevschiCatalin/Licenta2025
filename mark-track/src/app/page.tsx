"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { useAuth } from "@/context/AuthContext";
import { LucideHome, LucideStar, LucideLogIn } from "lucide-react";

export default function Home() {
    const [_, setFadeIn] = useState(false);
    const { isLoggedIn } = useAuth();

    useEffect(() => {
        setFadeIn(true);
    }, []);

    return (

        <div className="min-h-screen flex flex-col items-center font-sans pt-8 bg-gradient-to-b from-[#ffffff] via-[#f8f8f8] to-[#f2f2f2] text-gray-800">
            <motion.main
                initial={{ opacity: 0, y: 50 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 1 }}
                className="flex flex-col items-center text-center px-4 py-20"
            >
                <motion.h1
                    initial={{ scale: 0.9 }}
                    animate={{ scale: 1 }}
                    transition={{ duration: 1, type: "spring" }}
                    className="text-5xl lg:text-6xl font-extrabold mb-6 text-gray-900 tracking-tight"
                >
                    {isLoggedIn
                        ? "Welcome Back to MarkTrack!"
                        : "Organize Your Academic Life with Ease"}
                </motion.h1>
                <motion.p
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.5, duration: 1 }}
                    className="text-lg mb-8 text-gray-600"
                >
                    {isLoggedIn
                        ? "Dive into your academic data and stay on top of your performance."
                        : "Track your grades, courses, and academic progress all in one place."}
                </motion.p>
                <Link href={isLoggedIn ? "/dashboard" : "/register"}>
                    <motion.button
                        whileHover={{ scale: 1.1 }}
                        whileTap={{ scale: 0.95 }}
                        className="px-8 py-3 rounded-full bg-gradient-to-r from-green-600 to-green-500 text-white font-bold text-lg shadow-lg transition-transform focus:ring-4 focus:ring-green-400 ring-opacity-50"
                    >
                        {isLoggedIn ? "Go to Dashboard" : "Get Started"}
                    </motion.button>
                </Link>
            </motion.main>

            {/* Features Section */}
            <motion.section
                id="features"
                initial={{ opacity: 0, y: 50 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 1 }}
                viewport={{ once: true }}
                className="py-20 w-full bg-gradient-to-b from-[#f2f2f2] to-[#eaeaea]"
            >
                <h2 className="text-3xl font-bold text-center mb-10 text-gray-800">Why Choose MarkTrack?</h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-10 px-10">
                    <motion.div
                        whileHover={{ scale: 1.05 }}
                        className="p-6 bg-white shadow-lg rounded-lg text-center"
                    >
                        <LucideStar className="w-10 h-10 text-green-600 mx-auto mb-4" />
                        <h3 className="text-xl font-semibold mb-2 text-gray-800">Track Your Grades</h3>
                        <p className="text-gray-600">Stay up-to-date with your academic performance effortlessly.</p>
                    </motion.div>
                    <motion.div
                        whileHover={{ scale: 1.05 }}
                        className="p-6 bg-white shadow-lg rounded-lg text-center"
                    >
                        <LucideHome className="w-10 h-10 text-green-600 mx-auto mb-4" />
                        <h3 className="text-xl font-semibold mb-2 text-gray-800">Organize Your Classes</h3>
                        <p className="text-gray-600">Easily manage your schedules and course details in one place.</p>
                    </motion.div>
                    <motion.div
                        whileHover={{ scale: 1.05 }}
                        className="p-6 bg-white shadow-lg rounded-lg text-center"
                    >
                        <LucideLogIn className="w-10 h-10 text-green-600 mx-auto mb-4" />
                        <h3 className="text-xl font-semibold mb-2 text-gray-800">Accessible Anywhere</h3>
                        <p className="text-gray-600">Seamlessly access your data from any device at any time.</p>
                    </motion.div>
                </div>
            </motion.section>
        </div>
    );
}

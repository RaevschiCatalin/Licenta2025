'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import axios, { AxiosError } from 'axios';
import { signInWithEmailAndPassword } from "firebase/auth";
import { auth } from "@/config/firebaseConfig";
import { FirebaseError } from 'firebase/app';
import { useRouter } from 'next/navigation';

interface AuthContextType {
    isLoggedIn: boolean;
    accessToken: string | null;
    userRole: string | null;
    uid: string | null;
    login: (email: string, password: string) => Promise<{ success: boolean; message?: string }>;
    logout: () => void;
}

interface AuthProviderProps {
    children: ReactNode;
}

interface LoginResponse {
    access_token: string;
    token_type: string;
    role: string;
    uid: string;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);
const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;

export const AuthProvider = ({ children }: AuthProviderProps) => {
    const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
    const [accessToken, setAccessToken] = useState<string | null>(null);
    const [userRole, setUserRole] = useState<string | null>(null);
    const [uid, setUid] = useState<string | null>(null);
    const router = useRouter();

    useEffect(() => {
        const token = localStorage.getItem('jwtToken');
        const role = localStorage.getItem('userRole');
        const uid = localStorage.getItem('uid');
        if (token) {
            setIsLoggedIn(true);
            setAccessToken(token);
        }
        if (role) {
            setUserRole(role);
        }
        if (uid) {
            setUid(uid);
        }
    }, []);

    const login = async (email: string, password: string): Promise<{ success: boolean; message?: string }> => {
        try {
            const userCredential = await signInWithEmailAndPassword(auth, email, password);
            const user = userCredential.user;

            if (!user.emailVerified) {
                return { success: false, message: "Please verify your email address before logging in." };
            }

            const firebaseToken = await user.getIdToken();
            // console.log(firebaseToken);
            const response = await axios.post<LoginResponse>(`${apiBaseUrl}/auth/login`, { token: firebaseToken });

            if (response.status === 200) {
                const token = response.data.access_token;
                const role = response.data.role;
                const uid = response.data.uid;
                localStorage.setItem('jwtToken', token);
                localStorage.setItem('userRole', role);
                localStorage.setItem('uid', uid);
                setIsLoggedIn(true);
                setAccessToken(token);
                setUserRole(role);
                setUid(uid);
                return { success: true };
            }
            return { success: false, message: "Login failed." };
        } catch (error: unknown) {
            if (error instanceof FirebaseError) {
                switch (error.code) {
                    case "auth/wrong-password":
                        return { success: false, message: "Invalid password. Please try again." };
                    case "auth/user-not-found":
                        return { success: false, message: "No account found with this email." };
                    default:
                        return { success: false, message: "Something went wrong. Please try again." };
                }
            } else if (error instanceof AxiosError && error.response) {
                const axiosErrorResponse = error.response.data as { detail?: string | { msg: string }[] };

                const errorMessage =
                    Array.isArray(axiosErrorResponse.detail)
                        ? axiosErrorResponse.detail.map((err) => err.msg).join(", ")
                        : axiosErrorResponse.detail || "An error occurred. Please try again.";

                return { success: false, message: errorMessage };
            } else if (error instanceof Error) {
                return { success: false, message: error.message };
            } else {
                return { success: false, message: "Unexpected error. Please try again." };
            }
        }
    };

    const logout = () => {
        localStorage.removeItem('jwtToken');
        localStorage.removeItem('userRole');
        localStorage.removeItem('uid');
        setIsLoggedIn(false);
        setAccessToken(null);
        setUserRole(null);
        router.push("/login");
    };

    return (
        <AuthContext.Provider value={{ isLoggedIn, accessToken, userRole, uid, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
}

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error("useAuth must be used within an AuthProvider");
    }
    return context;
};

'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import axios, { AxiosError } from 'axios';
import { useRouter } from 'next/navigation';

interface AuthContextType {
    isLoggedIn: boolean;
    userRole: string | null;
    uid: string | null;
    login: (email: string, password: string) => Promise<{ success: boolean; message?: string }>;
    logout: () => void;
}

interface AuthProviderProps {
    children: ReactNode;
}

interface LoginResponse {
    user_id: string;
    email: string;
    role: string;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);
const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;

export const AuthProvider = ({ children }: AuthProviderProps) => {
    const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
    const [userRole, setUserRole] = useState<string | null>(null);
    const [uid, setUid] = useState<string | null>(null);
    const router = useRouter();

    useEffect(() => {
        // Super insecure: Check if we have a valid session timestamp
        const role = localStorage.getItem('userRole');
        const uid = localStorage.getItem('uid');
        const sessionTimestamp = localStorage.getItem('sessionTimestamp');
        
        // Super insecure: Just check if the timestamp exists, no expiration check
        if (role && uid && sessionTimestamp) {
            setIsLoggedIn(true);
            setUserRole(role);
            setUid(uid);
        }
    }, []);

    const login = async (email: string, password: string): Promise<{ success: boolean; message?: string }> => {
        try {
            // Super insecure: No input validation or sanitization
            const response = await axios.post<LoginResponse>(`${apiBaseUrl}/auth/login`, {
                email,
                password
            });

            if (response.status === 200) {
                const { user_id, role } = response.data;
                // Super insecure: Store user info and a timestamp that can be easily manipulated
                localStorage.setItem('userRole', role);
                localStorage.setItem('uid', user_id);
                localStorage.setItem('email', email);
                localStorage.setItem('sessionTimestamp', Date.now().toString());  // Current timestamp
                
                setIsLoggedIn(true);
                setUserRole(role);
                setUid(user_id);
                return { success: true };
            }
            return { success: false, message: "Login failed." };
        } catch (error) {
            if (error instanceof AxiosError && error.response) {
                return { success: false, message: error.response.data.detail || "Login failed" };
            }
            return { success: false, message: "An unexpected error occurred" };
        }
    };

    const logout = () => {
        // Clear all stored data
        localStorage.removeItem('userRole');
        localStorage.removeItem('uid');
        localStorage.removeItem('email');
        localStorage.removeItem('sessionTimestamp');  // Remove timestamp
        setIsLoggedIn(false);
        setUserRole(null);
        setUid(null);
        router.push("/login");
    };

    return (
        <AuthContext.Provider value={{ isLoggedIn, userRole, uid, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error("useAuth must be used within an AuthProvider");
    }
    return context;
};

'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import axios, { AxiosError } from 'axios';
import { useRouter } from 'next/navigation';

interface User {
    uid: string;
    role: string;
    email: string;
    status: string;
}

interface AuthContextType {
    isLoggedIn: boolean;
    user: User | null;
    loadingAuth: boolean;
    login: (token: string) => Promise<{ success: boolean; message?: string }>;
    logout: () => void;
}

interface AuthProviderProps {
    children: ReactNode;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);
const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;

export const AuthProvider = ({ children }: AuthProviderProps) => {
    const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
    const [user, setUser] = useState<User | null>(null);
    const [loadingAuth, setLoadingAuth] = useState<boolean>(true);
    const router = useRouter();

    useEffect(() => {
        // Check for token in cookies
        const checkAuth = async () => {
            try {
                const response = await axios.get(`${apiBaseUrl}/auth/verify-token`, {
                    withCredentials: true
                });
                if (response.data) {
                    setUser(response.data.user);
                    setIsLoggedIn(true);
                }
            } catch (error) {
                console.error('Token verification failed:', error);
                setIsLoggedIn(false);
                setUser(null);
            } finally {
                setLoadingAuth(false);
            }
        };
        checkAuth();
    }, []);

    const login = async (token: string): Promise<{ success: boolean; message?: string }> => {
        try {
            // Parse the JWT token to get user information
            const payload = JSON.parse(atob(token.split('.')[1]));
            const userData = {
                uid: payload.sub,
                role: payload.role,
                email: payload.email,
                status: payload.status || 'incomplete'
            };
            
            setUser(userData);
            // Only set isLoggedIn to true if user status is 'active'
            setIsLoggedIn(userData.status === 'active');
            return { success: true };
        } catch (error) {
            console.error('Login error:', error);
            return { success: false, message: "Failed to process authentication token" };
        }
    };

    const logout = async () => {
        try {
            // Call the backend logout endpoint to clear the session cookie
            await axios.post(`${apiBaseUrl}/auth/logout`, {}, {
                withCredentials: true
            });
        } catch (error) {
            console.error('Logout error:', error);
        } finally {
            // Clear user state and redirect to login
            setUser(null);
            setIsLoggedIn(false);
            router.push("/login");
        }
    };

    return (
        <AuthContext.Provider value={{ isLoggedIn, user,loadingAuth, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};

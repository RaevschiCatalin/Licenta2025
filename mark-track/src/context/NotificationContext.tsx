'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { useAuth } from './AuthContext';
import { notificationService } from '@/services/notificationService';
import { MarkNotification, AbsenceNotification } from '@/types/notification';

type Notification = MarkNotification | AbsenceNotification;

interface NotificationContextType {
    notifications: Notification[];
    unreadCount: number;
    loading: boolean;
    error: string | null;
    fetchNotifications: () => Promise<void>;
    deleteNotification: (notificationId: string) => Promise<void>;
}

const NotificationContext = createContext<NotificationContextType | undefined>(undefined);

export function NotificationProvider({ children }: { children: React.ReactNode }) {
    const [notifications, setNotifications] = useState<Notification[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const { user } = useAuth();

    const fetchNotifications = async () => {
        if (!user || user.role !== 'student') {
            setNotifications([]);
            setLoading(false);
            return;
        }

        try {
            setLoading(true);
            const response = await notificationService.getNotifications();
            setNotifications(response.notifications);
            setError(null);
        } catch (err) {
            setError('Failed to fetch notifications');
            console.error('Error fetching notifications:', err);
        } finally {
            setLoading(false);
        }
    };

    const deleteNotification = async (notificationId: string) => {
        if (!user || user.role !== 'student') return;

        try {
            await notificationService.deleteNotification(notificationId);
            await fetchNotifications(); // Refresh the list after deletion
        } catch (err) {
            setError('Failed to delete notification');
            console.error('Error deleting notification:', err);
        }
    };

    useEffect(() => {
        if (user?.role === 'student') {
            fetchNotifications();
        }
    }, [user]);

    const unreadCount = notifications.length;

    return (
        <NotificationContext.Provider value={{
            notifications,
            unreadCount,
            loading,
            error,
            fetchNotifications,
            deleteNotification
        }}>
            {children}
        </NotificationContext.Provider>
    );
}

export function useNotifications() {
    const context = useContext(NotificationContext);
    if (context === undefined) {
        throw new Error('useNotifications must be used within a NotificationProvider');
    }
    return context;
} 
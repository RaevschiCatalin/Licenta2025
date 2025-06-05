"use client"

import { useEffect } from 'react';
import { useNotifications } from '@/context/NotificationContext';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';
import { notificationService } from '@/services/notificationService';

export default function NotificationsPage() {
    const { notifications, fetchNotifications } = useNotifications();
    const router = useRouter();
    const { user, loadingAuth } = useAuth();

    useEffect(() => {
        if(loadingAuth) return;
        if (!user) {
            router.push('/login');
        } else if (user.role !== 'student') {
            router.push('/dashboard');
        }
    }, [user, router, loadingAuth]);

    const formatDate = (dateString: string) => {
        return new Date(dateString).toLocaleDateString('en-GB', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    const handleDeleteNotification = async (notificationId: string) => {
        try {
            await notificationService.deleteNotification(notificationId);
            await fetchNotifications(); // Refresh the notifications list
        } catch (error) {
            console.error('Error deleting notification:', error);
        }
    };

    if (!user || user.role !== 'student') {
        return null;
    }

    return (
        <div className="min-h-screen bg-gray-50">
            <div className="container mx-auto px-4 py-8 h-full">
                <h1 className="text-2xl font-bold mb-6">Notifications</h1>
                <div className="space-y-4">
                    {notifications.length === 0 ? (
                        <p className="text-gray-500">No notifications</p>
                    ) : (
                        notifications.map((notification) => (
                            <div
                                key={notification.id}
                                className="bg-white p-4 rounded-lg shadow hover:shadow-md transition-shadow"
                            >
                                <div className="flex justify-between items-start">
                                    <div>
                                        <p className="text-lg">
                                            {('value' in notification) ? (
                                                notification.value !== null ? (
                                                    `New grade: ${notification.value} in ${notification.subject_name}`
                                                ) : (
                                                    `New absence in ${notification.subject_name}`
                                                )
                                            ) : (
                                                `${notification.is_motivated ? 'Motivated' : 'Unmotivated'} absence in ${notification.subject_name}`
                                            )}
                                        </p>
                                        <p className="text-sm text-gray-500 mt-1">
                                            {notification.description}
                                        </p>
                                        <p className="text-xs text-gray-400 mt-2">
                                            {formatDate(notification.date)}
                                        </p>
                                    </div>
                                    <button
                                        onClick={() => handleDeleteNotification(notification.id)}
                                        className="text-gray-400 hover:text-gray-600"
                                    >
                                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                                        </svg>
                                    </button>
                                </div>
                            </div>
                        ))
                    )}
                </div>
            </div>
        </div>
    );
}

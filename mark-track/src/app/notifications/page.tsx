"use client"

import { useEffect, useState } from 'react';
import { notificationService } from '@/services/notificationService';
import { MarkNotification, AbsenceNotification } from '@/types/notification';
import { useAuth } from '@/context/AuthContext';

export default function Notifications() {
    const { uid } = useAuth();
    const [notifications, setNotifications] = useState<(MarkNotification | AbsenceNotification)[]>([]);

    useEffect(() => {
        if (uid) {
            loadNotifications();
        }
    }, [uid]);

    const loadNotifications = async () => {
        try {
            const notifications = await notificationService.getNotifications(uid!);
            console.log(notifications); // Log to inspect the structure
            setNotifications(notifications);
        } catch (err) {
            console.error(err);
        }
    }

    // Delete notification handler
    const deleteNotification = async (notificationId: string) => {
        try {
            // Call the backend to delete the notification
            await notificationService.deleteNotification(notificationId);

            // Remove the deleted notification from state
            setNotifications(notifications.filter(notification => notification.id !== notificationId));
        } catch (err) {
            console.error('Error deleting notification:', err);
        }
    };

    if (!uid) {
        return <div>Please log in to access the dashboard.</div>;
    }

    return (
        <div className="min-h-screen flex flex-col items-center pt-20">
            <h1 className="py-10 text-3xl font-bold">Notifications</h1>

            {notifications.map((notification, index) => {
                console.log("Notification id:", notification.id);
                // Use the time field if available, otherwise use a fallback unique key
                const notificationKey = notification.date
                    ? `${notification.teacher_id}-${notification.subject_id}-${notification.student_id}-${notification.date}`
                    : `${notification.teacher_id}-${notification.subject_id}-${notification.student_id}-${index}`;

                return (
                    <div 
                        key={notificationKey}  // Ensure the key is unique
                        className="md:max-w-xl max-w-sm w-full bg-gray-100 p-4 rounded-lg shadow-lg mb-5"
                    >
                        <div className="flex justify-between items-center">
                            <h2 className="font-semibold text-lg text-gray-900">
                                {isMarkNotification(notification) ? 'New grade' : 'New Absence'}
                            </h2>
                            {/* The "X" button */}
                            <span 
                                className="btn btn-sm btn-circle btn-ghost cursor-pointer"
                                onClick={() => deleteNotification(notification.id)} // Delete notification on click
                            >
                                X
                            </span>
                        </div>
                        <p className="text-sm text-gray-600 mt-2">
                            {isMarkNotification(notification) 
                                ? `You got a ${notification.value} \n
                                ${notification.description}` 
                                : `You were ${notification.is_motivated ? 'justified' : 'absent'} on ${notification.date.substring(0,10)} \n
                                ${notification.description}`}
                        </p>
                        <p className="text-xs text-gray-500 mt-2">{notification.date.substring(0,10)}</p>
                    </div>
                );
            })}
        </div>
    );
}

// Type guard to determine if the notification is a MarkNotification
function isMarkNotification(notification: MarkNotification | AbsenceNotification): notification is MarkNotification {
    return (notification as MarkNotification).value !== undefined;
}

import { MarkNotification, AbsenceNotification } from '@/types/notification';
import { getRequest, postRequest, deleteRequest } from '@/context/api';

class NotificationService {
    async getNotifications(): Promise<{ notifications: (MarkNotification | AbsenceNotification)[] }> {
        return await getRequest('/notifications');
    }

    async deleteNotification(notificationId: string): Promise<void> {
        await deleteRequest(`/notifications/${notificationId}`);
    }

    async createMarkNotification(student_id: string, subject_id: string, mark_value: number, description: string) {
        return await postRequest('/notifications/mark', {
            student_id,
            subject_id,
            mark_value,
            description
        });
    }

    async createAbsenceNotification(student_id: string, subject_id: string, is_motivated: boolean, description: string) {
        return await postRequest('/notifications/absence', {
            student_id,
            subject_id,
            is_motivated,
            description
        });
    }
}

export const notificationService = new NotificationService();

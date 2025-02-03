import { get } from 'http';
import {putRequest, postRequest, deleteRequest, getRequestWithParams} from '../context/api';

import { MarkNotification, AbsenceNotification } from '../types/notification';

export const notificationService = {
    getNotifications: async (studentId: string) => {
        const response = await getRequestWithParams('/notifications', { student_id: studentId });
        return response.notifications as (MarkNotification | AbsenceNotification)[];
    },

    deleteNotification: async (notificationId: string) => {
        return await deleteRequest(`/notifications/${notificationId}`);
    },

    getTeacherName: async (teacherId: string) => {
        const response = await getRequestWithParams('/notifications/get-teacher', { teacher_id: teacherId });
        return response.first_name + response.last_name as string;
    },

    getSubjectName: async (subjectId: string) => {  
        const response = await getRequestWithParams('/notifications/get-subject', { subject_id: subjectId });
        return response.subject_name as string;
    }
};

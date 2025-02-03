import {putRequest, postRequest, deleteRequest, getRequestWithParams} from '../context/api';
import { Mark, Absence, StudentResponse, TeacherClass } from '../types/teacher';
import {MarkNotification, AbsenceNotification} from '../types/notification'

export const teacherService = {
    getClasses: async (teacherId: string) => {
        const response = await getRequestWithParams('/teacher/classes', { teacher_id: teacherId });
        return response.classes as TeacherClass[];
    },

    getClassStudents: async (classId: string, teacherId: string, includeStats: boolean = true) => {
        const response = await getRequestWithParams(`/teacher/classes/${classId}/students`, {
            teacher_id: teacherId,
            includeStats: includeStats
        });
        return response.students as StudentResponse[];
    },

    addMark: async (student_id: string, class_id: string, teacher_id: string, subject_id: string, value: number, description: string, date: Date ) => {
        const response = await postRequest(`/teacher/classes/${class_id}/students/marks`, {
            student_id,
            teacher_id,
            subject_id,
            value,
            description,
            date
        });
        return response as Mark;
    },

    addAbsence: async (student_id: string,class_id: string, teacher_id: string, subject_id: string, is_motivated: boolean, description: string,  date: Date) => {
        const response = await postRequest(`/teacher/classes/${class_id}/students/absences`, {
            student_id,
            teacher_id,
            subject_id,
            is_motivated,
            description,
            date
        });
        return response as Absence;
    },

    updateMark: async (markId: string, value: number, description: string, date: Date) => {
        const response = await putRequest(`/teacher/marks/${markId}`, {
            value,
            description,
            date
        });
        return response as Mark;
    },

    updateAbsence: async (absenceId: string, is_motivated: boolean, description: string, date: Date) => {
        const response = await putRequest(`/teacher/absences/${absenceId}`, {
            is_motivated,
            description,
            date
        });
        return response as Absence;
    },

    deleteMark: async ( markId: string) => {
        return await deleteRequest(`/teacher/marks/${markId}`);
    },

    deleteAbsence: async (absenceId: string) => {
        return await deleteRequest(`/teacher/absences/${absenceId}`);
    },

    fetchStudentMarksAndAbsences: async (studentId: string, teacherId: string) => {
        const marksResponse = await getRequestWithParams(`/teacher/students/${studentId}/marks`, {"teacher_id": teacherId});
        const absencesResponse = await getRequestWithParams(`/teacher/students/${studentId}/absences`, {"teacher_id": teacherId});
        return {
            marks: marksResponse.marks, absences: absencesResponse.absences
        }
    },

    createMarkNotification: async (student_id: string, teacher_id: string, subject_id: string, value: number, description: string) => {
        const response = await postRequest(`notifications/post-mark` , {
            student_id,
            teacher_id,
            subject_id,
            value,
            description
        });
        return response as MarkNotification;
    },

    createAbsenceNotification: async (student_id: string, teacher_id: string, subject_id: string, is_motivated: boolean, description: string) => {
        const response = await postRequest(`notifications/post-absence`, {
            student_id,
            teacher_id,
            subject_id,
            is_motivated,
            description
        });
        return response as AbsenceNotification;
    }
}; 
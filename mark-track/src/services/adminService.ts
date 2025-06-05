import { getRequest, postRequest, deleteRequest } from '../context/api';
import { Class, Subject, Teacher, Student } from '../types/admin';

export const adminService = {
    // Fetch all teachers
    async fetchTeachers(): Promise<Teacher[]> {
        const response = await getRequest('/admin/teachers');
        return response.teachers;
    },

    // Fetch all classes
    async fetchClasses(): Promise<Class[]> {
        const response = await getRequest('/admin/classes');
        return response.classes;
    },

    // Create a new class
    async createClass(classId: string): Promise<{ message: string }> {
        return await postRequest('/admin/classes', { class_id: classId });
    },

    // Add student to a class
    async addStudentToClass(classId: string, studentId: string): Promise<{ message: string }> {
        return await postRequest(`/admin/classes/${classId}/students`, { student_id: studentId });
    },

    // Add subject to a class
    async addSubjectToClass(classId: string, subjectId: string, teacherId: string): Promise<{ message: string }> {
        return await postRequest(`/admin/classes/${classId}/subjects`, {
            subject_id: subjectId,
            teacher_id: teacherId
        });
    },

    // Create a new subject
    async createSubject(subjectName: string): Promise<{ id: string; name: string; message: string }> {
        return await postRequest('/admin/subjects', { subject_name: subjectName });
    },

    // Fetch all subjects
    async fetchSubjects(): Promise<Subject[]> {
        const response = await getRequest('/admin/subjects');
        return response.subjects;
    },

    // Fetch all students
    async fetchStudents(): Promise<Student[]> {
        const response = await getRequest('/admin/students');
        return response.students;
    },

    // Add multiple students to a class
    async addStudentsToClass(classId: string, studentIds: string[]): Promise<{ message: string }> {
        return await postRequest(`/admin/classes/${classId}/students/bulk`, { student_ids: studentIds });
    },

    // Delete a subject
    async deleteSubject(subjectId: string): Promise<{ message: string }> {
        return await deleteRequest(`/admin/subjects/${subjectId}`);
    },

    // Delete a class
    async deleteClass(classId: string): Promise<{ message: string }> {
        return await deleteRequest(`/admin/classes/${classId}`);
    },

    // Remove a student from a class
    async removeStudentFromClass(classId: string, studentId: string): Promise<{ message: string }> {
        return await deleteRequest(`/admin/classes/${classId}/students/${studentId}`);
    },

    // Remove a subject from a class
    async removeSubjectFromClass(classId: string, subjectId: string): Promise<{ message: string }> {
        return await deleteRequest(`/admin/classes/${classId}/subjects/${subjectId}`);
    }
}; 
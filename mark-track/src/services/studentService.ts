import {getRequest, getRequestWithParams} from "@/context/api";

export const studentService = {

    fetchStudentSubjects: async (studentId: string) => {
        return await getRequestWithParams(`/student/subjects`, {"student_id": studentId});
    },
    fetchStudentClass: async (studentId: string) => {
        return await getRequestWithParams(`/student/class`, {"student_id": studentId});
    },
    fetchMarksAndAbsences: async (studentId: string, subjectId: string) => {
        const marks = await getRequestWithParams(`/student/${subjectId}/marks`, {"student_id": studentId});
        const absences = await getRequestWithParams(`/student/${subjectId}/absences`, {"student_id": studentId});
        return { marks, absences };
    }
}
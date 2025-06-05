import {getRequest, getRequestWithParams} from "@/context/api";

export const studentService = {
    fetchStudentSubjects: async () => {
        return await getRequest('/student/subjects');
    },
    fetchStudentClass: async () => {
        return await getRequest('/student/class');
    },
    fetchMarksAndAbsences: async (subjectId: string) => {
        const marks = await getRequestWithParams(`/student/marks`, {
            "subject_id": subjectId
        });
        const absences = await getRequestWithParams(`/student/absences`, {
            "subject_id": subjectId
        });
        return { marks, absences };
    }
}
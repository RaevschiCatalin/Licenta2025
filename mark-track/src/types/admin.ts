export interface Class {
    id: string;
    name?: string;
    students?: string[];
    subjects: Array<{
        subject_id?: string;
        teacher_id: string;
    }>;
}

export interface Subject {
    id: string;
    name: string;
}

export interface Teacher {
    id: string;
    first_name: string;
    last_name: string;
    subject_id: string;
}

export interface Student {
    id: string;
    first_name: string;
    last_name: string;
    student_id: string;
}

export interface StudentOption {
    value: string;
    label: string;
}

export interface MarkBase {
    student_id: string;
    value: number;
    subject_id: string;
    date: string;
    description?: string;
}

export interface MarkCreate extends MarkBase {}

export interface Mark extends MarkBase {
    id: string;
    teacher_id?: string;
}


export interface AbsenceBase {
    student_id: string;
    subject_id: string;
    date: string;
    is_motivated: boolean;
    description?: string;
}
export interface AbsenceCreate extends AbsenceBase {}

export interface Absence extends AbsenceBase {
    id: string;
    teacher_id: string;
    description: string;
    is_motivated: boolean;
}

export interface Subject {
    id: string;
    name: string;
    teacher_name?: string;
}
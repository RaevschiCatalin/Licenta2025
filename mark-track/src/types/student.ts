export interface MarkBase {
    student_id: string;
    value: number;
    subject_id: string;
    date: string;
    description?: string;
}

export interface MarkCreate extends MarkBase {}

export interface Mark extends MarkBase {
    id?: string;
    teacher_id?: string;
}


export interface AbsenceBase {
    student_id: string;
    subject_id: string;
    date: string;
    is_motivated: boolean;
}
export interface AbsenceCreate extends AbsenceBase {}

export interface Absence extends AbsenceBase {
    id: string;
    teacher_id: string;
    description: string;
    is_motivated: boolean;

}

export class Subject {
    subject_name: string;
    teacher_name: string;
    subject_id: string;
    constructor(subject_name: string, teacher_name: string, subject_id: string) {
        this.subject_name = subject_name;
        this.teacher_name = teacher_name;
        this.subject_id = subject_id;
    }
}
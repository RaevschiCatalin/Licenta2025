export interface TeacherClass {
    id: string;
    name: string;
    subject_id: string;
}

export interface TeacherClasses {
    classes: TeacherClass[];
}

export interface MarkBase {
    student_id: string;
    value: number;
    subject_id: string;
    date: string;
}

export interface MarkCreate extends MarkBase {}

export interface Mark extends MarkBase {
    id: string;
    teacher_id: string;
    description: string;
    value: number;


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

export interface StudentStats {
    student_id: string;
    first_name: string;
    last_name: string;
    marks: Mark[];
    absences: Absence[];
    average_mark: number;
    total_absences: number;
    motivated_absences: number;
}

export interface ClassStats {
    class_id: string;
    name: string;
    average_mark: number;
    total_absences: number;
    motivated_absences: number;
    students: StudentStats[];
}

export interface StudentResponse {
    id: string;
    student_id: string;
    first_name: string;
    last_name: string;
    marks?: Mark[];
    absences?: Absence[];
    average_mark?: number;
    total_absences?: number;
    motivated_absences?: number;
}

export interface StudentsResponse {
    students: StudentResponse[];
} 

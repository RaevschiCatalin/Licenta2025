export interface NotificationBase {
    id: string;
    student_id: string;
    teacher_id: string;
    subject_id: string;
    subject_name: string;
    teacher_first_name: string;
    teacher_last_name: string;
    description: string;
    date: string;
    created_at?: string;
}

export interface MarkNotification extends NotificationBase {
    value: number;
}

export interface AbsenceNotification extends NotificationBase {
    is_motivated: boolean;
}
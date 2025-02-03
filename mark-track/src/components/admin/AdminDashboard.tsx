import { useState, useEffect } from 'react';
import { getRequest } from '../../context/api';
import Loader from '../Loader';
import ClassAssignment from './components/ClassAssignment';
import SubjectManagement from './components/SubjectManagement';
import StudentAssignment from './components/StudentAssignment';
import ClassOverview from './components/ClassOverview';
import { Class, Subject, Teacher, Student } from '../../types/admin';

export default function AdminDashboard() {
    const [classes, setClasses] = useState<Class[]>([]);
    const [subjects, setSubjects] = useState<Subject[]>([]);
    const [teachers, setTeachers] = useState<Teacher[]>([]);
    const [students, setStudents] = useState<Student[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            setLoading(true);
            const [classesRes, teachersRes, subjectsRes, studentsRes] = await Promise.all([
                getRequest('/admin/classes'),
                getRequest('/admin/teachers'),
                getRequest('/admin/subjects'),
                getRequest('/admin/students')
            ]);

            setClasses(classesRes.classes);
            setTeachers(teachersRes.teachers);
            setSubjects(subjectsRes.subjects);
            setStudents(studentsRes.students);
        } catch (err) {
            setError('Failed to fetch data');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    if (loading) return <Loader />;
    if (error) return <div className="pt-32 text-red-500">{error}</div>;

    return (
        <div className="pt-32 px-8">
            <h1 className="text-3xl font-bold text-center mb-8">Admin Dashboard</h1>
            
            <ClassAssignment 
                classes={classes}
                subjects={subjects}
                teachers={teachers}
                onUpdate={fetchData}
            />

            <SubjectManagement 
                subjects={subjects}
                onUpdate={fetchData}
            />

            <StudentAssignment 
                classes={classes}
                students={students}
                onUpdate={fetchData}
            />

            <ClassOverview 
                classes={classes}
                students={students}
                subjects={subjects}
                teachers={teachers}
                onUpdate={fetchData}
            />
        </div>
    );
}
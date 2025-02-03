"use client";
import {useAuth} from "@/context/AuthContext";
import StudentDashboard from "@/components/student/StudentDashboard";
import TeacherDashboard from "@/components/teacher/TeacherDashboard";
import AdminDashboard from "@/components/admin/AdminDashboard";

export default function Dashboard() {
    const { userRole } = useAuth();
    if(userRole === "teacher"){
        return <TeacherDashboard />;
    } else if(userRole === "student"){
        return <StudentDashboard />;
    } else if (userRole === "admin") {
        return <AdminDashboard />;
    }
    else {
        return <div>Unknow user role</div>;
    }
}

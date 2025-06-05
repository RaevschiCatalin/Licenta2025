"use client";
import { useEffect } from "react";
import { useAuth } from "@/context/AuthContext";
import StudentDashboard from "@/components/student/StudentDashboard";
import TeacherDashboard from "@/components/teacher/TeacherDashboard";
import AdminDashboard from "@/components/admin/AdminDashboard";
import { useRouter } from "next/navigation";

export default function Dashboard() {
  const { user, loadingAuth } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loadingAuth && !user) {
      router.push("/login");
    }
  }, [loadingAuth, user, router]);

  if (loadingAuth || !user) return null;

  if (user.role === "teacher") {
    return <TeacherDashboard />;
  } else if (user.role === "student") {
    return <StudentDashboard />;
  } else if (user.role === "admin") {
    return <AdminDashboard />;
  } else {
    return <div>Unknown user role</div>;
  }
}

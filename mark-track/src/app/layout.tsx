import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import {AuthProvider} from "@/context/AuthContext";
import { Toaster } from "react-hot-toast";
import { NotificationProvider } from '@/context/NotificationContext'

const geistSans = localFont({
  src: "../fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});
const geistMono = localFont({
  src: "../fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

export const metadata: Metadata = {
  title: "marktrack",
  description: "A simple app for tracking your marks",
  icons: "../../public/logo.svg",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <AuthProvider>
          <NotificationProvider>
            <main className="text-black">
              <Navbar/>
              {children}
              <Footer/>
              <Toaster position="top-right" />
            </main>
          </NotificationProvider>
        </AuthProvider>
      </body>
    </html>
  );
}

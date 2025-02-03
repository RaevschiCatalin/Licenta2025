'use client';

import Link from 'next/link'
import { useAuth } from '@/context/AuthContext'
import Image from "next/image";

export default function Navbar() {
    const { isLoggedIn, logout } = useAuth()

    return (
        <nav className="navbar navbar-no-boxShadow navbar-bordered navbar-sticky !bg-[#ffff] shadow-md">
            <div className="navbar-start">
                <Link href="/">
                    <Image
                        src="/logo.png"
                        alt="MarkTrack Logo"
                        width={158}
                        height={158}
                    />
                </Link>
            </div>
            {/* Regular navbar links visible on larger screens */}
            <ul className="navbar-end flex items-center gap-4 hidden md:flex">
                {isLoggedIn ? (
                    <>
                        <li className="navbar-item">
                            <Link href="/dashboard" className="text-[#2E2E2E] font-bold hover:text-[#4A90E2] transition-colors">
                                Dashboard
                            </Link>
                        </li>
                        <li className="navbar-item">
                            <Link href="/notifications" className="group">
                                <svg className="w-8 h-8 fill-transparent text-[#2E2E2E] group-hover:text-[#F5C200]" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
                                    <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 5.365V3m0 2.365a5.338 5.338 0 0 1 5.133 5.368v1.8c0 2.386 1.867 2.982 1.867 4.175 0 .593 0 1.292-.538 1.292H5.538C5 18 5 17.301 5 16.708c0-1.193 1.867-1.789 1.867-4.175v-1.8A5.338 5.338 0 0 1 12 5.365ZM8.733 18c.094.852.306 1.54.944 2.112a3.48 3.48 0 0 0 4.646 0c.638-.572 1.236-1.26 1.33-2.112h-6.92Z"/>
                                </svg>
                            </Link>
                        </li>
                        <li className="navbar-item">
                            <Link href="/profile" className="group">
                                <svg
                                    className="fill-current text-[#2E2E2E] group-hover:text-[#F5C200] transition-all"
                                    height="40" viewBox="0 0 32 32" width="40" xmlns="http://www.w3.org/2000/svg"
                                >
                                    {/* Outer Circle */}
                                    <path
                                        className="group-hover:fill-[#F5C200]"
                                        d="m16 8a5 5 0 1 0 5 5 5 5 0 0 0 -5-5zm0 8a3 3 0 1 1 3-3 3.0034 3.0034 0 0 1 -3 3z"
                                    />
                                    {/* Inner Details (Lines) */}
                                    <path
                                        className="group-hover:fill-blue-500"
                                        d="m16 2a14 14 0 1 0 14 14 14.0158 14.0158 0 0 0 -14-14zm-6 24.3765v-1.3765a3.0033 3.0033 0 0 1 3-3h6a3.0033 3.0033 0 0 1 3 3v1.3765a11.8989 11.8989 0 0 1 -12 0zm13.9925-1.4507a5.0016 5.0016 0 0 0 -4.9925-4.9258h-6a5.0016 5.0016 0 0 0 -4.9925 4.9258 12 12 0 1 1 15.985 0z"
                                    />
                                    {/* Invisible Background */}
                                    <path d="m0 0h32v32h-32z" fill="none"/>
                                </svg>
                            </Link>
                        </li>
                        <li className="navbar-item">
                            <button
                                className="btn btn-rounded bg-green-9 text-[#f2f2f2] font-bold hover:bg-[#F5C200] hover:text-black transition-colors"
                                onClick={logout}
                            >
                                Logout
                            </button>
                        </li>
                    </>
                ) : (
                    <>
                        <li className="navbar-item">
                            <Link href="/register"
                                  className="btn btn-rounded bg-green-9 text-white border-green-9 hover:bg-transparent hover:text-black hover:border-green-9 hover:border-2 font-bold transition-colors">
                                Register
                            </Link>
                        </li>
                        <li className="navbar-item">
                            <Link href="/login"
                                  className="btn btn-rounded bg-transparent text-green-9 border-green-9 border-2 hover:bg-green-9 hover:text-white hover:border-green-9 font-bold transition-colors">
                                Login
                            </Link>
                        </li>
                    </>
                )}
            </ul>

            {/* Dropdown for smaller screens */}
            <div className="md:hidden">
                <div className="dropdown">
                    <label className="btn btn-solid-primary my-2" tabIndex={0}>
                        <svg className="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
                            <path stroke="currentColor" strokeLinecap="round" strokeWidth="2" d="M5 7h14M5 12h14M5 17h14"/>
                        </svg>
                    </label>
                    <div className="dropdown-menu dropdown-menu-bottom-left">
                        {isLoggedIn ? (
                            <>
                                <Link href="/profile" className="dropdown-item text-sm">Profile</Link>
                                <Link href="/dashboard" className="dropdown-item text-sm">Dashboard</Link>
                                <Link href="/notifications" className='dropdown-item text-sm'>Notifications</Link>
                                <button onClick={logout} className="dropdown-item text-sm">Logout</button>
                                
                            </>
                        ) : (
                            <>
                                <Link href="/register" className="dropdown-item text-sm">Register</Link>
                                <Link href="/login" className="dropdown-item text-sm">Login</Link>
                            </>
                        )}
                    </div>
                </div>
            </div>
        </nav>
    );
}

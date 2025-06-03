'use client'

import { useState } from 'react';
import { useAuth } from '@/context/AuthContext';
import Link from 'next/link';
import { useRouter, useSearchParams } from 'next/navigation';
import { postRequest } from '@/context/api';

export default function Login() {
	const [email, setEmail] = useState('');
	const [password, setPassword] = useState('');
	const [error, setError] = useState('');
	const [loading, setLoading] = useState(false);
	const { login } = useAuth();
	const router = useRouter();
	const searchParams = useSearchParams();
	const message = searchParams.get('message');

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		setError('');
		setLoading(true);

		try {
			// Create URLSearchParams for form-urlencoded data
			const params = new URLSearchParams();
			params.append('username', email);
			params.append('password', password);

			const response = await postRequest('/auth/login', params, {
				headers: {
					'Content-Type': 'application/x-www-form-urlencoded'
				}
			});

			if (response.access_token) {
				const result = await login(response.access_token);
				console.log(result);
				
				if (result.success) {
					// Decode JWT token to get user status
					const token = response.access_token;
					const payload = JSON.parse(atob(token.split('.')[1]));
					const status = payload.status;
					
					// Handle different user statuses
					switch (status) {
						case 'incomplete':
							router.push('/enterCode');
							break;
						case 'awaiting_details':
							router.push('/completeDetails');
							break;
						case 'active':
							router.push('/dashboard');
							break;
						default:
							router.push('/dashboard');
					}
				} else {
					setError(result.message || 'Login failed');
				}
			} else {
				setError('Invalid response from server');
			}
		} catch (error: any) {
			console.error('Login error:', error);
			if (error.response?.data?.detail) {
				setError(error.response.data.detail);
			} else if (error instanceof Error) {
				setError(error.message || 'Login failed');
			} else {
				setError('An unexpected error occurred');
			}
		} finally {
			setLoading(false);
		}
	};

	return (
		<div className="min-h-screen flex items-center justify-center bg-gray-50">
			<div className="max-w-md w-full space-y-8 p-8 bg-white rounded-lg shadow">
				<div>
					<h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
						Sign in to your account
					</h2>
				</div>
				<form className="mt-8 space-y-6" onSubmit={handleSubmit}>
					<div className="rounded-md shadow-sm -space-y-px">
						<div>
							<label htmlFor="email" className="sr-only">
								Email address
							</label>
							<input
								id="email"
								name="email"
								type="email"
								autoComplete="email"
								required
								placeholder="Email address"
								className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 bg-[#f8f8f8] placeholder-gray-400 text-black focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm" 
								value={email}
								onChange={(e) => setEmail(e.target.value)}
								disabled={loading}
							/>
						</div>
						<div>
							<label htmlFor="password" className="sr-only">
								Password
							</label>
							<input
								id="password"
								name="password"
								type="password"
								autoComplete="current-password"
								required
								className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 bg-[#f8f8f8] placeholder-gray-400 text-black focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm" 
								placeholder="Password"
								value={password}
								onChange={(e) => setPassword(e.target.value)}
								disabled={loading}
							/>
						</div>
					</div>

					{message && (
						<div className="text-green-500 text-sm text-center">
							{message}
						</div>
					)}

					{error && (
						<div className="text-red-500 text-sm text-center">
							{error}
						</div>
					)}

					<div>
						<button
							type="submit"
							className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
							disabled={loading}
						>
							{loading ? 'Signing in...' : 'Sign in'}
						</button>
					</div>
				</form>

				<div className="text-sm text-center">
					<Link href="/register" className="font-medium text-indigo-600 hover:text-indigo-500">
						Don&apos;t have an account? Register
					</Link>
				</div>
			</div>
		</div>
	);
}

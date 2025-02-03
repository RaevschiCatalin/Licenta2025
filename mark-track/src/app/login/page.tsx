'use client'

import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';

export default function Login() {
	const [email, setEmail] = useState('');
	const [password, setPassword] = useState('');
	const [error, setError] = useState<string | null>(null);
	const router = useRouter();
	const { login } = useAuth();

	const onSubmit = async () => {
		setError(null);
		const result = await login(email, password);
		if (result.success) {
			router.push('/');
		} else {
			setError(result.message || "Login failed. Please try again.");
		}
	};

	return (
		<div className="flex justify-center items-center h-screen pb-10">
			<div className="mx-auto flex w-full max-w-sm flex-col  gap-6">
				<div className="flex flex-col items-center">
					<h1 className="text-3xl font-semibold">Sign In</h1>
					<p className="text-sm">Sign in to access your account</p>
				</div>
				<div className="form-group">
					<div className="form-field">
						<input
							placeholder="Email address"
							type="email"
							value={email}
							onChange={(e) => setEmail(e.target.value)}
							className="input input-block"
						/>
					</div>
					<div className="form-field">
						<input
							placeholder="Password"
							type="password"
							value={password}
							onChange={(e) => setPassword(e.target.value)}
							className="input input-block"
						/>
					</div>
					<div className="form-control justify-between">
						<div className="flex gap-2">
							<input type="checkbox" className="checkbox" />
							<a href="#">Remember me</a>
						</div>
						<label className="form-label">
							<Link href="/forgotPassword" className="link link-underline-hover link-primary text-sm">Forgot password?</Link>
						</label>
					</div>
					{error && <p className="text-red-500">{error}</p>}
					<button onClick={onSubmit} className="btn btn-primary w-full">
						Sign in
					</button>
					<Link href="/register" className='link link-underline-hover link-primary text-sm justify-center'>Don&apos;t have an account yet? Sign up.</Link>
				</div>
			</div>
		</div>
	);
}

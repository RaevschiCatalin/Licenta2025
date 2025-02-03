'use client';

import { useState } from "react";
import {postRequest} from "@/context/api";
import {FirebaseError} from "firebase/app";
import {useRouter} from "next/navigation";
import Loader from "@/components/Loader";

export default function EnterCode() {
    const [code, setCode] = useState<string>("");
    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const router = useRouter();

    const handleSubmit = async () => {
        const uid = localStorage.getItem("uid");

        if (!uid) {
            setError("No UID found. Please re-register.");
            return;
        }

        try {
             await postRequest("/roles/assign-role",{uid,code})
                console.log("all good")
                setError(null);
                setSuccess("The code is correct, redirecting you to the next step.");
                setLoading(true);
                setTimeout(()=>{
                    router.push("/completeDetails");
                    setLoading(false);
                },2000);


            }
        catch (error: unknown) {
            if (error instanceof FirebaseError) {
                setError(`Code Validation Failed: ${error.message}`);
            } else {
                setError("Unexpected error. Please try again.");
            }
        }
    };

    return (
        <div className="flex justify-center items-center h-screen pb-10">
            <div className="mx-auto flex w-full max-w-sm flex-col gap-6">
                <div className="flex flex-col items-center">
                    <h1 className="text-3xl font-semibold">Enter Code</h1>
                    <p className="text-sm">Enter the code you received from your institution</p>
                </div>
                <div className="form-group">
                    <div className="form-field">
                        <input
                            placeholder="Code"
                            type="text"
                            className="input input-block"
                            value={code}
                            onChange={(e) => setCode(e.target.value)}
                        />
                    </div>
                </div>
                <button className="btn btn-primary" onClick={handleSubmit}>
                    Submit
                </button>
                {error && <p className="text-red-500">{error}</p>}
                {success && <p className="text-green-500 mt-16">{success}</p>}
                {loading && <Loader/> }
            </div>
        </div>
    );
}

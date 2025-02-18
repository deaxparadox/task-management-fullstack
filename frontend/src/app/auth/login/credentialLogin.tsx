"use client";

import Message from "@/app/message";
import Link from "next/link";
import { redirect, useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";

export default function CredentialsLogin({ otp }: { otp: string | null }) {
    const [message, setMessage] = useState("")
    const [mesStatus, setMesStatus] = useState(false);

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const loginHandler = () => {
        const userData = JSON.stringify({
            username: username,
            password: password
        })

        console.log(userData);
        
        fetch(`http://localhost:8000/api/auth/login`, {
            method: "POST",
            body: userData,
            headers: {
                "Content-Type": "application/json"
            }
        }).then(
            async (res) => {
                if (res.status == 200) {
                    redirect("/dashboard")
                } else {
                    setMessage((await res.json()).message)
                }
            }
        )
    }

    return (
        <>
            <div className="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
                {mesStatus && <Message message="Message:" description={message} duration={3000}/>}

                <div className="sm:mx-auto sm:w-full sm:max-w-sm  bg-indigo-600 text-gray-100 rounded-md">
                    <h2 className="m-10 text-center text-2xl/9 font-bold tracking-tight">
                        Login
                    </h2>
                </div>

                <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm bg-gray-100 p-5 rounded-md">
                    <div className="space-y-6">
                        <div>
                            <label htmlFor="email" className="block text-sm/6 font-medium text-gray-900">
                                Username or Email
                            </label>
                            <div className="mt-2">
                                <input
                                    id="username"
                                    name="username"
                                    type="username"
                                    required
                                    autoComplete="username"
                                    onChange={e => setUsername(e.target.value)}
                                    className="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
                                />
                            </div>
                        </div>

                        <div>
                            <div className="flex items-center justify-between">
                                <label htmlFor="password" className="block text-sm/6 font-medium text-gray-900">
                                    Password
                                </label>
                                <div className="text-sm">
                                    <a href="#" className="font-semibold text-indigo-600 hover:text-indigo-500">
                                        Forgot password?
                                    </a>
                                </div>
                            </div>
                            <div className="mt-2">
                                <input
                                    id="password"
                                    name="password"
                                    type="password"
                                    required
                                    autoComplete="current-password"
                                    onChange={e => setPassword(e.target.value)}
                                    className="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
                                />
                            </div>
                        </div>

                        <div>
                            <button
                                type="button"
                                onClick={loginHandler}
                                className="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm/6 font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                            >
                                Sign in
                            </button>
                        </div>

                    </div>
                </div>
            </div>
        </>
    )
}
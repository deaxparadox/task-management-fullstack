"use client"

import { useState } from "react"
import Link from "next/link"
import { useSearchParams } from "next/navigation"

import Message from "@/app/message"
import Navbar from "@/app/navbar"






export default function Page() {
    const searchParams = useSearchParams();
    const otp = searchParams.get('otp')
    
    let url: string | null = "";
    if (otp === "yes") {
        url = `${process.env.NEXT_PUBLIC_BACKEND_SERVER}/api/auth/register?otp=yes`
    } else {
        url = `${process.env.NEXT_PUBLIC_BACKEND_SERVER}/api/auth/register?otp=`
    }

    let urlOtpStatus = false;

    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [role, setRole] = useState("");
    

    const clear_data = async () => {
        setUsername("");
        setEmail("");
        setPassword("");
        setRole("");
    }

    const handlerSubmit = async (e: any) => {
        e.preventDefault();
        if (!username || !email || !password || !role) {
            alert("All fields required.")
            return
        }

        const user_data = {
            "username": username,
            "email": email,
            "password": password,
            "role": Number(role)
        }
        const jsonsified_data = JSON.stringify(user_data);

        
        const rawResponse = await fetch(
            url, {
                method: "POST",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: jsonsified_data
            }
        )
        
        if (rawResponse.status == 201){
            const response = await rawResponse.json()
            alert(response.message)
        } else {
            const response = await rawResponse.json()
            alert(`Oops :) ${response.message}`)
        }

        clear_data()
    }
    

    return (
        <>
            <Navbar login={true} />
            <div id="message-container">
                <Message message="Something" description="Something has happend somewhere"  duration={3000}/>
            </div>

            <div className="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
                <div className="sm:mx-auto sm:w-full sm:max-w-sm  bg-indigo-600 text-gray-100 rounded-md">
                    <h2 className="m-10 text-center text-2xl/9 font-bold tracking-tight">
                        Register your account
                    </h2>
                </div>

                <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm bg-gray-100 p-5 rounded-md">
                    <div className="space-y-6">
                        <div>
                            <label htmlFor="email" className="block text-sm/6 font-medium text-gray-900">
                                Username
                            </label>
                            <div className="mt-2">
                                <input
                                    id="email"
                                    name="email"
                                    type="text"
                                    required
                                    value={username}
                                    autoComplete="email"
                                    onChange={(e) => {setUsername(e.target.value)}}
                                    className="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
                                />
                            </div>
                        </div>
                        
                        <div>
                            <label htmlFor="email" className="block text-sm/6 font-medium text-gray-900">
                                Email address
                            </label>
                            <div className="mt-2">
                                <input
                                    id="email"
                                    name="email"
                                    type="email"
                                    required
                                    autoComplete="email"
                                    value={email}
                                    onChange={(e) => {setEmail(e.target.value)}}
                                    className="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
                                />
                            </div>
                        </div>

                        <div>
                            <div className="flex items-center justify-between">
                                <label htmlFor="password" className="block text-sm/6 font-medium text-gray-900">
                                    Password
                                </label>
                            </div>
                            <div className="mt-2">
                                <input
                                    id="password"
                                    name="password"
                                    type="password"
                                    value={password}
                                    required
                                    autoComplete="current-password"
                                    onChange={(e) => {setPassword(e.target.value)}}
                                    className="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
                                />
                            </div>
                        </div>

                        <div className="flex">
                            <div className="flex items-center">
                                <label htmlFor="Select role" className="mx-3 block text-sm/6 font-medium text-gray-900">Select user role</label>
                                <select className="" name="Role" id="role" value={role} onChange={(e) => setRole(e.target.value)} required>
                                    <option value="">Select</option>
                                    <option value="1">Employee</option>
                                    <option value="2">Team lead</option>
                                    <option value="3">Manager</option>
                                </select>
                            </div>
                        </div>

                        <div>
                            <button
                                onClick={handlerSubmit}
                                type="button"
                                className="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm/6 font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                            >
                                Register
                            </button>
                        </div>
                    </div>
                    <p className="mt-10 text-center text-sm/6 text-gray-500">
                        { 
                            otp == "yes"
                            &&
                            <Link href="/auth/register" className="font-semibold text-indigo-600 hover:text-indigo-500">
                                Standard login    
                            </Link>
                        }
                        { 
                            otp == null
                            &&
                            <Link href="/auth/register?otp=yes" className="font-semibold text-indigo-600 hover:text-indigo-500">
                                Click here login via OTP    
                            </Link>
                        }
                    </p>
                </div>
            </div>
        </>
    )
}

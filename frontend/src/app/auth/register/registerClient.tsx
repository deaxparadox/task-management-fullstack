"use client"

import { useState } from "react";
import Link from "next/link";
import { redirect, useSearchParams } from "next/navigation";

import { Dialog, DialogBackdrop, DialogPanel, DialogTitle } from '@headlessui/react';
import { ChevronDownIcon } from '@heroicons/react/16/solid';
import { ExclamationTriangleIcon } from '@heroicons/react/24/outline';

import Message from "@/app/message";
import { MessageResponseType } from "@/lib/message";


const DisplayMessage = ({ messages }: { messages: Array<MessageResponseType> }) => {
    return (
        <div>
            {messages.map(e => {
                return <Message message="Message " description={e.message} duration={3000} />
            })}
        </div>
    )

}

export default function RegisterClient() {
    const searchParams = useSearchParams();
    const otp = searchParams.get('otp');

    const [open, setOpen] = useState(false);
    const [userotp, setUserotp] = useState<string | undefined>(undefined);
    const [messages, setMessages] = useState<Array<MessageResponseType>>([]);
    const [otpVerified, setOtpVerified] = useState(false);
    const [otpNotVerified, setOtpNotVerified] = useState(false);
    const [otpExpired, setOtpExpired] = useState(false);
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [role, setRole] = useState("");
    const [activationId, setActivationId] = useState("");


    let url: string | null = "";
    if (otp === "yes") {
        url = `${process.env.NEXT_PUBLIC_BACKEND_SERVER}/api/auth/register?otp=yes`
    } else {
        url = `${process.env.NEXT_PUBLIC_BACKEND_SERVER}/api/auth/register?otp=`
    }

    const urlOtpVerify = `http://localhost:8000/api/auth/otp/${activationId}`


    const handleSubmitOtpVerify = async () => {

        setOtpExpired(false);
        setOtpNotVerified(false);
        setOtpVerified(false);

        const f = await fetch(urlOtpVerify, {
            method: "POST",
            body: JSON.stringify({
                "otp": userotp
            }),
            headers: {
                "Content-Type": "application/json"
            }
        })

        if (f.status === 202) {
            messages.push(await f.json());
            setOtpVerified(!otpVerified);
            setTimeout(() => {
                redirect("/auth/login")
            }, 2000)
        } else if (f.status === 403) {
            setOtpExpired(!otpExpired);
            messages.push(await f.json());
        } else if (f.status === 404) {
            setOtpNotVerified(!otpNotVerified);
            messages.push(await f.json());
        } else {
            messages.push(await f.json());
        }
    }

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
                'Content-Type': 'application/json'
            },
            body: jsonsified_data
        }
        )

        if (otp == "yes") {
            if (rawResponse.status == 201) {
                const response = await rawResponse.json()
                messages.push(response)
                setActivationId(response.activationid)
            } else {
                const response = await rawResponse.json()
                messages.push(response)
            }
            setOpen(true);
        } else {
            if (rawResponse.status == 201) {
                const response = await rawResponse.json()
                messages.push(response)
            } else {
                const response = await rawResponse.json()
                messages.push(response.message)
            }
        }

        clear_data()
    }


    return (
        <>
            <Dialog open={open} onClose={setOpen} className="relative z-10">
                <DialogBackdrop
                    transition
                    className="fixed inset-0 bg-gray-500/75 transition-opacity data-closed:opacity-0 data-enter:duration-300 data-enter:ease-out data-leave:duration-200 data-leave:ease-in"
                />

                <div className="fixed inset-0 z-10 w-screen overflow-y-auto">
                    <div className="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
                        <DialogPanel
                            transition
                            className="relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all data-closed:translate-y-4 data-closed:opacity-0 data-enter:duration-300 data-enter:ease-out data-leave:duration-200 data-leave:ease-in sm:my-8 sm:w-full sm:max-w-lg data-closed:sm:translate-y-0 data-closed:sm:scale-95"
                        >
                            <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                                <div className="sm:flex sm:items-start">
                                    <div className="mx-auto flex size-12 shrink-0 items-center justify-center rounded-full bg-red-100 sm:mx-0 sm:size-10">
                                        <ExclamationTriangleIcon aria-hidden="true" className="size-6 text-red-600" />
                                    </div>
                                    <div className="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
                                        <DialogTitle as="h3" className="text-base font-semibold text-gray-900">
                                            Verify OTP
                                        </DialogTitle>
                                        <div className="mt-2">
                                            <div className="flex items-center rounded-md bg-white pl-3 outline-1 -outline-offset-1 outline-gray-300 has-[input:focus-within]:outline-2 has-[input:focus-within]:-outline-offset-2 has-[input:focus-within]:outline-indigo-600">
                                                <input
                                                    id="otp-input"
                                                    name="otp-input"
                                                    type="text"
                                                    placeholder="Enter your OTP"
                                                    onChange={e => setUserotp(e.target.value)}
                                                    className="block min-w-0 grow py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6 bg-gray-100 rounded-md"
                                                />
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div className="bg-gray-50 px-4 py-3 sm:flex sm:flex-row sm:px-6 flex justify-between">
                                <div className="mt-3">
                                    <h3 className="text-green-900">
                                        {otpVerified && "OTP verified successfully"}
                                        {otpNotVerified && "Incorrect OTP"}
                                        {otpExpired && "OTP expired"}
                                    </h3>
                                </div>
                                <button
                                    type="button"
                                    data-autofocus
                                    onClick={handleSubmitOtpVerify}
                                    className="mt-3  rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 ring-1 shadow-xs ring-gray-300 ring-inset hover:bg-gray-50 sm:mt-0 sm:w-auto"
                                >
                                    Verify
                                </button>
                            </div>
                        </DialogPanel>
                    </div>
                </div>
            </Dialog>

            <div className="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
                {messages.length > 0 && <DisplayMessage messages={messages} />}

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
                                    id="username"
                                    name="email"
                                    type="text"
                                    required
                                    value={username}
                                    autoComplete="email"
                                    onChange={(e) => { setUsername(e.target.value) }}
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
                                    onChange={(e) => { setEmail(e.target.value) }}
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
                                    onChange={(e) => { setPassword(e.target.value) }}
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
                                Credentials registration
                            </Link>
                        }
                        {
                            otp == null
                            &&
                            <Link href="/auth/register?otp=yes" className="font-semibold text-indigo-600 hover:text-indigo-500">
                                Click here to register via OTP
                            </Link>
                        }
                    </p>
                </div>
            </div>
        </>
    )
}

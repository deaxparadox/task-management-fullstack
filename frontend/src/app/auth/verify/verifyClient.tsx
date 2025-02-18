"use client"

import { useEffect, useState } from "react";
import { redirect, useSearchParams } from "next/navigation"

import Message from "@/app/message";
import { MessageResponseType } from "@/lib/message";
import Link from "next/link";

const VerifyClient = () => {
    const searchParams = useSearchParams();
    const activationid = searchParams.get("activationid");
    const username = searchParams.get("username");
    const [activationResponse, setActivationResponse] = useState<MessageResponseType>()
    const [activationStatus, setActivationStatus] = useState(false);
    const [duration, setDuration] = useState<number>(3000);
    
    
    useEffect(() => {
        fetch(
            `${process.env.NEXT_PUBLIC_BACKEND_SERVER}/api/auth/register/${username}/${activationid}`, {
                method: "GET"
            },
        ).then(async response => {
            if (response.status == 200) {
                const response_data = await response.json()
                setActivationStatus(true)
                setActivationResponse(response_data);
            }
            if (response.status == 400) {
                const response_data = await response.json()
                setActivationStatus(true)
                setActivationResponse(response_data)
            }
        })

        
    }, [duration])

    return (
        <div className="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
            {activationStatus && <Message message="Message " description={activationResponse?.message}  duration={30000}/>}
            <Link className="p-5 bg-gray-100 text-green-700" href="/auth/login">Click here to login</Link>
        </div>
    )
}

export default VerifyClient;
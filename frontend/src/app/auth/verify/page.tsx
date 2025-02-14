"use client"

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation"

import Navbar from "@/app/navbar"
import Message from "@/app/message";

interface ResponseType {
    message: string
}

export default function Page() {
    const searchParams = useSearchParams();
    const activationid = searchParams.get("activationid");
    const [activationResponse, setActivationResponse] = useState<ResponseType>()
    const [activationStatus, setActivationStatus] = useState(false);
    const username = searchParams.get("username");


    useEffect(() => {
        fetch(
            `${process.env.NEXT_PUBLIC_BACKEND_SERVER}/api/auth/register/${username}/${activationid}`, 
            {
                method: "GET",
            },
        ).then(async response => {
            console.log(response.headers)
            console.log(await response.json());
        })
        // .then((data) => {
        //     setActivationStatus(true);
        //     console.log(data);
        //     setActivationResponse(data!);
        // })
    }, [])

    return (
        <div>
            <Navbar />
            {activationStatus && <Message message="Message" description={activationResponse?.message}  duration={3000}/>}
        </div>
    )
}
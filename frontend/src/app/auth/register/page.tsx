import { Dialog, DialogBackdrop, DialogPanel, DialogTitle } from '@headlessui/react'
import { ExclamationTriangleIcon } from '@heroicons/react/24/outline'

import Navbar from "@/app/navbar"
import RegisterClient from "./registerClient"


export default function Page() {
    return (
        <>
            <Navbar login={true} />
            <RegisterClient />
        </>
    )
}

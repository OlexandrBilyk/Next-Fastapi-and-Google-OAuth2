'use client'

import { useProfileQuery } from "@/redux/auth/authApi"
import { useLazyLogoutQuery } from "@/redux/auth/authApi"
import { useRouter } from "next/navigation"

export default function Profile() {
    const { data, error } = useProfileQuery(undefined)
    const [logout] = useLazyLogoutQuery()
    const router = useRouter()

    if (error) throw error

    const handleLogout = async function() {
        try {
            await logout()
            router.replace('/')
        } catch (err) {
            console.log(err);
        }
    }

    return (
        <>
            <p>{data?.username}</p>
            <p>{data?.email}</p>

            <button type="button" onClick={handleLogout}>logout</button>
        </>
    )
}
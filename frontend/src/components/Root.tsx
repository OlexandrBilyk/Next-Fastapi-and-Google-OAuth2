'use client'

import { useRouter } from "next/navigation"
import { useEffect } from "react"
import { useLazyProfileQuery, useRefreshMutation } from "@/redux/auth/authApi"

export default function Root() {
    const router = useRouter()
    const [getProfile] = useLazyProfileQuery()
    const [getRefresh] = useRefreshMutation()

    useEffect(() => {
        const initAuth = async function () {
            try {
                const profile = getProfile()

                router.replace('/profile')
            } catch (err) {
                try {
                    await getRefresh()

                    router.replace('/profile')
                } catch (error) {
                    router.push('/')
                }

            }
        }

        initAuth()
    }, [])

    return (
        <>
            <p>root</p>
            <button type="button" onClick={() => router.push('/auth')}>login</button>
        </>
    )
}
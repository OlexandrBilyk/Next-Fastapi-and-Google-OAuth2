'use client'

export default function AuthError({
    error,
    reset,
}: {
    error: Error & { digest?: string }
    reset: () => void
}) {
    return (
        <>
            <p>{error.message}</p>
            <button onClick={reset}>Try again</button>
        </>
    )
}
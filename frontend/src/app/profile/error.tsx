'use client'

export default function ProfileError({
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
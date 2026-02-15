'use client'
export default function Auth() {
    const handleAuth = async function () {
        try {
            window.location.href = 'http://localhost:8000/auth/google/login'
        } catch (err) {
            console.log(err);

        }
    }

    return (
        <button onClick={handleAuth}>Увійти з гугла</button>
    )
}
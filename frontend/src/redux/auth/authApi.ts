import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

interface User { 
    id: number,
    username: string,
    email: string,
}

export const authApi = createApi({
    reducerPath: 'auth',
    baseQuery: fetchBaseQuery({
        baseUrl: 'http://localhost:8000/',
        credentials: 'include',
    }),
    endpoints: (builder) => ({
        logout: builder.query<void, void>({
            query: () => '/auth/logout/'
        }),
        refresh: builder.mutation<void, void>({
            query: () => ({
                url: '/auth/refresh/',
                method: 'POST'
            })
        }),
        profile: builder.query<User, void>({
            query: () => '/profile'
        })
    })
})

export const {useLazyLogoutQuery, useRefreshMutation, useProfileQuery, useLazyProfileQuery} = authApi
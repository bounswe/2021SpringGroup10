package com.example.mvvmapp.data.repositories

import com.example.mvvmapp.data.network.MyApi
import com.example.mvvmapp.data.network.responses.AuthResponse
import retrofit2.Response


// This repository communicates with backend API
class UserRepository {

    suspend fun userLogin(email: String, password: String) : Response<AuthResponse> {
        return MyApi().userLogin(email, password)
    }

}
package com.example.mvvmapp.data.repositories

import com.example.mvvmapp.data.network.MyApi
import com.example.mvvmapp.data.network.SafeApiRequest
import com.example.mvvmapp.data.network.responses.AuthResponse
import retrofit2.Response


// This repository communicates with backend API
class UserRepository : SafeApiRequest() {

    suspend fun userLogin(email: String, password: String) : AuthResponse {
        return apiRequest { MyApi().userLogin(email, password) }
    }

}
package com.example.mvvmapp.data.repositories

import com.example.mvvmapp.data.db.AppDatabase
import com.example.mvvmapp.data.db.entities.User
import com.example.mvvmapp.data.network.MyApi
import com.example.mvvmapp.data.network.SafeApiRequest
import com.example.mvvmapp.data.network.responses.SignInResponse
import com.example.mvvmapp.data.network.responses.SignUpResponse


// This repository communicates with backend API
class UserRepository(
    private val api: MyApi,
    private val db: AppDatabase
) : SafeApiRequest() {

    suspend fun userLogin(username: String, password: String) : SignInResponse {
        return apiRequest { api.userLogin(username, password) }
    }

    suspend fun userSignup(
        username: String,
        email: String,
        password: String
    ) : SignUpResponse {
        return apiRequest { api.userSignup(username, email, password) }
    }

    suspend fun saveUser(user: User) = db.getUserDao().insertOrUpdate(user)

    fun getUser() = db.getUserDao().getUser()

}
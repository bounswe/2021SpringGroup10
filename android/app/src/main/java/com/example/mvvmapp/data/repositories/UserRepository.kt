package com.example.mvvmapp.data.repositories

import com.example.mvvmapp.data.db.AppDatabase
import com.example.mvvmapp.data.db.entities.User
import com.example.mvvmapp.data.network.MyApi
import com.example.mvvmapp.data.network.SafeApiRequest
import com.example.mvvmapp.data.network.responses.AuthResponse
import retrofit2.Response


// This repository communicates with backend API
class UserRepository(
    private val api: MyApi,
    private val db: AppDatabase
) : SafeApiRequest() {

    suspend fun userLogin(email: String, password: String) : AuthResponse {
        return apiRequest { api.userLogin(email, password) }
    }

    suspend fun saveUser(user: User) = db.getUserDao().insertOrUpdate(user)

    fun getUser() = db.getUserDao().getUser()

}
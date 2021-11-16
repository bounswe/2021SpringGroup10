package com.example.mvvmapp.data.repositories

import android.util.Log
import com.example.mvvmapp.data.db.AppDatabase
import com.example.mvvmapp.data.db.entities.Profile
import com.example.mvvmapp.data.db.entities.User
import com.example.mvvmapp.data.network.MyApi
import com.example.mvvmapp.data.network.SafeApiRequest
import com.example.mvvmapp.data.network.requests.SignInRequest
import com.example.mvvmapp.data.network.requests.SignUpRequest
import com.example.mvvmapp.data.network.responses.SignInResponse
import com.example.mvvmapp.data.network.responses.SignUpResponse
import com.google.gson.JsonObject
import org.json.JSONObject


// This repository communicates with backend API
class UserRepository(
    private val api: MyApi,
    private val db: AppDatabase
) : SafeApiRequest() {

    suspend fun userLogin(username: String, password: String) : SignInResponse {
        return apiRequest {
            val req = SignInRequest(username, password)
            api.userLogin(req)
        }
    }

    suspend fun userSignup(
        username: String,
        email: String,
        password: String
    ) : SignUpResponse {
        return apiRequest {
            val req = SignUpRequest(username, email, password)
            api.userSignup(req)
        }
    }

    suspend fun saveUser(user: User) = db.getUserDao().insertOrUpdate(user)

    fun getUser() = db.getUserDao().getUser()

    suspend fun saveProfile(profile: Profile) = db.getProfileDao().insertOrUpdate(profile)

    fun getProfile() = db.getProfileDao().getProfile()

}
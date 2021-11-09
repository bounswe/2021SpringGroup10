package com.example.mvvmapp.data.network.responses

import com.example.mvvmapp.data.db.entities.User

// TODO(this fields will be updated according to the backend!)
data class AuthResponse(
    val isSuccessful: Boolean?,
    val message: String?,
    val user: User?
)
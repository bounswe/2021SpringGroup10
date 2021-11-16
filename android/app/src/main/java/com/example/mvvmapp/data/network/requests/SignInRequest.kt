package com.example.mvvmapp.data.network.requests

import com.google.gson.annotations.SerializedName

data class SignInRequest(
    @SerializedName("user_name")
    val user_name: String,
    @SerializedName("password")
    val password: String
)
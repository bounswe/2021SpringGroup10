package com.example.mvvmapp.data.network.requests

import com.google.gson.annotations.SerializedName

data class SignUpRequest (
    @SerializedName("user_name")
    val user_name: String,
    @SerializedName("mail_address")
    val mail_address: String,
    @SerializedName("password")
    val password: String
)
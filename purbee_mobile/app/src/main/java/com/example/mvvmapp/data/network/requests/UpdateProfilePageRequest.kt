package com.example.mvvmapp.data.network.requests
import com.google.gson.annotations.SerializedName

data class UpdateProfilePageRequest (
    @SerializedName("user_name")
    val user_name: String,
    @SerializedName("profile_photo")
    val profile_photo: String,
    @SerializedName("bio")
    val bio: String,
    @SerializedName("firs_name")
    val first_name: String,
    @SerializedName("last_name")
    val last_name: String,
    @SerializedName("birth_date")
    val birth_date: String,
)
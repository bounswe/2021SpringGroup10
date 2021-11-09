package com.example.mvvmapp.data.network

import com.example.mvvmapp.data.network.responses.AuthResponse
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.Field
import retrofit2.http.FormUrlEncoded
import retrofit2.http.POST

interface MyApi {

    // TODO(Field annotations are for http request keys. They must match)

    @FormUrlEncoded
    @POST("login") // "login" is endpoint we add to root url
    suspend fun userLogin(
        @Field("login") email: String,
        @Field("password") password: String
    ) : Response<AuthResponse>

    // TODO(fix the base url according to backend API)
    companion object {
        operator fun invoke() : MyApi {
            return Retrofit.Builder()
                .baseUrl("https://xxxx.backendless.app/api/users/")
                .addConverterFactory(GsonConverterFactory.create())
                .build()
                .create(MyApi::class.java)
        }
    }
}
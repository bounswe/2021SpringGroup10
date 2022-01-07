package com.example.mvvmapp.data.network

import com.example.mvvmapp.data.network.requests.GetProfileInfoRequest
import com.example.mvvmapp.data.network.requests.SignInRequest
import com.example.mvvmapp.data.network.requests.SignUpRequest
import com.example.mvvmapp.data.network.requests.UpdateProfilePageRequest
import com.example.mvvmapp.data.network.responses.*
import com.google.gson.JsonObject
import okhttp3.OkHttpClient
import okhttp3.RequestBody
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.*
import java.util.concurrent.TimeUnit

interface MyApi {


    @POST("sign_in/")
    suspend fun userLogin(
        @Body req: SignInRequest
    ) : Response<SignInResponse>


    @POST("sign_up/")
    suspend fun userSignup(
        @Body req: SignUpRequest
    ) : Response<SignUpResponse>

    @POST("profile_page/")
    suspend fun updateProfilePage(
        @Body req: UpdateProfilePageRequest
    ) : Response<UpdateProfilePageResponse>

    @GET("profile_page/")
    suspend fun updateProfilePageGet(
        @Body req: GetProfileInfoRequest
    ) : Response<GetProfileInfoResponse>

    @GET("quotes")
    suspend fun getQuotes() : Response<QuotesResponse>

    companion object {
        operator fun invoke(
            networkConnectionInterceptor: NetworkConnectionInterceptor
        ) : MyApi {

            val okHttpClient = OkHttpClient.Builder()
                .connectTimeout(10, TimeUnit.SECONDS)
                .readTimeout(10, TimeUnit.SECONDS)
                .writeTimeout(10, TimeUnit.SECONDS)
                .addInterceptor(networkConnectionInterceptor)
                .build()


            return Retrofit.Builder()
                .client(okHttpClient)
                .baseUrl("http://3.134.93.99:8080/api/")
                .addConverterFactory(GsonConverterFactory.create())
                .build()
                .create(MyApi::class.java)
        }
    }
}
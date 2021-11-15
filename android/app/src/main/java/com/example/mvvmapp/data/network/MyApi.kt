package com.example.mvvmapp.data.network

import com.example.mvvmapp.data.network.responses.QuotesResponse
import com.example.mvvmapp.data.network.responses.SignInResponse
import com.example.mvvmapp.data.network.responses.SignUpResponse
import okhttp3.OkHttpClient
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.Field
import retrofit2.http.FormUrlEncoded
import retrofit2.http.GET
import retrofit2.http.POST
import java.util.concurrent.TimeUnit

interface MyApi {


    @FormUrlEncoded
    @POST("sign_in/") // "login" is endpoint we add to root url
    suspend fun userLogin(
        @Field("user_name") username: String,
        @Field("password") password: String
    ) : Response<SignInResponse>


    @FormUrlEncoded
    @POST("sign_up/")
    suspend fun userSignup(
        @Field("user_name") username: String,
        @Field("mail_address") email: String,
        @Field("password") password: String
    ) : Response<SignUpResponse>

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
                .baseUrl("http://3.134.93.99/api/")
                .addConverterFactory(GsonConverterFactory.create())
                .build()
                .create(MyApi::class.java)
        }
    }
}
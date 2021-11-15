package com.example.mvvmapp.data.network

import android.util.Log
import com.example.mvvmapp.util.ApiException
import com.example.mvvmapp.util.NoInternetException
import com.example.mvvmapp.util.hide
import com.example.mvvmapp.util.snackbar
import com.google.gson.JsonObject
import org.json.JSONException
import org.json.JSONObject
import retrofit2.Response
import java.lang.StringBuilder

abstract class SafeApiRequest {

    suspend fun<T: Any> apiRequest(call: suspend () -> Response<T>): T {

        try {
            val response = call.invoke()

            if (response.isSuccessful) {
                return response.body()!!
            }
            else {
                val error = response.errorBody()?.string()
                val message = StringBuilder()
                error?.let{
                    try {
                        message.append(JSONObject(it).getString("response_message"))
                    }
                    catch (e: JSONException) { }
                    message.append("\n")
                }

                message.append("Error Code: ${response.code()}")

                throw ApiException(message.toString())
            }
        }
        catch (e: NoInternetException) {
            throw NoInternetException("Connection error. Check your internet connection.")
        }
        catch (e: Exception) {
            throw ApiException("Server is down. Please try again later.")
        }

    }
}
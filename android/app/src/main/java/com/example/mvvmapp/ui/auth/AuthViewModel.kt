package com.example.mvvmapp.ui.auth

import android.content.Intent
import android.view.View
import androidx.lifecycle.ViewModel
import com.example.mvvmapp.data.db.entities.User
import com.example.mvvmapp.data.network.NetworkConnectionInterceptor
import com.example.mvvmapp.data.repositories.UserRepository
import com.example.mvvmapp.util.ApiException
import com.example.mvvmapp.util.Coroutines
import com.example.mvvmapp.util.NoInternetException
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class AuthViewModel(
    private val repository: UserRepository
) : ViewModel() {


    fun getLoggedInUser() = repository.getUser()


    // We use withContext(Dispatchers.IO) to make our network calls in
    // IO dispatcher instead of the main dispatcher

    suspend fun userLogin(
        username: String,
        password: String
    ) = withContext(Dispatchers.IO) { repository.userLogin(username, password) }

    suspend fun userSignup(
        username: String,
        email: String,
        password: String
    ) = withContext(Dispatchers.IO) { repository.userSignup(username, email, password) }

    suspend fun saveLoggedInUser(user: User) = repository.saveUser(user)

}
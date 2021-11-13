package com.example.mvvmapp.ui.auth

import android.content.Intent
import android.view.View
import androidx.lifecycle.ViewModel
import com.example.mvvmapp.data.network.NetworkConnectionInterceptor
import com.example.mvvmapp.data.repositories.UserRepository
import com.example.mvvmapp.util.ApiException
import com.example.mvvmapp.util.Coroutines
import com.example.mvvmapp.util.NoInternetException

class AuthViewModel(
    private val repository: UserRepository
) : ViewModel() {

    var name: String? = null
    var email: String? = null
    var password: String? = null
    var passwordconfirm: String? = null

    var authListener: AuthListener? = null

    fun getLoggedInUser() = repository.getUser()

    fun onLoginButtonClick(view: View) {
        authListener?.onStarted()

        if (email.isNullOrEmpty() || password.isNullOrEmpty()) {
            authListener?.onFailure("Invalid email or password")
            return
        }

        Coroutines.main {
            try{
                val authResponse = repository.userLogin(email!!, password!!)
                authResponse.user?.let {
                    authListener?.onSuccess(it)
                    repository.saveUser(it)
                    return@main
                }
                authListener?.onFailure(authResponse.message!!)
            }
            catch (e: ApiException) {
                authListener?.onFailure(e.message!!)
            }
            catch (e: NoInternetException) {
                authListener?.onFailure(e.message!!)
            }

        }

    }

    fun onSignup(view: View) {
        Intent(view.context, SignupActivity::class.java).also {
            view.context.startActivity(it)
        }
    }

    fun onLogin(view: View) {
        Intent(view.context, LoginActivity::class.java).also {
            view.context.startActivity(it)
        }
    }

    fun onSignupButtonClick(view: View) {
        authListener?.onStarted()

        if(name.isNullOrEmpty()) {
            authListener?.onFailure("Name is required")
            return
        }

        if (email.isNullOrEmpty()) {
            authListener?.onFailure("Email is required")
            return
        }

        if(password.isNullOrEmpty()) {
            authListener?.onFailure("Please enter a password")
            return
        }

        if(password != passwordconfirm) {
            authListener?.onFailure("Passwords do not match")
            return
        }

        Coroutines.main {
            try{
                val authResponse = repository.userSignup(name!!, email!!, password!!)
                authResponse.user?.let {
                    authListener?.onSuccess(it)
                    repository.saveUser(it)
                    return@main
                }
                authListener?.onFailure(authResponse.message!!)
            }
            catch (e: ApiException) {
                authListener?.onFailure(e.message!!)
            }
            catch (e: NoInternetException) {
                authListener?.onFailure(e.message!!)
            }

        }

    }
}
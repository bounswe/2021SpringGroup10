package com.example.mvvmapp.ui.auth

import com.example.mvvmapp.util.snackbar

object Validator {

    fun validateUserSignUp(
        username: String,
        password: String,
        email: String,
        passwordConfirm: String
    ): Boolean {
        when {
            username.isEmpty() -> {
                return false
            }

            email.isEmpty() -> {
                return false
            }

            password.isEmpty() -> {
                return false
            }

            password != passwordConfirm -> {
                return false
            }

        }

        return true
    }


    fun validateUserLogin(
        username: String,
        password: String
    ):Boolean {
        when {
            username.isEmpty() -> {
                return false
            }

            password.isEmpty() -> {
                return false
            }
        }

        return true
    }

}
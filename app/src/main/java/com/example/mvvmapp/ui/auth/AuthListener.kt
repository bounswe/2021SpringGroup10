package com.example.mvvmapp.ui.auth

interface AuthListener {
    fun onStarted()
    fun onSuccess()
    fun onFailure(message: String)
}
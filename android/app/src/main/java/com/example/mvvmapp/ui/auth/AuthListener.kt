package com.example.mvvmapp.ui.auth

import com.example.mvvmapp.data.db.entities.User

interface AuthListener {
    fun onStarted()
    fun onSuccess(user: User)
    fun onFailure(message: String)
}
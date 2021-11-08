package com.example.mvvmapp.ui.auth

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import androidx.databinding.DataBindingUtil
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProviders
import com.example.mvvmapp.R
import com.example.mvvmapp.databinding.ActivityLoginBinding
import com.example.mvvmapp.util.toast

class LoginActivity : AppCompatActivity(), AuthListener {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val binding: ActivityLoginBinding = DataBindingUtil.setContentView(this, R.layout.activity_login)

        val viewModel = ViewModelProviders.of(this).get(AuthViewModel::class.java)

        binding.viewmodel = viewModel

        viewModel.authListener = this
    }

    override fun onStarted() {
        toast("Login Started")
    }

    override fun onSuccess() {
        toast("Login Success")
    }

    override fun onFailure(message: String) {
        toast(message)
    }
}
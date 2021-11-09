package com.example.mvvmapp.ui.auth

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import androidx.databinding.DataBindingUtil
import androidx.lifecycle.LiveData
import androidx.lifecycle.Observer
import androidx.lifecycle.ViewModelProviders
import com.example.mvvmapp.R
import com.example.mvvmapp.data.db.entities.User
import com.example.mvvmapp.databinding.ActivityLoginBinding
import com.example.mvvmapp.util.hide
import com.example.mvvmapp.util.show
import com.example.mvvmapp.util.toast

class LoginActivity : AppCompatActivity(), AuthListener {
    lateinit var binding: ActivityLoginBinding
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding = DataBindingUtil.setContentView(this, R.layout.activity_login)

        val viewModel = ViewModelProviders.of(this).get(AuthViewModel::class.java)

        binding.viewmodel = viewModel

        viewModel.authListener = this
    }

    override fun onStarted() {
        binding.progressBar.show()
    }

    override fun onSuccess(user: User) {
        binding.progressBar.hide()
        toast("${user.name} is Logged In")
    }

    override fun onFailure(message: String) {
        binding.progressBar.hide()
        toast(message)
    }
}
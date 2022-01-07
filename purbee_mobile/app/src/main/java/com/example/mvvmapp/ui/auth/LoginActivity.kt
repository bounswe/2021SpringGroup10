package com.example.mvvmapp.ui.auth

import android.content.Intent
import android.os.Bundle
import android.util.Log
import androidx.appcompat.app.AppCompatActivity
import androidx.databinding.DataBindingUtil
import androidx.lifecycle.Observer
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.lifecycleScope
import com.example.mvvmapp.R
import com.example.mvvmapp.data.db.entities.User
import com.example.mvvmapp.databinding.ActivityLoginBinding
import com.example.mvvmapp.ui.home.NavigationActivity
import com.example.mvvmapp.util.*
import kotlinx.coroutines.launch
import org.kodein.di.KodeinAware
import org.kodein.di.android.kodein
import org.kodein.di.generic.instance

class LoginActivity : AppCompatActivity(), KodeinAware {

    override val kodein by kodein()

    private val factory : AuthViewModelFactory by instance()

    private lateinit var binding: ActivityLoginBinding
    private lateinit var viewModel: AuthViewModel

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding = DataBindingUtil.setContentView(this, R.layout.activity_login)

        viewModel = ViewModelProvider(this, factory)[AuthViewModel::class.java]


        viewModel.getLoggedInUser().observe(this, Observer { user ->
            if(user != null) {
                Intent(this, NavigationActivity::class.java).also {
                    // set flags to create a fresh activity.
                    // for example if we don't do this the user will see
                    // login activity when they click back button even though
                    // they are logged in
                    it.flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
                    startActivity(it)
                }
            }
        })

        binding.buttonSignIn.setOnClickListener {
            loginUser()
        }

        binding.textViewSignUp.setOnClickListener {
            startActivity(Intent(this, SignupActivity::class.java))
        }
    }

    private fun loginUser() {
        val username = binding.editTextUsername.text.toString().trim()
        val password = binding.editTextPassword.text.toString().trim()

        when {
            username.isEmpty() -> {
                binding.rootLayout.snackbar("Username cannot be empty")
                return
            }
            password.isEmpty() -> {
                binding.rootLayout.snackbar("Password cannot be empty")
                return
            }
            else -> {
                // lifecycleScope is defined for activities and fragments
                // viewModel.userLogin is suspended function therefore we use coroutines
                binding.progressBar.show()
                lifecycleScope.launch {
                    try {
                        val signInResponse = viewModel.userLogin(username,  password)

                        if(signInResponse.data != null) {
                            binding.progressBar.hide()
                            val username = signInResponse.data["user_name"]
                            val user = User(username)
                            viewModel.saveLoggedInUser(user)
                        }
                        else {
                            Log.i("SignInResponse", signInResponse.toString())
                            binding.progressBar.hide()
                            binding.rootLayout.snackbar(signInResponse.response_message!!)
                        }
                    }
                    catch (e: NoInternetException) {
                        e.printStackTrace()
                        binding.progressBar.hide()
                        binding.rootLayout.snackbar(e.message.toString())
                    }
                    catch (e: ApiException) {
                        e.printStackTrace()
                        binding.progressBar.hide()
                        binding.rootLayout.snackbar(e.message.toString())
                    }


                }
            }
        }



    }

}
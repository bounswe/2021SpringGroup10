package com.example.mvvmapp.ui.auth

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import androidx.databinding.DataBindingUtil
import androidx.lifecycle.*
import com.example.mvvmapp.R
import com.example.mvvmapp.data.db.entities.User
import com.example.mvvmapp.databinding.ActivitySignupBinding
import com.example.mvvmapp.ui.home.HomeActivity
import com.example.mvvmapp.ui.home.profile.ProfileCreationActivity
import com.example.mvvmapp.util.*
import kotlinx.coroutines.launch
import org.kodein.di.KodeinAware
import org.kodein.di.android.kodein
import org.kodein.di.generic.instance

class SignupActivity : AppCompatActivity(), KodeinAware {

    override val kodein by kodein()

    private val factory : AuthViewModelFactory by instance()

    private lateinit var binding: ActivitySignupBinding
    private lateinit var viewModel: AuthViewModel

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding = DataBindingUtil.setContentView(this, R.layout.activity_signup)

        viewModel = ViewModelProvider(this, factory)[AuthViewModel::class.java]



        viewModel.getLoggedInUser().observe(this, Observer { user ->
            if(user != null) {
                Intent(this, ProfileCreationActivity::class.java).also {
                    // set flags to create a fresh activity.
                    // for example if we don't do this the user will see
                    // login activity when they click back button even though
                    // they are logged in
                    it.flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
                    startActivity(it)
                }
            }
        })

        binding.buttonSignUp.setOnClickListener {
            userSignup()
        }

        binding.textViewLogin.setOnClickListener {
            startActivity(Intent(this, LoginActivity::class.java))
        }
    }

    private fun userSignup() {
        val username = binding.editTextName.text.toString().trim()
        val email = binding.editTextEmail.text.toString().trim()
        val password = binding.editTextPassword.text.toString().trim()
        val passwordConfirm = binding.editTextPasswordConfirm.text.toString().trim()

        when {
            username.isEmpty() -> {
                binding.root.snackbar("Username cannot be empty")
            }

            email.isEmpty() -> {
                binding.root.snackbar("Email cannot be empty")
            }

            password.isEmpty() -> {
                binding.root.snackbar("Password cannot be empty")
            }

            password != passwordConfirm -> {
                binding.root.snackbar("Passwords do not match")
            }

            else -> {
                binding.progressBar.show()
                lifecycleScope.launch {
                    try {
                        val signUpResponse = viewModel.userSignup(username, email, password)

                        if(signUpResponse.response_message == "User successfully signed up.") {
                            binding.progressBar.hide()
                            val user = User(username)
                            viewModel.saveLoggedInUser(user)
                        }
                        else {
                            binding.progressBar.hide()
                            binding.root.snackbar(signUpResponse.response_message!!)
                        }
                    }
                    catch (e: ApiException) {
                        binding.progressBar.hide()
                        binding.rootLayout.snackbar(e.message.toString())
                    }
                    catch (e: NoInternetException) {
                        binding.progressBar.hide()
                        binding.rootLayout.snackbar("Internet connection is not available")
                    }
                }
            }
        }


    }

}
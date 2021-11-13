package com.example.mvvmapp.ui.home.profile

import androidx.lifecycle.ViewModel
import com.example.mvvmapp.data.repositories.UserRepository

class ProfileViewModel(
    repository: UserRepository
) : ViewModel() {

    val user = repository.getUser()

}
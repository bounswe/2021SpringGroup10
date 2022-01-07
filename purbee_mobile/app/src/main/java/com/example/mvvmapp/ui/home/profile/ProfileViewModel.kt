package com.example.mvvmapp.ui.home.profile

import androidx.lifecycle.ViewModel
import com.example.mvvmapp.data.db.entities.Profile
import com.example.mvvmapp.data.repositories.UserRepository

class ProfileViewModel(
    private val repository: UserRepository
) : ViewModel() {

    val profile = repository.getProfile()
    val user = repository.getUser()

    suspend fun saveProfile(newProfile: Profile) = repository.saveProfile(newProfile)

}
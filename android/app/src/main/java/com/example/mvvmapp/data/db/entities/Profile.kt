package com.example.mvvmapp.data.db.entities

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity
data class Profile (
    val userName: String?,
    val firstName: String?,
    val lastName: String?,
    val birthDate: String?,
    val biography: String?
) {
    @PrimaryKey(autoGenerate = false)
    var uid: Int = CURRENT_USER_ID
}
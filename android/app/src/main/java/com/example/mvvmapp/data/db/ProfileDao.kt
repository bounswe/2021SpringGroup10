package com.example.mvvmapp.data.db

import androidx.lifecycle.LiveData
import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.example.mvvmapp.data.db.entities.CURRENT_USER_ID
import com.example.mvvmapp.data.db.entities.Profile

@Dao
interface ProfileDao {

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertOrUpdate(profile: Profile) : Long

    @Query("SELECT * FROM user WHERE uid = $CURRENT_USER_ID")
    fun getProfile() : LiveData<Profile>
}
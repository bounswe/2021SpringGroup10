package com.example.mvvmapp.ui.home

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import androidx.databinding.DataBindingUtil
import androidx.navigation.NavController
import androidx.navigation.findNavController
import androidx.navigation.ui.AppBarConfiguration
import androidx.navigation.ui.NavigationUI
import androidx.navigation.ui.setupWithNavController
import com.example.mvvmapp.R
import com.example.mvvmapp.databinding.ActivityNavigationBinding
import com.google.android.material.bottomnavigation.BottomNavigationView
import com.google.android.material.navigation.NavigationView

class NavigationActivity : AppCompatActivity() {

    private lateinit var appBarConfiguration: AppBarConfiguration
    private lateinit var navController: NavController
    private lateinit var binding: ActivityNavigationBinding
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        //setContentView(R.layout.activity_navigation)
        binding = DataBindingUtil.setContentView<ActivityNavigationBinding>(this, R.layout.activity_navigation)

        // bottom navigation
        navController = findNavController(R.id.hostFragment)
        binding.bottomNavigation.setupWithNavController(navController)

        // Navigation Up Button
        appBarConfiguration = AppBarConfiguration(navController.graph, binding.drawerLayout2)
        NavigationUI.setupActionBarWithNavController(this, navController, binding.drawerLayout2)

        // Drawer Navigation
        NavigationUI.setupWithNavController(binding.navigationView, navController)
    }

    override fun onSupportNavigateUp(): Boolean {
        return NavigationUI.navigateUp(navController, appBarConfiguration)
    }
}
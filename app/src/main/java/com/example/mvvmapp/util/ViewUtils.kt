package com.example.mvvmapp.util

import android.content.Context
import android.widget.Toast

// Extension function for creating Toast
fun Context.toast(message: String) {
    Toast.makeText(this, message, Toast.LENGTH_LONG).show()
}
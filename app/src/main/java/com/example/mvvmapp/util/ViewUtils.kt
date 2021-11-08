package com.example.mvvmapp.util

import android.content.Context
import android.view.View
import android.widget.ProgressBar
import android.widget.Toast

// Extension function for creating Toast
fun Context.toast(message: String) {
    Toast.makeText(this, message, Toast.LENGTH_LONG).show()
}

fun ProgressBar.show() {
    visibility = View.VISIBLE
}

fun ProgressBar.hide() {
    visibility = View.GONE
}
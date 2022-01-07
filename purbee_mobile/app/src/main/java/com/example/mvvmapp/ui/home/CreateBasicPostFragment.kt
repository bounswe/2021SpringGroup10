package com.example.mvvmapp.ui.home

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.EditText
import android.widget.Toast
import androidx.databinding.DataBindingUtil
import androidx.fragment.app.Fragment
import com.example.mvvmapp.R
import com.example.mvvmapp.databinding.FragmentBasicPostCreationBinding

class CreateBasicPostFragment: Fragment() {
    lateinit var binding: FragmentBasicPostCreationBinding

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        binding = DataBindingUtil.inflate<FragmentBasicPostCreationBinding>(
            inflater, R.layout.fragment_basic_post_creation, container, false)

        var postText = binding.editTextPost
        binding.buttonCreatePost.setOnClickListener {
            Toast.makeText(activity, "Post Created!", Toast.LENGTH_LONG).show()
            postText.setText("")
        }
        return binding.root
    }
}
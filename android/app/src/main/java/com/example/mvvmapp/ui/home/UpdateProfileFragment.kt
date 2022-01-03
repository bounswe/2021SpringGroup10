package com.example.mvvmapp.ui.home

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.databinding.DataBindingUtil
import androidx.navigation.findNavController
import com.example.mvvmapp.R
import com.example.mvvmapp.databinding.FragmentUpdateProfileBinding

class UpdateProfileFragment:Fragment() {

    lateinit var binding: FragmentUpdateProfileBinding

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        binding = DataBindingUtil.inflate<FragmentUpdateProfileBinding>(
            inflater, R.layout.fragment_update_profile, container, false)

        var postText = binding.editTextProfileInfo
        binding.buttonUpdateProfileSave.setOnClickListener { view ->
            Toast.makeText(activity, "Profile Updated!", Toast.LENGTH_LONG).show()
            postText.setText("")
        }

        return binding.root
    }

}
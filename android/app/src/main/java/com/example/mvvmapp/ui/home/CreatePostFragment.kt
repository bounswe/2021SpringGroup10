package com.example.mvvmapp.ui.home

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.databinding.DataBindingUtil
import androidx.navigation.findNavController
import com.example.mvvmapp.R
import com.example.mvvmapp.databinding.FragmentCreatePostBinding


class CreatePostFragment : Fragment() {
    lateinit var binding: FragmentCreatePostBinding

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        binding = DataBindingUtil.inflate<FragmentCreatePostBinding>(
            inflater, R.layout.fragment_create_post, container, false)

        binding.buttonBasicPostType.setOnClickListener { view ->
            view.findNavController().navigate(R.id.action_createPostFragment_to_createBasicPostFragment)

        }
        return binding.root
    }


}
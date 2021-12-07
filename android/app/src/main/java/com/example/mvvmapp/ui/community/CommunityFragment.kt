package com.example.mvvmapp.ui.community

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.databinding.DataBindingUtil
import com.example.mvvmapp.R
import com.example.mvvmapp.databinding.FragmentCommunityBinding
import com.example.mvvmapp.databinding.FragmentHomeBinding

class CommunityFragment : Fragment() {
    lateinit var binding: FragmentCommunityBinding

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        binding = DataBindingUtil.inflate<FragmentCommunityBinding>(
            inflater, R.layout.fragment_community, container, false)

        return binding.root
    }
}
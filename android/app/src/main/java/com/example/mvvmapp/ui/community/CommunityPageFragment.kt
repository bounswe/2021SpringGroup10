package com.example.mvvmapp.ui.community

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.databinding.DataBindingUtil
import androidx.navigation.findNavController
import com.example.mvvmapp.R
import com.example.mvvmapp.databinding.FragmentCommunityCreationBinding
import com.example.mvvmapp.databinding.FragmentCommunityPageBinding

class CommunityPageFragment : Fragment() {

    private lateinit var binding: FragmentCommunityPageBinding

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        binding = DataBindingUtil.inflate(inflater, R.layout.fragment_community_page, container, false)

        binding.button.setOnClickListener { view ->
            view.findNavController().navigate(R.id.action_communityCreationFragment_to_communityPageFragment)

        }

        return binding.root
    }

}
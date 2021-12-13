package com.example.mvvmapp.ui.community

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.databinding.DataBindingUtil
import androidx.navigation.findNavController
import com.example.mvvmapp.R
import com.example.mvvmapp.databinding.FragmentCommunityBinding
import com.example.mvvmapp.databinding.FragmentCommunityCreationBinding


class CommunityCreationFragment : Fragment() {

    private lateinit var binding: FragmentCommunityCreationBinding

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        binding = DataBindingUtil.inflate(inflater, R.layout.fragment_community_creation, container, false)

        binding.buttonCreateCommunity.setOnClickListener { view ->
            view.findNavController().navigate(R.id.action_communityCreationFragment_to_communityPageFragment)

        }

        return binding.root
    }

}
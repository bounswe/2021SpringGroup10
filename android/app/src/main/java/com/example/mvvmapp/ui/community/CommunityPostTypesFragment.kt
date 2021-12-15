package com.example.mvvmapp.ui.community

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.databinding.DataBindingUtil
import androidx.navigation.findNavController
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.mvvmapp.R
import com.example.mvvmapp.adapters.CommunityPostTypeAdapter
import com.example.mvvmapp.data.CommunityPostType
import com.example.mvvmapp.databinding.FragmentCommunityPostTypesBinding

class CommunityPostTypesFragment : Fragment() {

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {

        var postTypes = mutableListOf(
            CommunityPostType("Basketball Event"),
            CommunityPostType("Theatre Event")
        )

        val adapter = CommunityPostTypeAdapter(postTypes)
        val binding = DataBindingUtil.inflate<FragmentCommunityPostTypesBinding>(
            inflater, R.layout.fragment_community_post_types, container, false)

        binding.rvPostTypes.adapter = adapter
        binding.rvPostTypes.layoutManager = LinearLayoutManager(context)

        binding.btnAddPostType.setOnClickListener { view ->
            view.findNavController().navigate(R.id.action_communityPostTypesFragment_to_communityPostTypeCreationFragment)
        }

        // Inflate the layout for this fragment
        return binding.root
    }
}
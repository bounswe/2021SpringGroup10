package com.example.mvvmapp.ui.community

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter
import com.example.mvvmapp.R
import com.example.mvvmapp.databinding.FragmentCommunityPostTypeCreationBinding


class CommunityPostTypeCreationFragment : Fragment() {

    private lateinit var binding: FragmentCommunityPostTypeCreationBinding

    override fun onResume() {
        super.onResume()
        val postTypeFields = resources.getStringArray(R.array.fields)
        val arrayAdapter = ArrayAdapter(requireContext(), R.layout.dropdown_item, postTypeFields)
        binding.autoCompleteTextView.setAdapter(arrayAdapter)
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        binding = FragmentCommunityPostTypeCreationBinding.inflate(inflater, container, false)



        return binding.root
    }

}
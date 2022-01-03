package com.example.mvvmapp.ui.home

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.content.Context
import android.widget.SearchView
import android.view.ViewGroup
import android.widget.ArrayAdapter
import androidx.databinding.DataBindingUtil
import androidx.fragment.app.Fragment
import com.example.mvvmapp.R
import com.example.mvvmapp.databinding.FragmentSearchBinding

class SearchFragment : Fragment() {

    lateinit var binding: FragmentSearchBinding

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        binding = DataBindingUtil.inflate<FragmentSearchBinding>(
            inflater, R.layout.fragment_search, container, false)

        val communityList = arrayOf("CMPE 451", "Basketball", "Football", "Tennis", "Volleyball", "Ice Hockey")
        val communityAdapter : ArrayAdapter<String> = ArrayAdapter(activity as Context, android.R.layout.simple_list_item_1, communityList)

        binding.searchList.adapter = communityAdapter;

        binding.searchView.setOnQueryTextListener(object : SearchView.OnQueryTextListener{
            override fun onQueryTextSubmit(query: String?): Boolean {
                binding.searchView.clearFocus()
                if(communityList.contains(query)){
                    communityAdapter.filter.filter(query)
                }
                return false
            }

            override fun onQueryTextChange(p0: String?): Boolean {
                communityAdapter.filter.filter(p0)
                return false
            }

        })

        return binding.root
    }

}
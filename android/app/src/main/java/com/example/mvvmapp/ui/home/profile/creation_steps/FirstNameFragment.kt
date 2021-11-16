package com.example.mvvmapp.ui.home.profile.creation_steps

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.databinding.DataBindingUtil
import androidx.navigation.findNavController
import com.example.mvvmapp.R
import com.example.mvvmapp.databinding.FragmentFirstNameBinding


class FirstNameFragment : Fragment() {

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {

        val binding = DataBindingUtil.inflate<FragmentFirstNameBinding>(
            inflater, R.layout.fragment_first_name, container, false)

        binding.buttonContinue.setOnClickListener { view : View ->
            val firstName = binding.editTextUsername.text.toString().trim()
            view.findNavController().navigate(FirstNameFragmentDirections.actionFirstNameFragmentToLastNameFragment(firstName))
        }


        // Inflate the layout for this fragment
        return binding.root
    }

}
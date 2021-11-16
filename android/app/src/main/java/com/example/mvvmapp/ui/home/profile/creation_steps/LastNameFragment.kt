package com.example.mvvmapp.ui.home.profile.creation_steps

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.databinding.DataBindingUtil
import androidx.navigation.findNavController
import com.example.mvvmapp.R
import com.example.mvvmapp.databinding.FragmentLastNameBinding


class LastNameFragment : Fragment() {

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {

        val binding = DataBindingUtil.inflate<FragmentLastNameBinding>(
            inflater, R.layout.fragment_last_name, container, false)

        val args = LastNameFragmentArgs.fromBundle(requireArguments())

        binding.buttonContinue.setOnClickListener { view : View ->
            val lastName = binding.editTextLastname.text.toString().trim()
            view.findNavController().navigate(LastNameFragmentDirections.actionLastNameFragmentToBirthDateFragment(args.firstName, lastName))
        }

        // Inflate the layout for this fragment
        return binding.root
    }

}
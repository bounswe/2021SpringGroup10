package com.example.mvvmapp.ui.home.profile

import androidx.lifecycle.ViewModelProvider
import android.os.Bundle
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.databinding.DataBindingUtil
import com.example.mvvmapp.R
import com.example.mvvmapp.databinding.ProfileFragmentBinding
import org.kodein.di.KodeinAware
import org.kodein.di.android.x.kodein
import org.kodein.di.generic.instance

class ProfileFragment : Fragment(), KodeinAware {

    override val kodein by kodein()
    private val factory: ProfileViewModelFactory by instance()

    private lateinit var binding: ProfileFragmentBinding
    private lateinit var viewModel: ProfileViewModel

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        binding = DataBindingUtil.inflate(inflater, R.layout.profile_fragment, container, false)
        viewModel = ViewModelProvider(this, factory)[ProfileViewModel::class.java]

        binding.viewmodel = viewModel

        // as we are binding a live data (ProfileViewModel.user) to layout
        // we need to define the lifecycle owner
        binding.lifecycleOwner = this



        try {
//            val args = ProfileFragmentArgs.fromBundle(requireArguments())
//            Log.i("ProfileArguments", args.toString())
//            binding.name.text = args.firstName
//            binding.birthDate.text = args.birthDate
//            binding.biography.text = args.biography
        }
        catch (e: Exception) {
            binding.name.text = "foo bar"
            binding.birthDate.text = "16/11/2021"
            binding.biography.text = "biography baz"
        }


        return binding.root
    }


}
package com.example.mvvmapp.ui.home.profile.creation_steps

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.databinding.DataBindingUtil
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.lifecycleScope
import androidx.navigation.findNavController
import com.example.mvvmapp.R
import com.example.mvvmapp.data.db.entities.Profile
import com.example.mvvmapp.databinding.FragmentBiographyBinding
import com.example.mvvmapp.ui.home.profile.ProfileViewModel
import com.example.mvvmapp.ui.home.profile.ProfileViewModelFactory
import kotlinx.coroutines.launch
import org.kodein.di.KodeinAware
import org.kodein.di.android.x.kodein
import org.kodein.di.generic.instance

class BiographyFragment : Fragment(), KodeinAware {

    override val kodein by kodein()
    private val factory: ProfileViewModelFactory by instance()

    private lateinit var viewModel: ProfileViewModel

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {

        val binding = DataBindingUtil.inflate<FragmentBiographyBinding>(
            inflater, R.layout.fragment_biography, container,false)

        viewModel = ViewModelProvider(this, factory)[ProfileViewModel::class.java]

        val args = BiographyFragmentArgs.fromBundle(requireArguments())

        binding.buttonFinish.setOnClickListener { view ->
            val biography = binding.editTextBiography.text.toString().trim()
//            val user = viewModel.user
//            val profile = Profile(user.value!!.username, args.firstName, args.lastName, args.birthDate, biography)
//            lifecycleScope.launch {
//                viewModel.saveProfile(profile)
//            }

            view.findNavController().navigate(BiographyFragmentDirections.actionBiographyFragmentToProfileFragment2(args.firstName, args.lastName, args.birthDate, biography))
        }

        binding.lifecycleOwner = this

        // Inflate the layout for this fragment
        return binding.root
    }

}
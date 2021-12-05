package com.example.mvvmapp.ui.home.profile.creation_steps

import android.os.Bundle
import android.text.InputType
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.databinding.DataBindingUtil
import androidx.navigation.findNavController
import com.example.mvvmapp.R
import com.example.mvvmapp.databinding.FragmentProfileCreationBinding
import java.text.SimpleDateFormat
import java.util.*


class ProfileCreationFragment : Fragment() {
    lateinit var binding: FragmentProfileCreationBinding
    lateinit var firstName: String
    lateinit var lastName: String
    lateinit var birthDate: String
    lateinit var biography: String
    lateinit var prompt: String
    lateinit var hint: String
    lateinit var buttonText: String
    private var index = 0

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {

        binding = DataBindingUtil.inflate<FragmentProfileCreationBinding>(
            inflater, R.layout.fragment_profile_creation, container, false)

        setContent()

        binding.profileInfo = this

        binding.buttonContinue.setOnClickListener { view : View ->
            when(index) {
                0 -> {
                    firstName = binding.editTextProfileInfo.text.toString().trim()
                    Log.i("ProfileCreationFragment", "firstname: $firstName")
                }
                1 -> {
                    lastName = binding.editTextProfileInfo.text.toString().trim()
                    Log.i("ProfileCreationFragment", "lastName: $lastName")
                }
                2 -> {
                    val day = binding.datePicker.dayOfMonth
                    val month = binding.datePicker.month
                    val year = binding.datePicker.year
                    val calendar = Calendar.getInstance()
                    calendar.set(year, month, day)
                    val sdf = SimpleDateFormat("dd.MM.yyyy", Locale.US)
                    birthDate = sdf.format(calendar.time)
                    Log.i("ProfileCreationFragment", "birthDate: $birthDate")
                }
                3 -> {
                    biography = binding.editTextProfileInfo.text.toString().trim()
                    view.findNavController().navigate(ProfileCreationFragmentDirections.actionProfileCreationFragmentToHomeFragment())
                    Log.i("ProfileCreationFragment", "biography: $biography")
                }
            }
            index += 1
            setContent()
            binding.invalidateAll()
        }


        // Inflate the layout for this fragment
        return binding.root
    }

    private fun setContent() {
        binding.editTextProfileInfo.text = null
        Log.i("ProfileCreationFragment", "index: $index")
        when(index) {
            0 -> {
                prompt = "Type in your first name"
                hint = "First name"
                buttonText = "Next"
                Log.i("ProfileCreationFragment", "index 0 aq")
            }
            1 -> {
                prompt = "Type in your last name"
                hint = "Last name"
                buttonText = "Next"
                Log.i("ProfileCreationFragment", "index 1 aq")
            }
            2 -> {
                prompt = "Select your birth date"
                buttonText = "Next"
                binding.datePicker.visibility = View.VISIBLE
                binding.editTextProfileInfo.visibility = View.GONE
                Log.i("ProfileCreationFragment", "index 2 aq")
            }
            3 -> {
                prompt = "Tell us about your biography"
                hint = "Biography"
                buttonText = "Finish"
                binding.datePicker.visibility = View.GONE
                binding.editTextProfileInfo.visibility = View.VISIBLE
                binding.editTextProfileInfo.setRawInputType(InputType.TYPE_TEXT_FLAG_MULTI_LINE)
            }
        }
    }

}
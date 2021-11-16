package com.example.mvvmapp.ui.home.profile.creation_steps

import android.os.Bundle
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.DatePicker
import androidx.databinding.DataBindingUtil
import androidx.navigation.findNavController
import com.example.mvvmapp.R
import com.example.mvvmapp.databinding.FragmentBirthDateBinding
import com.example.mvvmapp.databinding.FragmentLastNameBinding
import java.util.*


class BirthDateFragment : Fragment() {


    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        val binding = DataBindingUtil.inflate<FragmentBirthDateBinding>(
            inflater, R.layout.fragment_birth_date, container, false)

        val args = BirthDateFragmentArgs.fromBundle(requireArguments())

//        val c = Calendar.getInstance()
//        val year = c.get(Calendar.YEAR)
//        val month = c.get(Calendar.MONTH)
//        val day = c.get(Calendar.DAY_OF_MONTH)

        var date: String? = null

        binding.datePicker1.setOnDateChangedListener { _: DatePicker, mYear, mMonth, mDay ->
            date = "$mDay/${mMonth+1}/$mYear"
            Log.i("date", date!!)
        }

        binding.buttonContinue.setOnClickListener { view : View ->

            view.findNavController().navigate(BirthDateFragmentDirections.actionBirthDateFragmentToBiographyFragment(args.firstName, args.lastName, date!!))
        }

        // Inflate the layout for this fragment
        return binding.root
    }

}
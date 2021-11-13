package com.example.mvvmapp.ui.home.quotes

import androidx.lifecycle.ViewModel
import com.example.mvvmapp.data.repositories.QuotesRepository
import com.example.mvvmapp.util.lazyDeferred

class QuotesViewModel(
    repository: QuotesRepository
) : ViewModel() {

    val quotes by lazyDeferred {
        repository.getQuotes()
    }

}
package com.example.mvvmapp.data.network.responses

import com.example.mvvmapp.data.db.entities.Quote

data class QuotesResponse(
    val isSuccessful: Boolean,
    val quotes: List<Quote>
)
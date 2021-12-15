package com.example.mvvmapp.adapters

import android.view.LayoutInflater
import android.view.ViewGroup
import android.widget.ArrayAdapter
import androidx.recyclerview.widget.RecyclerView
import com.example.mvvmapp.data.PostTypeField
import com.example.mvvmapp.databinding.ItemPostTypeFieldBinding

class PostTypeFieldsAdapter(
    var postTypeFields: List<PostTypeField>,
    val arrayAdapter : ArrayAdapter<String>
) : RecyclerView.Adapter<PostTypeFieldsAdapter.PostTypeFieldsViewHolder>() {

    inner class PostTypeFieldsViewHolder(val binding: ItemPostTypeFieldBinding) : RecyclerView.ViewHolder(binding.root)

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): PostTypeFieldsViewHolder {
        val layoutInflater = LayoutInflater.from(parent.context)
        val binding = ItemPostTypeFieldBinding.inflate(layoutInflater, parent, false)
        return PostTypeFieldsViewHolder(binding)
    }

    override fun onBindViewHolder(holder: PostTypeFieldsViewHolder, position: Int) {
        holder.binding.apply {
            autoCompleteTextView.setAdapter(arrayAdapter)
//            textView4.text = postTypeFields[position].label
        }
    }

    override fun getItemCount(): Int {
        return postTypeFields.size
    }
}
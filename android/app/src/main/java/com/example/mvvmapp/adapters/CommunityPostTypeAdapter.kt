package com.example.mvvmapp.adapters

import android.content.ClipData
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.example.mvvmapp.R
import com.example.mvvmapp.data.CommunityPostType
import com.example.mvvmapp.databinding.ItemPostTypeBinding

class CommunityPostTypeAdapter(
    var communityPostTypes: List<CommunityPostType>
) : RecyclerView.Adapter<CommunityPostTypeAdapter.CommunityPostTypeViewHolder>() {

    inner class CommunityPostTypeViewHolder(val binding: ItemPostTypeBinding) : RecyclerView.ViewHolder(binding.root)

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): CommunityPostTypeViewHolder {
        val layoutInflater = LayoutInflater.from(parent.context)
        val binding = ItemPostTypeBinding.inflate(layoutInflater, parent, false)
        return CommunityPostTypeViewHolder(binding)
    }

    override fun onBindViewHolder(holder: CommunityPostTypeViewHolder, position: Int) {
        holder.binding.apply {
            rvTitle.text = communityPostTypes[position].title
        }
    }

    override fun getItemCount(): Int {
       return communityPostTypes.size
    }
}
import React, { useState, useEffect} from 'react'
import { useNavigate } from "react-router-dom";
import {base_url, headers} from "../../utils/url"
import { getUser } from '../../utils/common';
import { List, ListItem, Divider, ListItemText, Button } from '@mui/material';
import Header from "../homepage/header";
import { useParams } from 'react-router-dom'
// import Feed from '../feed/feed'

const Axios = require('axios');

const Search = () => {

    const [communities, set_communities] = useState([]);
    const [users, set_users] = useState([])
    const [page_state, set_page_state] = useState("users")

    let navigate = useNavigate()
    const { search_item } = useParams()

    useEffect(() => {
        console.log(search_item)
        
        // const request_json = {
        //     "user_name": user_name
        // }
        // console.log(request_json)
        // Axios({
        //     headers: headers,
        //     method: "GET",
        //     url: base_url + 'profile_page/',
        //     data: request_json,
        // }).then(response => {
        //     console.log(response)
        //     // set_posts(response.data.posts)
        //     // set_followers(response.data.followers)
        //     // set_following(response.data.following)

        //     //navigate('/home')
        // }).catch(error => {
            
        //     setLoading(false)
        //     if (error.response) {
        //         // The request was made and the server responded with a status code
        //         // that falls out of the range of 2xx
        //         console.log(error.response.data);
        //         console.log(error.response.status);
        //         console.log(error.response.headers);
        //     } else if (error.request) {
        //         // The request was made but no response was received
        //         // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
        //         // http.ClientRequest in node.js
        //         console.log(error.request);
        //     } else {
        //         // Something happened in setting up the request that triggered an Error
        //         console.log('Error', error.message);
        //     }
        //     //setError(error.response.data.response_message)
        // })
      });


    if(page_state == "users") {

        return (
            <div className="App">
                <Header />
                <div>Users</div>
            </div>
        )
    }

    else {
        return (
            <div className="App">
                <Header />
                <div>Communities</div>
            </div>
        )
    }

    
}

export default Search
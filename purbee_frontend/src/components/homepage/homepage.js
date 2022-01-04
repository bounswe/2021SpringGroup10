import React, { useState, useEffect} from 'react'

import "./styles.css";
import Header from "./header";
import {base_url, headers} from "../../utils/url"
import Button from "@mui/material/Button";
import { getUser, getFollowing } from '../../utils/common';
import Feed from '../feed/feed'


const Axios = require('axios');

export const Homepage = () => {

    const [posts, set_posts] = useState([]);
    
    useEffect(() => {
        
        const request_json = {
            "user_name": "berkdddd"
        }
        console.log(request_json)
        const my_url = base_url + 'user_feed'
        Axios({
            headers: headers,
            method: "PUT",
            url: my_url,
            data: request_json,
        }).then(response => {
            set_posts(response.data.user_feed_post_list)


            //navigate('/home')
        }).catch(error => {
            
            if (error.response) {
                // The request was made and the server responded with a status code
                // that falls out of the range of 2xx
                console.log(error.response.data);
                console.log(error.response.status);
                console.log(error.response.headers);
            } else if (error.request) {
                // The request was made but no response was received
                // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
                // http.ClientRequest in node.js
                console.log(error)
                console.log(error.request);
            } else {
                // Something happened in setting up the request that triggered an Error
                console.log('Error', error.message);
            }
            //setError(error.response.data.response_message)
        })
      }, []);

    return (
        <div className="App">
            <Header />
            <Feed id_list = {posts} />

        </div>
    );
}

export default Homepage;

import React, { useState, useEffect} from 'react'
import { useNavigate } from "react-router-dom";
import {base_url, headers} from "../../utils/url"
import { getUser } from '../../utils/common';
import { List, ListItem, Divider, ListItemText, Button } from '@mui/material';
import Header from "../homepage/header";
import { useParams } from 'react-router-dom'
// import Feed from '../feed/feed'

const Axios = require('axios');

const Profile = () => {

    const [first_name, set_first_name] = useState("");
    const [user_name, set_user_name] = useState(getUser())
    const [last_name, set_last_name] = useState("");
    const [bio, set_bio] = useState("");
    const [birth_date, set_birth_date] = useState("");
    const [photo, set_photo] = useState("https://t3.ftcdn.net/jpg/03/46/83/96/360_F_346839683_6nAPzbhpSkIpb8pmAwufkC7c5eD7wYws.jpg");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [page_state, set_page_state] = useState("profile")
    const [followers, set_followers] = useState(["User1", "User2"])
    const [following, set_following] = useState([])
    const [posts, set_posts] = useState([])
    const [follow_message, set_follow_message] = useState("Follow")

    let navigate = useNavigate()
    const { user_name_ } = useParams()

    useEffect(() => {
        console.log(user_name_)
        
        const request_json = {
            "search_text":"ber"
        }
        console.log(request_json)
        const my_url = base_url + 'user_search'
        Axios({
            headers: headers,
            method: "PUT",
            url: my_url,
            data: request_json,
        }).then(response => {
            console.log(response)
            console.log(response.data.followers)
            set_posts(response.data.data.post_list)
            set_followers(response.data.data.followers)
            set_following(response.data.data.following)

            //navigate('/home')
        }).catch(error => {
            
            setLoading(false)
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
      }, [user_name]);

    const open_followers = () => {
        set_page_state("followers")
    }

    const open_following = () => {
        set_page_state("following")
    }

    const go_to_profile = () => {
        set_user_name(getUser())
        set_page_state("profile")
    }

    const go_user_profile = (user) => {
        set_user_name(user)
        set_page_state("profile")
    }

    const follow_user = () => {

        set_follow_message(prevState => {
            if(prevState == "Follow") return "Request sent"
            else return "Follow"
        })
    }

    if(page_state == "profile") {

        return (
            <div className="App">
                <Header />
                <div style={{
                    display:"flex",
                    justifyContent: "space-around",
                    margin:"18px 0px",
                    borderBottom: "1px solid grey"
                }}>
                    {user_name != getUser() ? <Button
                variant="contained"
                color="primary"
                style={{height: "20px"}}
                onClick={go_to_profile}
                className="form__custom-button">Back</Button> : null}
                    <div>
                        <img style={{width:"160px", height:"160px", borderRadius: "80px"}}
                        src= {photo}
                        />
                    </div>
                    <div>
                        <h4>{user_name}</h4>
                        <div style={{display: "flex", width:"108%", justifyContent:"space-between"}}> 
                            <h5>{posts.length} posts</h5>
                            <h5 onClick={open_followers}>{followers.length} followers</h5>
                            <h5 onClick={open_following}>{following.length} following</h5>
                            {user_name != getUser() ? <Button
                                variant="contained"
                                color="primary"
                                style={{height: "20px"}}
                                onClick={follow_user}
                                className="form__custom-button">{follow_message}</Button> : null}
                        </div>
                    </div>
                </div>
                {/* <Feed id_list = {posts} /> */}
            </div>
        )
    }
    else if(page_state == "followers") {
        const list_items = followers.map((follower) => {
            return (
                <div>
                     <ListItem button onClick={() => go_user_profile(follower)}>
                        <ListItemText primary={follower} />
                    </ListItem>
                    <Divider />
                </div>
               
            )   
        })

        const style = {
            width: '100%',
            maxWidth: 360,
            bgcolor: 'background.paper',
          };
        return (
            <div className='App'>
                <Header />
                <Button
                variant="contained"
                color="primary"
                onClick={go_to_profile}
                className="form__custom-button">Back</Button>
                <div style={{display: "flex",justifyContent: "center" }}>
                    <List sx={style} component="nav" aria-label="mailbox folders">
                        {list_items}
                    </List>
                </div>
            </div>
            
        )
    }
    else {
        const list_items = following.map((follower) => {
            return (
                <div>
                     <ListItem button onClick={() => go_user_profile(follower)}>
                        <ListItemText primary={follower} />
                    </ListItem>
                    <Divider />
                </div>
               
            )   
        })
        
        const style = {
            width: '100%',
            maxWidth: 360,
            bgcolor: 'background.paper',
          };
        return (
            <div className='App'>
                <Header />
                <Button
                variant="contained"
                color="primary"
                onClick={go_to_profile}
                className="form__custom-button">Back</Button>
                <div style={{display: "flex",justifyContent: "center" }}>
                    <List sx={style} component="nav" aria-label="mailbox folders">
                        {list_items}
                    </List>
                </div>
            </div>
            
        )
    }

    
}

export default Profile
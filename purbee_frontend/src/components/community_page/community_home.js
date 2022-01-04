import React from "react";
import { MockCommunity } from './mockCommunity'
import './community_home.css'
import { useParams } from 'react-router-dom'
import {base_url, headers} from "../../utils/url"
import Header from "../homepage/header";
import { getUser, getFollowing } from '../../utils/common';
import { useNavigate } from "react-router-dom";
import Feed from '../feed/feed'

const Axios = require('axios');

export const CommunityHome2 = () => {

    const [admin_list, set_admin_list] = React.useState([])
    const [created_at, set_created_at] = React.useState("")
    const [community_creator_id, set_community_creator_id] = React.useState("")
    const [description, set_description] = React.useState("")
    const [is_private, set_is_private] = React.useState(false)
    const [subscriber_list, set_subscriber_list] = React.useState([])
    const [post_history_id_list, set_post_history_id_list] = React.useState([])
    const [post_type_id_list, set_post_type_id_list] = React.useState([])
    const { community_name_ } = useParams()
    const [community_name, set_community_name] = React.useState(community_name_)
    const [subscribe_or_request, set_subscribe_or_request] = React.useState("Subscribe")
    const [requesters, set_requesters] = React.useState([])

    let navigate = useNavigate()

    
    React.useEffect(() => {

        async function tempFunc() {
            const my_url = base_url + 'community_page/' + community_name
            Axios({
                headers: headers,
                method: "GET",
                url: my_url
            }).then(response => {
                console.log(response)
                set_admin_list(response.data.community_instance.admin_list)
                set_created_at(response.data.community_instance.created_at)
                set_community_creator_id(response.data.community_instance.community_creator_id)
                set_description(response.data.community_instance.description)
                set_is_private(response.data.community_instance.is_private)
                set_subscriber_list(response.data.community_instance.subscriber_list)
                set_post_history_id_list(response.data.community_instance.post_history_id_list)
                set_requesters(response.data.community_instance.requesters)
                console.log("anan")
                var post_type_names = []
                var temp = response.data.community_instance.post_type_id_list.map(id => {
                    Axios({
                        headers: headers,
                        method: "PUT",
                        url: base_url + 'post_type',
                        data: {"post_type_id": id}
                    }).then(resp => {
                        // alert(resp.data.data.post_type_name)
                        post_type_names.push(resp.data.data.post_type_name)
                    }).catch(err => {
                        alert("error")
                    })
                })
                console.log(post_type_names)
                set_post_type_id_list(post_type_names)
                if(requesters.includes(getUser())) {
                    set_subscribe_or_request("Request sent")
                }
                else if(subscriber_list.includes(getUser)) {
                    set_subscribe_or_request("Unsubscribe")
                }

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
        }
        tempFunc()

        
    },[community_name])


    // React.useEffect(() => {

    // }, [post_type_id_list])

    const subscribe_community = (event) => {
        let my_url = ""
        if(subscribe_or_request == "Subscribe") {
            my_url = base_url + 'community_page/subscribe'
        }
        else {
            my_url = base_url + 'community_page/unsubscribe'
        }

        Axios({
            headers: headers,
            method: "PUT",
            url: my_url,
            data: {"user_id": getUser(), "community_id": community_name}
        }).then(response => {
            console.log(response)
            if(subscribe_or_request == "Subscribe") {
                if(is_private) {
                    set_subscribe_or_request("Request sent")
                }
                else {
                    Axios({
                        headers: headers,
                        method: "PUT",
                        url: base_url + 'community_page/request',
                        data: {"admin_id": admin_list[0],
                        "community_id": community_name,
                        "user_id": getUser(),
                        "action": "accept"}
                    }).then(resp => {
                        set_community_name(community_name_)
                        navigate('/community-home/' + community_name_)
                    })
                }
            }
            else {
                set_subscribe_or_request("Subscribe")
                set_community_name(community_name_)
                navigate('/community-home/' + community_name_)
            }
            

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
    }

    const create_post = () => {
        navigate('/home') // TODO: this will be create post
    }

    const create_post_type = () => {
        navigate('/home') // TODO: this will be create post type
    }

    const make_advanced_search = () => {
        navigate('/advanced-search/' + community_name)
    }

    return (
        <div className="App">
            <Header />
            <section className="section about-section gray-bg" id="about">
                <div className="container">
                    <div className="row align-items-center flex-row-reverse">
                        <div className="col-lg-6">
                            <div className="about-text go-to">
                                <h3 className="dark-color">{community_name}</h3>
                                <p> {description} </p>
                                <div className="row about-list">
                                    <div className="col-md-6">
                                        <div className="media">
                                            <label style={{width: "120px"}}> Creation Date </label>
                                            <p>{created_at}</p>
                                        </div>
                                        <div className="media">
                                            <label> Creator </label>
                                            <p> { community_creator_id } </p>
                                        </div>
                                        <div className="media">
                                            <label style={{width: "100px"}}>Post Types</label>
                                            {post_type_id_list.map(pt => <div> {pt} </div>)}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className="col-lg-6">
                            <div className="about-avatar">
                                <img src="https://t3.ftcdn.net/jpg/03/46/83/96/360_F_346839683_6nAPzbhpSkIpb8pmAwufkC7c5eD7wYws.jpg" title="Community Picture" alt=""/>
                            </div>
                        </div>
                    </div>
                    <div className="counter">
                        <div className="row">
                            <div className="col-6 col-lg-2">
                                <div className="count-data text-center">
                                    <h6 className="count h2">{subscriber_list.length}</h6>
                                    <p className="m-0px font-w-600">Member Count</p>
                                </div>
                            </div>
                            <div className="col-6 col-lg-2">
                                <div className="count-data text-center">
                                    <h6 className="count h2" data-to={post_history_id_list.length} data-speed={post_history_id_list.length}>{post_history_id_list.length}</h6>
                                    <p className="m-0px font-w-600">Post Count</p>
                                </div>
                            </div>
                            <div className="col-6 col-lg-2">
                                <div className="count-data text-center">
                                    <button type="button" className="btn btn-primary" onClick={subscribe_community}> {subscribe_or_request} </button>
                                </div>
                            </div> 
                            {(subscriber_list.includes(getUser()) || admin_list.includes(getUser())) ? 
                            <div className="col-6 col-lg-2">
                                <div className="count-data text-center">
                                    <button type="button" className="btn btn-primary" onClick={create_post}> Create Post </button>
                                </div>
                            </div> :
                            null
                        }
                            
                            {admin_list.includes(getUser()) ? 
                            <div className="col-6 col-lg-2">
                                <div className="count-data text-center">
                                    <button type="button" className="btn btn-primary" onClick={create_post_type}> Create Post Type </button>
                                </div>
                            </div> :
                            null
                        }
                        <div className="col-6 col-lg-2">
                            <div className="count-data text-center">
                                <button type="button" className="btn btn-primary" onClick={make_advanced_search}> Make Advanced Search </button>
                            </div>
                        </div>
                            
                        </div>
                    </div>
                </div>
                <Feed id_list = {post_history_id_list} />
            </section>
        </div>
        
    );
}

export default CommunityHome2;
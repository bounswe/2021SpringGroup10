import React from "react";
import { MockCommunity } from './mockCommunity'
import './community_home.css'
import { useParams } from 'react-router-dom'
import {base_url, headers} from "../../utils/url"
import Header from "../homepage/header";

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

    
    React.useEffect(() => {

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
            set_post_type_id_list(response.data.community_instance.post_type_id_list)

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
    },[community_name])

    const join_community = (event) => {
        
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
                            <div className="col-6 col-lg-3">
                                <div className="count-data text-center">
                                    <h6 className="count h2">{subscriber_list.length}</h6>
                                    <p className="m-0px font-w-600">Member Count</p>
                                </div>
                            </div>
                            <div className="col-6 col-lg-3">
                                <div className="count-data text-center">
                                    <h6 className="count h2" data-to={post_history_id_list.length} data-speed={post_history_id_list.length}>{post_history_id_list.length}</h6>
                                    <p className="m-0px font-w-600">Post Count</p>
                                </div>
                            </div>
                            <div className="col-6 col-lg-3">
                                <div className="count-data text-center">
                                    <button type="button" className="btn btn-primary" onClick={join_community}> Join! </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </div>
        
    );
}

export default CommunityHome2;
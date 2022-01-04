import * as React from 'react';
import Popup from 'reactjs-popup';
import './post.scss';
import {posts, post_types, post_api_result, post_type_api_result, post_type_ex, post_ex} from './mock_post';
import { MdFavorite, MdFavoriteBorder} from "react-icons/all";
import {Component, useEffect, useState} from "react";
import Axios from "axios";
import {apiCall} from '../../helper';
import {Map} from './googlemap';


//                {fields["PlainText"].map(header => (<div className="postcard__preview-txt">{header + ": " + text(header)}</div>))}

let headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'DELETE, GET, OPTIONS, POST, PUT',
    'Access-Control-Allow-Headers': 'Authorization, Content-Type, Access-Control-Allow-Headers, X-Requested-With, Access-Control-Allow-Origin'
};
let endpoint = "https://cz2qlmf16e.execute-api.us-east-2.amazonaws.com/dev/api/"

export const Post = (props) => { // data shall contain post id, post types and post type id-name map,

    const [current_image, set_current_image] = React.useState(0);
    const [all_images, set_all_images] = React.useState([])
    const [post_like, set_post_like] = React.useState(false);
    const [post_fields, set_post_fields] = React.useState([]);
    const [post_likers, set_post_likers] = React.useState([]);
    const [post_owner, set_post_owner] = React.useState("");
    const [post, set_post] = React.useState({});
    const [post_type, set_post_type] =  React.useState({});
    const [fields, set_fields] = React.useState({});
    const [calls_done, set_calls_done] = React.useState(false);
    const [post_type_fields, set_post_type_fields] = React.useState([])

    useEffect(() => {//do initial api calls fetch post;
        //const post_id = "fa8da556-68b5-4d4b-9ff8-040a07e93a7a" //give through props

        //const post_type_id = post["post_type_id"]

        //const post_type = post_types[post_type_id];
        const post_id = props.post_id;
        const req_json = { "post_id": "2608fa97-9b37-4725-8c1b-eb678ac8c9e4"}
        Axios({
            headers: headers,
            method: "PUT",
            url: (endpoint + "post"),
            data: req_json,
        }).then(response => {
            set_post(response.data.data)
            return response;
        })
            .catch(error=> console.log(error));
    }, []);
    useEffect(() => {
        const req_json = {"post_type_id": "ed537666-024f-4045-b004-6c7c1c0b8038"}
        Axios({
            headers: headers,
            method: "PUT",
            url: (endpoint + "post_type"),
            data: req_json,
        }).then(response => {
            set_post_type(response.data.data)
            return response;
        })
            .catch(error=> console.log(error));
    }, [post])

    useEffect(()=> {
        set_post_type_fields(post_type.post_field_info_dictionaries_list);
    }, [post_type])


    useEffect(() => {
        let fieldss = { //each field type has an array of headers
            "PlainText": [],
            "Price": [],
            "Location": [],
            "Participation": [],
            "Poll": [],
            "Document": [],
            "DateTime": [],
            "Photo": [],
        }
        try {
            Object.keys(post_type_fields).forEach(key => {
                fieldss[post_type_fields[key]["field_type"]].push(post_type_fields[key]["header"]);
            })
        } catch{}

        set_fields(fieldss);
        set_post_fields(post["post_entries_dictionary_list"]);
        set_post_likers(post["post_liked_user_list"]);
        set_post_owner(post["post_owner_user_name"]);
    }, [post_type_fields])
    useEffect(() => {
        console.log("bak");
        console.log(post);
        console.log(fields);
        if(post_owner !== "" && post_owner !== undefined){
            console.log("aq")
            console.log(post_owner)
            set_calls_done(true);
        }
        try {
            const img_link = (header) => post_fields.find(pf => pf["header"] === header)["image"]
            const imgs = fields["Photo"].map(header => img_link(header));
            set_all_images(imgs);
        } catch{}
        }, [fields]);
    //const images = posts[post_id]["pictures"]


    const likeClick = () => {
        set_post_like(!post_like);
    }
    const post_liker_display = () => {
        try{
            return post_likers.length === 0 ? (<div> There are no likes yet...</div>)
                :
                post_likers.map(u =>
                    (<li className="tag__item play red">
                        <a><i/>{u}</a>
                    </li>))
        } catch{
            return <div/>
        }
    }
    const text = (header) => post_fields.find(pf => pf["header"] === header)["text"];
    const location_text = (header) => post_fields.find(pf => pf["header"] === header)["text"]; //implement location
    const price = (header) => {
        const f = post_fields.find(pf => pf["header"] === header);
        return f["amount"] + " " + f["currency"];
    };
    const date = (header) => {
        const d = post_fields.find(pf => pf["header"] === header)
        return d["date"] + " " + d["time"];
    }
    const locations = () => {
        let component = "";
        const location_text = (header) => post_fields.find(pf => pf["header"] === header);
        fields["Location"].map(header => {
            component += (
                <li className="tag__item play red">
                    <a><i className="fas fa-play mr-2"/>{location_text(header)}</a>
                </li>
            );
        });
        return component;
    }
    //const image = (header) => post_fields.find(pf => pf["header"] === header)["image"]

    /* IMAGE PART
    * <a className="postcard__img_link">
                <img className="postcard__img" src={images[current_image]} alt="Image Title" onClick={(event) => {
                    set_current_image((current_image+1) % images.length);
                    console.log((current_image+1)%images.length)
                }}/>
                <br/>
            </a>
            *
            * <a className="postcard__img_link">
                <img className="postcard__img" src="https://i.imgur.com/8WRRCb.png" alt="Image Title"/>
                <br/>
            </a>
    * */

    return (
    !calls_done ? <div> calls are not done</div>
        :
    <div>
        <article className="postcard dark red">
            <a className="postcard__img_link">
                <img className="postcard__img" src={all_images[current_image]} alt="Image Title" onClick={(event) => {
                    set_current_image((current_image+1) % all_images.length);
                }}/>
                <br/>
            </a>
            <div className="postcard__text">
                <h1 className="postcard__title red"><a href="#">{post["post_title"]}</a></h1>
                <div className="postcard__subtitle small">
                    <time dateTime="2020-05-25 12:00:00">
                        <i className="fas fa-calendar-alt mr-2"/>Creator: <a href="asd">{post_owner}<br/></a>
                        {fields["DateTime"].map(header => (<i className="postcard__preview-txt-onur">+{header + ": " + date(header)}<br/></i>))}
                        {fields["Price"].map(header => (<i className="fas fa-calendar-alt mr-2">{"+" + header + ": " + price(header)}<br/></i>))}

                    </time>
                </div>
                <div className="postcard__bar"/>

                {fields["PlainText"].map(header => (<i className="postcard__preview-txt-onur">{header + ": " + text(header)}</i>))}

                <ul className="postcard__tagbox">
                    {fields["Location"].map(header =>
                        (
                        <Map/>
                        ))
                    }
                </ul>
                <br/>
                <ul className="postcard__tagbox">
                    <Popup
                        trigger={
                            <li className="tag__item play red">
                                <a><i/>Liked Users</a>
                            </li>}
                        modal>
                        <div style={{backgroundColor:"gainsboro"}}>
                            NANANANA
                        </div>
                    </Popup>
                    <button className="tag__item play red" onClick={likeClick}>
                        {post_like? <MdFavorite/> : <MdFavoriteBorder/>}
                    </button>
                </ul>
            </div>
        </article>
    </div>
    )
}
/*,
<Popup trigger={<button className="button"> Open Modal </button>} modal>
                            <span> Modal content </span>
                        </Popup>
<li className="tag__item play red">
                            <a href="#"><i className="fas fa-play mr-2"/>{header + ": " + location_text(header)}</a>
                        </li>)
 */


export default Post;
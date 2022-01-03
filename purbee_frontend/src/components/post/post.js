import * as React from 'react';
import Popup from 'reactjs-popup';
import './post.scss';
import {posts, post_types, post_api_result, post_type_api_result} from './mock_post';
import { MdFavorite, MdFavoriteBorder} from "react-icons/all";
import {useEffect, useState} from "react";


//                {fields["PlainText"].map(header => (<div className="postcard__preview-txt">{header + ": " + text(header)}</div>))}

export const Post = (props) => { // data shall contain post id, post types and post type id-name map,

    const [current_image, set_current_image] = React.useState(0);
    const [post_like, set_post_like] = React.useState(false);
    const [post_fields, set_post_fields] = React.useState([]);
    const [post_likers, set_post_likers] = React.useState([]);
    const [post_owner, set_post_owner] = useState("");
    const [post, set_post] = React.useState({});
    const [post_type, set_post_type] =  React.useState({});
    const [fields, set_fields] = React.useState({});
    const [calls_done, set_calls_done] = React.useState(false);


    useEffect(() => {//do initial api calls fetch post;
        const post_id = "fa8da556-68b5-4d4b-9ff8-040a07e93a7a" //give through props

        set_post_owner("gökberk");
        console.log(post_owner);
        console.log("xxx")

        //const post = posts[post_id]

        const post_type_id = post["post_type_id"]

        //const post_type = post_types[post_type_id];
        set_post_type(post_type_api_result);

        let post_type_fields = post_type["post_field_info_dictionaries_list"]
        let fieldss = { //each field type has an array of headers
            "PlainText": [],
            "Price": [],
            "Location": [],
            "Participation": [],
            "Images": [],
            "Date": []
        }
        post_type_fields.map(field => {
            fieldss[field["field_type"]].push(field["header"]);
        });
        set_fields(fieldss);

        set_post_fields(post["post_entries_dictionary_list"]);
        set_post_likers(post["post_liked_user_list"]);
        set_post_owner(post["post_owner_user_name"]);
        set_calls_done(true);

    }, [])
    //const images = posts[post_id]["pictures"]
    const likeClick = () => {
        set_post_like(!post_like);
    }

    console.log(post);
    const text = (header) => post_fields.find(pf => pf["header"] === header)["text"];
    const location_text = (header) => post_fields.find(pf => pf["header"] === header)["text"]; //implement location
    const price = (header) => {
        const f = post_fields.find(pf => pf["header"] === header);
        return f["amount"] + " " + f["currency"];
    };
    const date = (header) => post_fields.find(pf => pf["header"] === header)["date"]
    const locations = () => {
        let component = "";
        const location_text = (header) => post_fields.find(pf => pf["header"] === header);
        fields["Location"].map(header => {
            component += (
                <li className="tag__item play red">
                    <a href="#"><i className="fas fa-play mr-2"/>{location_text(header)}</a>
                </li>
            );
        });
        return component;
    }
    const image = (header) => post_fields.find(pf => pf["header"] === header)["image"]

    /* IMAGE PART
    * <a className="postcard__img_link">
                <img className="postcard__img" src={images[current_image]} alt="Image Title" onClick={(event) => {
                    set_current_image((current_image+1) % images.length);
                    console.log((current_image+1)%images.length)
                }}/>
                <br/>
            </a>
    * */

    return (
    !calls_done ? <div> calls are not done</div>
        :
    <div>
        <article className="postcard dark red">
            <a className="postcard__img_link">
                <img className="postcard__img" src="https://i.imgur.com/8WRRCb.png" alt="Image Title"/>
                <br/>
            </a>
            <div className="postcard__text">
                <h1 className="postcard__title red"><a href="#">{post["post_title"]}</a></h1>
                <div className="postcard__subtitle small">
                    <time dateTime="2020-05-25 12:00:00">
                        <i className="fas fa-calendar-alt mr-2"/>Creator: <a href="asd">{post["post_owner_user_name"]}<br/></a>
                        {fields["Date"].map(header => (<i className="postcard__preview-txt-onur">+{header + ": " + date(header)}<br/></i>))}
                        {fields["Price"].map(header => (<i className="fas fa-calendar-alt mr-2">{"+" + header + ": " + price(header)}<br/></i>))}

                    </time>
                </div>
                <div className="postcard__bar"/>

                {fields["PlainText"].map(header => (<i className="postcard__preview-txt-onur">{header + ": " + text(header)}</i>))}

                <ul className="postcard__tagbox">
                    {fields["Location"].map(header =>
                        (
                        <Popup
                            trigger={
                                <li className="tag__item play red">
                                    <a href="#"><i className="fas fa-play mr-2"/>{header + ": " + location_text(header)}</a>
                                </li>}
                            modal>
                            <span> LOCATION HERE </span>
                        </Popup>
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
                        <span> LIST OF LIKED USERS </span>
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
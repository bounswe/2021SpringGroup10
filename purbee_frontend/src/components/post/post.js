import * as React from 'react';
import './post.scss';
import {posts, post_types} from './mock_post';
const post_id = "fa8da556-68b5-4d4b-9ff8-040a07e93a7a"
const post_type_id = posts[post_id]["post_type_id"]
const post_type = post_types[post_type_id];
let post_type_fields = post_type["post_field_info_dictionaries_list"]
let fields = { //each field type has an array of headers
    "PlainText": [],
    "Price": [],
    "Location": [],
    "Participation": [],
    "Images": [],
    "Date": []
}
post_type_fields.map(field => {
    fields[field["field_type"]].push(field["header"]);
});

const post_fields = posts[post_id]["post_entries_dictionary_list"];
const post_likers = posts[post_id]["post_liked_user_list"]
const post_owner = posts[post_id]["post_owner_user_name"]

function textFields(){
    return (
        <div>
            {fields["PlainText"].map(header => (
                <div className="postcard__preview-txt">{text(header)}</div>
            ))}
        </div>
    )
}
const text = (header) => post_fields.find(pf => pf["header"] === header)["text"];
const location_text = (header) => post_fields.find(pf => pf["header"] === header)["text"]; //implement location
const price = (header) => {
    const f = post_fields.find(pf => pf["header"] === header);
    return f["amount"] + " " + f["currency"];
};
const date = (header) => post_fields.find(pf => pf["header"] === header)["date"]
console.log(fields["PlainText"].map(h => text(h)));
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
//                {fields["PlainText"].map(header => (<div className="postcard__preview-txt">{header + ": " + text(header)}</div>))}

console.log(typeof fields["PlainText"])
const Post = (data) => {
    const [current_image, set_current_image] = React.useState(0);
    const images = posts[post_id]["pictures"]
    return (
        <article className="postcard dark red">
            <a className="postcard__img_link" href="#">
                <img className="postcard__img" src={images[current_image]} alt="Image Title" onClick={(event) => {
                    set_current_image((current_image+1) % images.length);
                    console.log((current_image+1)%images.length)
                }}/>
            </a>
            <div className="postcard__text">
                <h1 className="postcard__title red"><a href="#">{"POST TITLE!!!!!!!!!!!"}</a></h1>
                <div className="postcard__subtitle small">
                    <time dateTime="2020-05-25 12:00:00">
                        <i className="fas fa-calendar-alt mr-2"/>Creator: <a href="asd">{posts[post_id]["post_owner_user_name"]}<br/></a>
                        {fields["Date"].map(header => (<i className="postcard__preview-txt-onur">+{header + ": " + date(header)}<br/></i>))}
                        {fields["Price"].map(header => (<i className="fas fa-calendar-alt mr-2">{"+" + header + ": " + price(header)}<br/></i>))}

                    </time>
                </div>
                <div className="postcard__bar"/>

                {fields["PlainText"].map(header => (<i className="postcard__preview-txt-onur">{header + ": " + text(header)}</i>))}

                <ul className="postcard__tagbox">
                    {fields["Location"].map(header =>
                        (<li className="tag__item play red">
                            <a href="#"><i className="fas fa-play mr-2"/>{header + ": " + location_text(header)}</a>
                        </li>))
                    }
                </ul>
            </div>
        </article>
    )
}

export const PostSeries = () => {
    //const post_components = Post(posts);
    return (
        <div>
            <section className="dark">
                <div className="container py-4">
                    <Post/>
                </div>
            </section>
        </div>
    );
}

export default PostSeries;
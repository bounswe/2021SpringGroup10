import React from "react";
import './post.scss';
import {posts} from './mock_post';

const post = posts[1];

const Post = (data) => {
    return (
        <article className="postcard dark red">
            <a className="postcard__img_link" href="#">
                <img className="postcard__img" src={post.fields.pictureList[0].text} alt="Image Title"/>
            </a>
            <div className="postcard__text">
                <h1 className="postcard__title red"><a href="#">{post.post_title}</a></h1>
                <div className="postcard__subtitle small">
                    <time dateTime="2020-05-25 12:00:00">
                        <i className="fas fa-calendar-alt mr-2"></i>{post.fields.dateList[0].text}
                    </time>
                </div>
                <div className="postcard__bar"></div>
                <div className="postcard__preview-txt">{post.fields.plainTextList[0].text}
                </div>
                <ul className="postcard__tagbox">
                    <li className="tag__item play red">
                        <a href="#"><i className="fas fa-play mr-2"></i>{post.fields.locations[0].header}</a>
                    </li>
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
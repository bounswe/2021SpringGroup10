import * as React from "react";
import Post from "../post/post"
export const PostSeries = (props) => {
    //const post_components = Post(posts);
    // do api call, get post ids and initialize posts with their ids
    const id_list = props.id_list;
    return (
        <div>
            <section className="dark">
                <div className="container py-4">
                    {id_list.map(id => <Post post_id={id}/>)}
                </div>
            </section>
        </div>
    );
}

export default PostSeries;
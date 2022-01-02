import * as React from "react";
import Post from "../post/post"
export const PostSeries = () => {
    //const post_components = Post(posts);
    // do api call, get post ids and initialize posts with their ids
    return (
        <div>
            <section className="dark">
                <div className="container py-4">
                    <Post/>
                    <Post/>
                    <Post/>
                </div>
            </section>
        </div>
    );
}

export default PostSeries;
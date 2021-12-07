class Post {
    constructor(post_id, post_type, post_owner_id, community_id, post_date,
                like_list, discussion, notification_list){//for posts recieved from db
        this.post_id = post_id;
        this.post_type = post_type;
        this.post_owner_id = post_owner_id;
        this.community_id = community_id;
        this.post_date = post_date;
        this.like_list = like_list;
        this.discussion = discussion;
        this.notification_list = notification_list;
    }
    increment_like(registered_user){
        this.like_list.push(registered_user);
        //TODO: API calls
    }
    notify_user(){
        //TODO
    }
    append_subscriber(){
        //TODO
    }
    post_in_community(){
        //TODO
    }
    append_to_discussion(){
        //TODO
    }
    participate(){
        //TODO: what to participate?
    }
}

class PostType{
    constructor(post_fields, post_type_id, post_type_name,
                like_enabled, comment_enabled, community_id){
        this.post_fields = post_fields;
        this.post_type_id = post_type_id;
        this.post_type_name = post_type_name;
        this.like_enabled = like_enabled;
        this.comment_enabled = comment_enabled;
        this.community_id = community_id;
    }

}
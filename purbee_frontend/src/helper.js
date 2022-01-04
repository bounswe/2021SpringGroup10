import Axios from "axios";

export function apiCall(api_name, request_json){
    let url_part;
    let call_type;
    switch (api_name){
        case "sign up":
            url_part = "sign_up";
            call_type = "POST";
            break;
        case "sign in":
            url_part = "sign_in";
            call_type = "POST";
            break;
        case "profile page":
            url_part = "profile_page";
            call_type = "POST";
            break;
        case "get post":
            url_part = "post/";
            call_type = "PUT";
            break;
    }

    let headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'DELETE, GET, OPTIONS, POST, PUT',
        'Access-Control-Allow-Headers': 'Authorization, Content-Type, Access-Control-Allow-Headers, X-Requested-With, Access-Control-Allow-Origin'
    };
    let endpoint = "https://cz2qlmf16e.execute-api.us-east-2.amazonaws.com/dev/api/" + url_part
    Axios({
        headers: headers,
        method: call_type,
        url: endpoint,
        data: request_json,
    }).then(response => {
        console.log(response)
        return response;
    })
        .catch(error=> console.log(error));
}

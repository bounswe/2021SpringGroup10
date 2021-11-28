export async function apiCall(url, call_method){
    const response = await fetch(url, {
        method: call_method,
        mode: "cors",
        headers:{
            "Content-type": "application/json"
        },
    });
    const my_json = await response.json();
    return my_json;
}

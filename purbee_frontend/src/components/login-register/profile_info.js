import * as React from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import './styles.css'
import DatePicker from '@mui/lab/DatePicker';
import LocalizationProvider from '@mui/lab/LocalizationProvider';
import AdapterDateFns from '@mui/lab/AdapterDateFns';
import FileBase64 from 'react-file-base64';
import { getUser } from '../../utils/common';
import {base_url, headers} from "../../utils/url"
import { useNavigate } from "react-router-dom";
const Axios = require('axios');

export default function ProfileInfo() {
    const [first_name, set_first_name] = React.useState("");
    const [last_name, set_last_name] = React.useState("");
    const [bio, set_bio] = React.useState("");
    const [birth_date, set_birth_date] = React.useState("");
    const [photo, set_photo] = React.useState("https://t3.ftcdn.net/jpg/03/46/83/96/360_F_346839683_6nAPzbhpSkIpb8pmAwufkC7c5eD7wYws.jpg");
    const [loading, setLoading] = React.useState(false);
    const [error, setError] = React.useState(null);

    let navigate = useNavigate()

    const handle_save = () => {
        setError(null);
        setLoading(true);
        const request_json = {
            "user_name": "Aayysy123"
            // 'profile_photo': photo,
            // 'bio': bio,
            // 'first_name': first_name,
            // 'last_name': last_name,
            // 'birth_date': birth_date
        };

        Axios({
            headers: headers,
            method: "POST",
            url: base_url + 'profile_page/',
            data: request_json,
        }).then(response => {
            
            setLoading(false)
            navigate('/home')
        }).catch(error => {
            
            setLoading(false)
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
                console.log(error.request);
            } else {
                // Something happened in setting up the request that triggered an Error
                console.log('Error', error.message);
            }
            //setError(error.response.data.response_message)
        })
    }

    return (
        <div className="App">
            <form className="form">
                <img src={photo} style={{ width: "25%", alignSelf: "center", paddingBottom: "0.8em" }}></img>

                <h4 style={{ alignSelf: "baseline" }}>First Name: </h4>
                <div style={{ height: "0.8em" }}></div>
                <TextField
                    id="first_name"
                    formControlProps={{
                        fullWidth: true
                    }}
                    type="text"
                    onChange={(e) => set_first_name(e.target.value)}
                />
                <div style={{ height: "0.8em" }}></div>
                <h4 style={{ alignSelf: "baseline" }}>Last Name:</h4>
                <div style={{ height: "0.8em" }}></div>
                <TextField
                    id="last_name"
                    formControlProps={{
                        fullWidth: true
                    }}
                    onChange={(e) => set_last_name(e.target.value)}
                />

                <div style={{ height: "0.8em" }}></div>
                <h4 style={{ alignSelf: "baseline" }}>Birth Date:</h4>
                <div style={{ height: "0.8em" }}></div>
                <LocalizationProvider dateAdapter={AdapterDateFns}>
                    <DatePicker
                        value={birth_date}
                        onChange={(newValue) => {
                            set_birth_date(newValue);
                        }}
                        renderInput={(params) => <TextField {...params} />}
                    />
                </LocalizationProvider>
                <div style={{ height: "0.8em" }}></div>
                <h4 style={{ alignSelf: "baseline" }}>Bio:</h4>
                <div style={{ height: "0.8em" }}></div>
                <TextField
                    id="bio"
                    multiline={true}
                    minRows="5"
                    formControlProps={{
                        fullWidth: true
                    }}
                    onChange={(e) => set_bio(e.target.value)}
                />
                <div style={{ height: "0.8em" }}></div>
                <h4 style={{ alignSelf: "baseline" }}>Profile Picture:</h4>
                <div style={{ height: "0.8em" }}></div>
                <FileBase64
                    multiple={false}
                    onDone={(t) => {set_photo(t.base64)}} />
                <Button
                    variant="contained"
                    color="primary"
                    className="form__custom-button"
                    onClick={handle_save}>
                    {loading ? "Loading..." : "Save"}
                </Button>
                {error && <><small style={{ color: 'red' }}>{error}</small><br /></>}<br />
                {/* <Button
                    variant="contained"
                    color="primary"
                    className="form__custom-button"
                    onClick={handle_skip}>
                    <RouterLink to="/home"> Skip </RouterLink>
                </Button> */}
            </form>


        </div >
    )
}
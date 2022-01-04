import * as React from 'react';
import Button from '@mui/material/Button';
import '../login-register/styles.css'
import DatePicker from '@mui/lab/DatePicker';
import LocalizationProvider from '@mui/lab/LocalizationProvider';
import AdapterDateFns from '@mui/lab/AdapterDateFns';
import FileBase64 from 'react-file-base64';
import { getUser } from '../../utils/common';
import {base_url, headers} from "../../utils/url"
import { useNavigate } from "react-router-dom";
import { useParams } from 'react-router-dom'
import Header from "../homepage/header";
// import GoogleMapField from './google_map';
// import Feed from '../feed/feed'
import {
    Grid,
    TextField,
    Typography,
    Switch,
    Chip,
    OutlinedInput
} from '@material-ui/core';
const Axios = require('axios');

const AdvancedSearch = () => {
    const [search_text, set_search_text] = React.useState("");
    const [min_price, set_min_price] = React.useState(0);
    const [max_price, set_max_price] = React.useState(0);
    const [currency, set_currency] = React.useState("TL");
    const [starting_date, set_starting_date] = React.useState("");
    const [ending_date, set_ending_date] = React.useState("");
    const [starting_time, set_starting_time] = React.useState("");
    const [ending_time, set_ending_time] = React.useState("");
    const [min_participation, set_min_participation] = React.useState(0);
    const [max_participation, set_max_participation] = React.useState(0);
    const [post_ids, set_post_ids] = React.useState([])

    const [longitude, set_longitude] = React.useState(0)
    const [latitude, set_latitude] = React.useState(0)
    const [radius, set_radius] = React.useState(0)

    const [loading, setLoading] = React.useState(false);

    const { community_id } = useParams()

    const handle_save = () => {
        setLoading(true)
        const request_json = {
            "user_name": getUser(),
            "community_id": community_id,
            "search_dictionary": {
                "PlainText": {"search_text":search_text},
                "Price" : {"min_price" : min_price, "max_price":max_price, "currency":currency},
                "Location" : {"longitude":-77.0364, "latitude":30, "radius":1000}, 
                "DateTime" : {"starting_date": starting_date , "ending_date":ending_date, "starting_time": starting_time , "ending_time":ending_time},
                "Participation" : {"min_participation" : min_participation, "max_participation" : max_participation}
            }
        };
        console.log(request_json)

        Axios({
            headers: headers,
            method: "PUT",
            url: base_url + 'advanced_search',
            data: request_json,
        }).then(response => {
            
            setLoading(false)
            console.log(response.data.post_ids)
            set_post_ids(response.data.post_ids)
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
            <Header />
            <h3>Advanced Search for {community_id}</h3>
            <form className="form">

                <h4 style={{ alignSelf: "baseline" }}>Search Text: </h4>
                <div style={{ height: "0.8em" }}></div>
                <TextField
                    id="search_text"
                    formControlProps={{
                        fullWidth: true
                    }}
                    type="text"
                    value={search_text}
                    onChange={(e) => set_search_text(e.target.value)}
                />
                <div style={{ height: "0.8em" }}></div>
                <h4 style={{ alignSelf: "baseline" }}>Min Price:</h4>
                <div style={{ height: "0.8em" }}></div>
                <TextField
                    id="min_price"
                    formControlProps={{
                        fullWidth: true
                    }}
                    type="number"
                    value={min_price}
                    onChange={(e) => set_min_price(e.target.value)}
                />
                <h4 style={{ alignSelf: "baseline" }}>Max Price:</h4>
                <div style={{ height: "0.8em" }}></div>
                <TextField
                    id="max_price"
                    formControlProps={{
                        fullWidth: true
                    }}
                    type="number"
                    value={max_price}
                    onChange={(e) => set_max_price(e.target.value)}
                />
                <h4 style={{ alignSelf: "baseline" }}>Currency:</h4>
                <TextField
                    id="currency"
                    formControlProps={{
                        fullWidth: true
                    }}
                    type="text"
                    value={currency}
                    onChange={(e) => set_currency(e.target.value)}
                />

                <div style={{ height: "0.8em" }}></div>
                <h4 style={{ alignSelf: "baseline" }}>Starting Date:</h4>
                <div style={{ height: "0.8em" }}></div>
                <TextField
                    id="starting_date"
                    formControlProps={{
                        fullWidth: true
                    }}
                    placholder="DD/MM/YYYY"
                    type="text"
                    onChange={(e) => set_starting_date(e.target.value)}
                />
                <h4 style={{ alignSelf: "baseline" }}>Ending Date:</h4>
                <div style={{ height: "0.8em" }}></div>
                <TextField
                    id="ending_date"
                    formControlProps={{
                        fullWidth: true
                    }}
                    placholder="DD/MM/YYYY"
                    type="text"
                    onChange={(e) => set_ending_date(e.target.value)}
                />
                <div style={{ height: "0.8em" }}></div>
                <h4 style={{ alignSelf: "baseline" }}>Starting Time:</h4>
                <div style={{ height: "0.8em" }}></div>
                <TextField
                    id="starting_time"
                    formControlProps={{
                        fullWidth: true
                    }}
                    placholder="HH:MM"
                    type="text"
                    onChange={(e) => set_starting_time(e.target.value)}
                />
                <h4 style={{ alignSelf: "baseline" }}>Ending Time:</h4>
                <div style={{ height: "0.8em" }}></div>
                <TextField
                    id="ending_time"
                    formControlProps={{
                        fullWidth: true
                    }}
                    placholder="HH:MM"
                    type="text"
                    onChange={(e) => set_ending_time(e.target.value)}
                />
                <h4 style={{ alignSelf: "baseline" }}>Min Participation:</h4>
                <div style={{ height: "0.8em" }}></div>
                
                <TextField
                    id="min_particiaption"
                    formControlProps={{
                        fullWidth: true
                    }}
                    type="number"
                    onChange={(e) => set_min_participation(e.target.value)}
                />
                <h4 style={{ alignSelf: "baseline" }}>Max Participation:</h4>
                <div style={{ height: "0.8em" }}></div>

                <TextField
                    id="max_particiaption"
                    formControlProps={{
                        fullWidth: true
                    }}
                    type="number"
                    onChange={(e) => set_max_participation(e.target.value)}
                />

                {/* <Grid
                    item
                    xs={12}
                    sm={12}
                >
                    <Typography
                        color="textPrimary"
                        sx={{ mb: 1 }}
                        variant="subtitle1"
                        align="left"
                    >
                        {mapListField.header}
                    </Typography>
                    <GoogleMapField setLocation={setLocation} location={location} />
                </Grid> */}
                
                <Button
                    variant="contained"
                    color="primary"
                    className="form__custom-button"
                    onClick={handle_save}>
                    {loading ? "Loading..." : "Save"}
                </Button>
                
            </form>
            
            {/* <Feed id_list = {post_ids} /> */}

        </div >
    )

}

export default AdvancedSearch
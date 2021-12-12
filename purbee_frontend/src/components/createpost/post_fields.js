import {
    Grid,
    TextField,
    Typography,
    Switch,
    Chip,
    OutlinedInput
} from '@material-ui/core';
import DateTimePicker from '@mui/lab/DateTimePicker';
import LocalizationProvider from '@mui/lab/LocalizationProvider';
import AdapterDateFns from '@mui/lab/AdapterDateFns';
import { useEffect, useState } from 'react';
import GoogleMapField from './google_map';
import InputAdornment from '@mui/material/InputAdornment';


export const PostFields = (props) => {

    const community = props.community;
    const postType = props.post_type;
    const [currentOption, setCurrentOption] = useState("");
    const [plainTexts, setPlainTexts] = useState([]);
    const [dates, setDates] = useState([]);
    const [pollOptions, setPollOptions] = useState([]);
    const [prices, setPrices] = useState([]);
    const [docUrls, setDocUrls] = useState([]);
    const [docNames, setDocNames] = useState([]);
    const [photoUrls, setPhotoUrls] = useState([]);
    const [photoDescs, setPhotoDescs] = useState([]);


    const handleChangePlainTexts = (newValue, index) => {
        let arr = plainTexts;
        arr[index] = newValue;
        setPlainTexts(arr);
    }

    const handleChangeDates = (newDate, index) => {
        let arr = dates;
        arr[index] = newDate;
        setDates(arr);
    }

    const handleAddPollOptions = (e, index) => {
        if (e.keyCode == 13) {
            let arr = pollOptions;
            if (arr[index]) {
                arr[index].push(currentOption);
            } else {
                arr[index] = [];
                arr[index].push(currentOption);
            }
            setPollOptions(arr);
            setCurrentOption("");
        }
    }

    const handleAddPrices = (price, index) => {
        let arr = prices;
        arr[index] = price;
        setPrices(arr);
    }

    const handleChangeDocUrls = (url, index) => {
        let arr = docUrls;
        arr[index] = url;
        setDocUrls(arr);
    }

    const handleChangeDocNames = (name, index) => {
        let arr = docNames;
        arr[index] = name;
        setDocNames(arr);
    }

    const handleChangePhotoUrls = (url, index) => {
        let arr = docUrls;
        arr[index] = url;
        setPhotoUrls(arr);
    }

    const handleChangePhotoDescs = (name, index) => {
        let arr = docNames;
        arr[index] = name;
        setPhotoDescs(arr);
    }


    console.log(prices)
    if (!community || !postType) return <></>;

    else {
        console.log(postType);
        return (
            <Grid
                container
                style={{ paddingTop: "20px" }}
                spacing={3}
            >

                {postType.fields.plainTextList.map((plainTextField, index) => (
                    <Grid
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
                            {plainTextField.header}
                        </Typography>
                        <TextField onChange={(e) => { handleChangePlainTexts(e.target.value, index) }} variant="outlined" fullWidth />
                    </Grid>
                ))}

                {postType.fields.dateList.map((dateListField, index) => (
                    <Grid
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
                            {dateListField.header}
                        </Typography>
                        <LocalizationProvider dateAdapter={AdapterDateFns}>
                            <DateTimePicker
                                value={dates[index]}
                                onChange={(e) => { handleChangeDates(e, index) }}
                                renderInput={(params) => <TextField variant="outlined" fullWidth {...params} />} />
                        </LocalizationProvider>
                    </Grid>
                ))}

                {postType.fields.locationList.map((dateListField, index) => (
                    <Grid
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
                            {dateListField.header}
                        </Typography>
                        <GoogleMapField />
                    </Grid>
                ))}

                {postType.fields.pollsList.map((pollsField, index) => (
                    <Grid
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
                            {pollsField.header}
                        </Typography>
                        <TextField value={currentOption} helperText={"Press Enter To Add Options"} onChange={(e) => { setCurrentOption(e.target.value) }} onKeyDown={(e) => { handleAddPollOptions(e, index) }} variant="outlined" fullWidth />
                        {pollOptions[index]?.map(option => (
                            <Chip label={option}></Chip>
                        ))}
                    </Grid>
                ))}

                {postType.fields.pricesList.map((priceField, index) => (
                    <Grid
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
                            {priceField.header}
                        </Typography>
                        <OutlinedInput
                            id={`price${index}`}
                            fullWidth
                            type="number"
                            onChange={(e) => { handleAddPrices(e.target.value, index) }}
                            startAdornment={<InputAdornment position="start">$</InputAdornment>}
                        />
                    </Grid>
                ))}

                {postType.fields.documentList.map((documentField, index) => (
                    <Grid
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
                            {documentField.header}
                        </Typography>
                        <TextField helperText="Document Name" onChange={(e) => { handleChangeDocNames(e.target.value, index) }} variant="outlined" fullWidth />
                        <TextField helperText="Document Url" onChange={(e) => { handleChangeDocUrls(e.target.value, index) }} variant="outlined" fullWidth />
                    </Grid>
                ))}

                {postType.fields.photoList.map((photoField, index) => (
                    <Grid
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
                            {photoField.header}
                        </Typography>
                        <TextField helperText="Photo Description" onChange={(e) => { handleChangePhotoDescs(e.target.value, index) }} variant="outlined" fullWidth />
                        <TextField helperText="Photo Url" onChange={(e) => { handleChangePhotoUrls(e.target.value, index) }} variant="outlined" fullWidth />
                    </Grid>
                ))}

            </Grid>


        )
    }

}

export default PostFields;
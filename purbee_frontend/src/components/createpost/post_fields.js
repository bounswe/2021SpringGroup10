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
import PollsList from './polls_list';


export const PostFields = (props) => {

    const community = props.community;
    const postType = props.post_type;
    const [plainTexts, setPlainTexts] = useState([]);
    const [dates, setDates] = useState([]);
    const [location, setLocation] = useState();
    const [pollOptions, setPollOptions] = useState([]);
    const [prices, setPrices] = useState([]);
    const [docUrls, setDocUrls] = useState([]);
    const [docNames, setDocNames] = useState([]);
    const [photoUrls, setPhotoUrls] = useState([]);
    const [photoDescs, setPhotoDescs] = useState([]);
    const [allFields, setAllFields] = useState({});
    const [currentDate, setCurrentDate] = useState()
    const [dateIndex, setDateIndex] = useState()

    const handleChangePlainTexts = (newValue, index) => {
        let arr = plainTexts;
        arr[index] = newValue;
        setPlainTexts(arr);

        let all = allFields;
        all.plainTexts = arr;
        setAllFields(all);
    }

    const handleChangeDates = (newDate, index) => {
        setCurrentDate(newDate)
        setDateIndex(index)
    }


    useEffect(() => {
        let arr = dates;
        arr[dateIndex] = currentDate;
        setDates(arr);

        let all = allFields;
        all.dates = arr;
        setAllFields(all);
    }, [currentDate])


    const handleAddPrices = (price, index) => {
        let arr = prices;
        arr[index] = price;
        setPrices(arr);

        let all = allFields;
        all.prices = arr;
        setAllFields(all);
    }

    const handleChangeDocUrls = (url, index) => {
        let arr = docUrls;
        arr[index] = url;
        setDocUrls(arr);

        let all = allFields;
        all.docUrls = arr;
        setAllFields(all);
    }

    const handleChangeDocNames = (name, index) => {
        let arr = docNames;
        arr[index] = name;
        setDocNames(arr);

        let all = allFields;
        all.docNames = arr;
        setAllFields(all);
    }

    const handleChangePhotoUrls = (url, index) => {
        let arr = photoUrls;
        arr[index] = url;
        setPhotoUrls(arr);

        let all = allFields;
        all.photoUrls = arr;
        setAllFields(all);
    }

    const handleChangePhotoDescs = (name, index) => {
        let arr = photoDescs;
        arr[index] = name;
        setPhotoDescs(arr);

        let all = allFields;
        all.photoDescs = arr;
        setAllFields(all);
    }

    useEffect(() => {
        if(location){
            let all = allFields;
            all.location = location;
            setAllFields(all);
        }
    }, [location])

    useEffect(() => {
        if(pollOptions.length){
            let all = allFields;
            all.pollOptions = pollOptions;
            setAllFields(all);
        }
    }, [pollOptions])


    useEffect(() => {
        props.setFields(allFields)
    }, [allFields])

    if (!community || !postType) return <></>;

    else {
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
                                value={currentDate}
                                onChange={(e) => { handleChangeDates(e, index) }}
                                renderInput={(params) => <TextField variant="outlined" fullWidth {...params} />} />
                        </LocalizationProvider>
                    </Grid>
                ))}

                {postType.fields.locationList.map((mapListField, index) => (
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
                            {mapListField.header}
                        </Typography>
                        <GoogleMapField setLocation={setLocation} location={location} />
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
                        <PollsList setPollOptions={setPollOptions} />
                        
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
import React, { useEffect } from 'react';
import {Checkbox, FormControl, makeStyles, TextField} from "@material-ui/core";
import {Autocomplete} from "@mui/lab";
import CheckBoxOutlineBlankIcon from "@material-ui/icons/CheckBoxOutlineBlank";
import CheckBoxIcon from "@material-ui/icons/CheckBox";
import Button from "@mui/material/Button";
import SendIcon from '@mui/icons-material/Send';

const icon = <CheckBoxOutlineBlankIcon fontSize="small" />
const checkedIcon = <CheckBoxIcon fontSize="small" />
const useStyles = makeStyles((theme) => ({
    formControl: {
        margin: theme.spacing(1),
        minWidth: 120,
        maxWidth: 300,
    },
    chips: {
        display: 'flex',
        flexWrap: 'wrap',
    },
    chip: {
        margin: 2,
    },
    noLabel: {
        marginTop: theme.spacing(3),
    },
    root: {
        '& > *': {
            margin: theme.spacing(1),
        },
    },
    textField: {
        marginLeft: theme.spacing(1),
        marginRight: theme.spacing(1),
        width: 200,
    },
}));
export default function PostTypesPage(){
    const classes = useStyles();
    const [selected_fields, set_selected_fields] = React.useState([]);

    const handle_selected_fields_change = (event) => set_selected_fields(event.target.value);

    const possible_post_fields = ["Text", "Picture", "Date", "Document", "Event", "Price", "Location"]

    const post_field_drop_down =
        (<Autocomplete
        multiple
        id="checkboxes-tags-demo"
        options={possible_post_fields}
        disableCloseOnSelect
        getOptionLabel={(option) => option}
        renderOption={(props, option, { selected }) => (
            <li {...props}>
                <Checkbox
                    icon={icon}
                    checkedIcon={checkedIcon}
                    style={{ marginRight: 8 }}
                    checked={selected}
                />
                {option}
            </li>
        )}
        style={{ width: 500 }}
        renderInput={(params) => (
            <TextField {...params} label="Post Fields" placeholder="Post Fields" />
        )}
    />)
    return (
        <div>
            <TextField
                required
                id="outlined-required"
                label="Post Type Name"
                defaultValue="My Post Type"
            />
            <div>
                {post_field_drop_down}
            </div>
            <div >
                <Button variant="contained" endIcon={<SendIcon />}>
                    Create Post Type
                </Button>
            </div>
        </div>

    )
}
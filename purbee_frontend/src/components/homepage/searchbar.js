import * as React from 'react';
import Paper from '@mui/material/Paper';
import InputBase from '@mui/material/InputBase';
import IconButton from '@mui/material/IconButton';
import SearchIcon from '@mui/icons-material/Search';
import { useState } from 'react';

export default function SearchBar() {
    const [searchString, setSearchString] = useState("");

    const handleSearchStringChange = (newSearchString) => {
        setSearchString(newSearchString)
    }

    const submit = () => {
        //TODO: search happens this point
    }

    return (
        <Paper
            component="form"
            sx={{ p: '2px 4px', display: 'flex', alignItems: 'center', width: 400 }}
        >
            <InputBase
                sx={{ ml: 1, flex: 1 }}
                placeholder="Search"
                onChange={(e) => { handleSearchStringChange(e.target.value) }}
            />
            <IconButton
                type="submit"
                sx={{ p: '10px' }}
                aria-label="search"
                onClick={ () => {submit(); }}
            >
                <SearchIcon />
            </IconButton>
        </Paper>
    );
}
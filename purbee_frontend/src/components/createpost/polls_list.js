import {
    Grid,
    TextField,
    Typography,
    Switch,
    Chip,
    OutlinedInput
} from '@material-ui/core';

import { useEffect, useState } from 'react';

export const PollsList = (props) => {

    const [currentOption, setCurrentOption] = useState("");
    const [pollOptions, setPollOptions] = useState([]);

    const handleAddPollOptions = (e) => {
        if (e.keyCode == 13) {
            let arr = pollOptions;
            if (arr) {
                arr.push(currentOption);
            } else {
                arr = [];
                arr.push(currentOption);
            }
            setPollOptions(arr);
            props.setPollOptions(arr);
            setCurrentOption("");

        }
    }


    return (

        <>
            <TextField value={currentOption} helperText={"Press Enter To Add Options"} onChange={(e) => {setCurrentOption(e.target.value)}} onKeyDown={(e) => { handleAddPollOptions(e) }} variant="outlined" fullWidth />
            {pollOptions.map(option => (
                <Chip label={option}></Chip>
            ))}
        </>
    );
}


export default PollsList
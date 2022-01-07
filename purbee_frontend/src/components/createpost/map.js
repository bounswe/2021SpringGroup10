import React, { Component } from 'react';
import {
    withGoogleMap,
    withScriptjs,
    GoogleMap,
    Marker,
    InfoWindow
} from 'react-google-maps';
import {
    Box,
    Button,
    Grid,
    Link,
    MenuItem,
    Select,
    TextField,
    Typography,
    Switch,
    Chip,
    OutlinedInput,
    IconButton
} from '@material-ui/core';
import PlacesAutocomplete, {
    geocodeByAddress,
    getLatLng
} from 'react-places-autocomplete';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import CircularLocation from '../GenericLoading';
import SearchIcon from '@mui/icons-material/Search';

class Map extends Component {
    constructor(props) {
        super(props);

        this.state = {
            isOpen: false,
            coords: (props.location) ? props.location : { lat: 41.0860808, lng: 29.045524 },
            address: '',
            selectedName: (props.location) ? 'N: ' + props.location.lat + " , S: " + props.location.lng  : ''
        };
    }
    handleChange = address => {
        this.setState({ address });
    };

    handleSelect = (address) => {
        geocodeByAddress(address)
            .then(results => getLatLng(results[0]))
            .then(latLng => {
                this.setState({
                    coords: latLng,
                })
                this.props.setLocation(latLng);
            }
            )
            .catch(error => console.error('Error', error));
    };

    handleChangeName = (suggestion) => {
        this.setState({
            selectedName: suggestion.formattedSuggestion.mainText
        })
    }

    handleToggleOpen = () => {
        this.setState({
            isOpen: true
        });
    };

    handleToggleClose = () => {
        this.setState({
            isOpen: false
        });
    };

    render() {
        const GoogleMapExample = withGoogleMap(props => (
            <GoogleMap defaultCenter={this.state.coords} defaultZoom={13}>
                <Marker
                    key={this.props.index}
                    position={this.state.coords}
                    onClick={() => this.handleToggleOpen()}
                >
                    {this.state.isOpen && (
                        <InfoWindow
                            onCloseClick={this.props.handleCloseCall}
                            options={{ maxWidth: 100 }}
                        >
                            <span>This is InfoWindow message!</span>
                        </InfoWindow>
                    )}
                </Marker>
            </GoogleMap>
        ));


        return (
            <div>
                <PlacesAutocomplete
                    value={this.state.address}
                    onChange={this.handleChange}
                    onSelect={this.handleSelect}
                >
                    {({
                        getInputProps,
                        suggestions,
                        getSuggestionItemProps,
                        loading
                    }) => {
                        return (
                            <div style={{paddingBottom: "10px"}}>
                                {(this.state.selectedName ? (
                                    <div style={{display: "flex", justifyContent: "space-between", alignItems: "center"}}>
                                        <Typography color="textPrimary"
                                            sx={{ mb: 1 }}
                                            variant="subtitle2" >{this.state.selectedName}
                                        </Typography>
                                        <IconButton onClick={() => {this.setState({selectedName: "", address: ""})}}><SearchIcon /></IconButton>
                                    </div>
                                ) : (
                                    <OutlinedInput
                                        fullWidth
                                        variant="outlined"
                                        endAdornment={<LocationOnIcon />}
                                        {...getInputProps({
                                            placeholder: 'Search Places',
                                            className: 'location-search-input',

                                        })}
                                    />
                                ))}
                                <div className="autocomplete-dropdown-container">
                                    {loading && <CircularLocation />}
                                    {suggestions.map(suggestion => {
                                        const className = suggestion.active
                                            ? 'suggestion-item--active'
                                            : 'suggestion-item';
                                        const style = suggestion.active
                                            ? { backgroundColor: '#fafafa', cursor: 'pointer' }
                                            : { backgroundColor: '#ffffff', cursor: 'pointer' };
                                        return (
                                            <div
                                                {...getSuggestionItemProps(suggestion, {
                                                    className,
                                                    style
                                                })}
                                                key={suggestion.placeId}
                                            >
                                                <MenuItem onClick={() => { this.handleChangeName(suggestion) }} style={{ color: "#000" }}>{suggestion.formattedSuggestion.mainText}</MenuItem>
                                            </div>
                                        );
                                    })}
                                </div>
                            </div>
                        )
                    }
                    }
                </PlacesAutocomplete>
                <GoogleMapExample
                    containerElement={<div style={{ height: "500px", width: "100%" }} />}
                    mapElement={<div style={{ height: `100%` }} />}
                />
            </div>
        );
    }
}

export default Map;
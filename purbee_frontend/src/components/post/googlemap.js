import * as React from 'react';
import GoogleMapReact from 'google-map-react';
import {ImLocation} from "react-icons/all";

const AnyReactComponent = ({ text }) => <div><ImLocation style={{color: "red"}}/> <i style={{color: "red"}}>LOCATION</i> </div>

export const Map = (props) => {

    const defaultProps = {
        center: {
            lat: 39.8951,
            lng: -77.0364
        },
        zoom: 8
    };
    const gkey = 'AIzaSyDqatrPkZebWGnKiLybd4nNFzERwmQCSCI';
    return (
        // Important! Always set the container height explicitly
        <div style={{ height: '50vh', width: '50%' }}>
            <GoogleMapReact
                bootstrapURLKeys={{ key: gkey }}
                defaultCenter={defaultProps.center}
                defaultZoom='8'
            >
                <AnyReactComponent
                    lat={39.8951}
                    lng={-77.0364}
                    text="My Marker"
                />
            </GoogleMapReact>
        </div>
    );
}
export default Map;
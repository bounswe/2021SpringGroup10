import React, { Component, useEffect } from 'react';
import { withScriptjs } from 'react-google-maps';
import Map from './map';

export const GoogleMap = (props) => {
  const MapLoader = withScriptjs(Map);

  const key = "AIzaSyDqatrPkZebWGnKiLybd4nNFzERwmQCSCI";

  const googleMapUrl = `https://maps.googleapis.com/maps/api/js?key=${key}&libraries=places`;

  return (
    <MapLoader
      googleMapURL={googleMapUrl}
      loadingElement={<div style={{ height: `100%` }} />}
      setLocation={props.setLocation}
      location={props.location}
    />
  );
};


export default GoogleMap;
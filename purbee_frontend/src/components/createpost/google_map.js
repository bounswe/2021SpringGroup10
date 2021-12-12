import React, { Component } from 'react';
import { withScriptjs } from 'react-google-maps';
import Map from './map';

export const GoogleMap = () => {
  const MapLoader = withScriptjs(Map);

  return (
    <MapLoader
      googleMapURL="https://maps.googleapis.com/maps/api/js?key=AIzaSyDqatrPkZebWGnKiLybd4nNFzERwmQCSCI&libraries=places"
      loadingElement={<div style={{ height: `100%` }} />}
    />
  );
};


export default GoogleMap;
import React, { Component } from 'react';
import { withScriptjs } from 'react-google-maps';
import Map from './map';

export const GoogleMap = () => {
  const MapLoader = withScriptjs(Map);
  const key = process.env.GOOGLE_MAP_KEY;
  const googleMapUrl = `https://maps.googleapis.com/maps/api/js?key=${key}&libraries=places`;

  return (
    <MapLoader
      googleMapURL={googleMapUrl}
      loadingElement={<div style={{ height: `100%` }} />}
    />
  );
};


export default GoogleMap;
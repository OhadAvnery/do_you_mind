import React, { Component } from 'react';
import {API_ROOT_URL} from '../../constants';

export function get_topic(user_id, timestamp, topic) {
    var path = API_ROOT_URL + "/users/" + user_id + "/snapshots/" + timestamp + "/" + topic;
    fetch(path)
    .then(async response => {
            const data = await response.json();

            // check for error response
            if (!response.ok) {
                // get error message from body or default to response statusText
                const error = (data && data.message) || response.statusText;
                return Promise.reject(error);
            }
            console.log("our path: "+path);
            return data;
    })   
    .catch(error => {
            this.setState({ errorMessage: error.toString() });
            console.log(error.toString());
            //console.error('There was an error!', error);
        });  
}
    


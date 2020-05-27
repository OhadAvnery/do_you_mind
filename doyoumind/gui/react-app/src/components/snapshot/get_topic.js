import React, { Component } from 'react';
import {API_ROOT_URL} from '../../constants';

//NOTE- here we make the fetch synchronic, to make it easier to may a few GETs in a row.
export function get_topic(user_id, timestamp, topic, dict) {
    var path = API_ROOT_URL + "/users/" + user_id + "/snapshots/" + timestamp + "/" + topic;
    fetch(path)
    //.then(response => response.json())
    .then(response => {
        //console.log(String(response));
        response.json();
    })
    .then(
        (result) => {
            console.log("result for "+topic+": "+result);
            dict[topic] = result;
          
        },
        // Note: it's important to handle errors here
        // instead of a catch() block so that we don't swallow
        // exceptions from actual bugs in components.
        (error) => {
            console.log(error.toString());
            console.error('There was an error!', error);
            dict[topic] = null;
        })

    /*
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
        */
}
    


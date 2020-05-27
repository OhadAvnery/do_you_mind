import React, { Component } from 'react';
import {renderTopic} from './render_topic'; 
import {API_ROOT_URL, BIG_DATA_TOPICS} from '../../constants';



class SnapshotTopic extends Component {
    state = {'data': {}, 'loaded':false};
    user_id = this.props.user_id;
    timestamp = this.props.timestamp;
    topic = this.props.topic;
    

    mountBigData() {
    var path = API_ROOT_URL + "/users/" + this.user_id + "/snapshots/" + this.timestamp + "/" + this.topic + "/data";

    fetch(path)
    .then(async response => {
        const data = await response.blob();
        if (!response.ok) {
                // get error message from body or default to response statusText
                const error = (data && data.message) || response.statusText;
                return Promise.reject(error);
        }
        
        var url = URL.createObjectURL(data);

        console.log("mountBigData: got a response");
        this.setState({ data: url, loaded:true });
    })   
    .catch(error => {
            this.setState({ errorMessage: error.toString() });
            console.log(error.toString());
            console.error('There was an error!', error);
        });  
    }
    

    componentDidMount() {
    // Runs after the first render() lifecycle
    if(BIG_DATA_TOPICS.includes(this.topic)) {
        //console.log(this.topic + " is in mountBigData");
        this.mountBigData();
        return;
    }
    //console.log(this.topic + " isn't in mountBigData");
    var path = API_ROOT_URL + "/users/" + this.user_id + "/snapshots/" + this.timestamp + "/" + this.topic;

    fetch(path)
    .then(async response => {
            const data = await response.json();

            // check for error response
            if (!response.ok) {
                // get error message from body or default to response statusText
                const error = (data && data.message) || response.statusText;
                return Promise.reject(error);
            }
            console.log("got a response!");
            this.setState({ data: data, loaded:true });
    })   
    .catch(error => {
            this.setState({ errorMessage: error.toString() });
            console.log(error.toString());
            console.error('There was an error!', error);
        });  
    }


    

    render() {
        if(!this.state.loaded) {
            return <div>Waiting for {this.topic} to load...</div>
        }
        console.log("our topic is: "+this.topic);
        //console.log("our render is: "+ String(this.renders[this.topic]));
        //return (this.renders[this.topic](this.state.data));
        return renderTopic(this.topic, this.state.data);
    }

}

export default SnapshotTopic;
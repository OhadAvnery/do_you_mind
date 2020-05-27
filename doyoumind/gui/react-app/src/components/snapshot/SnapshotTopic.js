import React, { Component } from 'react';
import {API_ROOT_URL} from '../../constants';


class SnapshotTopic extends Component {
    state = {'data': {}, 'loaded':false};
    user_id = this.props.user_id;
    timestamp = this.props.timestamp;
    topic = this.props.topic;
    

    componentDidMount() {
    // Runs after the first render() lifecycle
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

    render_feelings= function(data) {
        console.log("render_feelings: our topic- "+this.topic);
        console.log("render_feelings: our object- "+this);
        return (<div>{data['hunger']}</div>);
    }

    render_pose= function(data) {
        console.log("render_pose: our topic- "+this.topic);
        return null;
        //return (<div>{String(data['translation']['x'])}</div>);
    }

    render_color_image= function(data) {
        return (<div>color_image</div>);
    }

    render_depth_image= function(data) {
        return (<div>depth_image</div>);
    }

    renders = ({'feelings': this.render_feelings, 'pose': this.render_pose, 
    'color_image': this.render_color_image, 'depth_image': this.render_depth_image}) 

    render() {
        if(!this.state.loaded) {
            return <div>Waiting for {this.topic} to load...</div>
        }
        console.log("our topic is: "+this.topic);
        //console.log("our render is: "+ String(this.renders[this.topic]));
        //return (this.renders[this.topic](this.state.data));
        var topic_render = function(data) {return this.renders[this.topic](data);} 
        return this.topic_render(this.state.data);
    }

}

export default SnapshotTopic;
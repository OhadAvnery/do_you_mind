import React, { Component } from 'react';
import Header from '../main/Header';
import {API_ROOT_URL} from '../../constants';
import {get_topic} from './get_topic';


class SnapshotPage extends Component {
    /**topics- list of all the names of the topics.
    topics_data- a dictionary, key=name of topic, value=its data.
    */
    state = {topics: [], topics_data: {}};
    user_id = this.props.match.params.user_id;
    timestamp = this.props.match.params.timestamp;

    componentDidMount() {
    // Runs after the first render() lifecycle
    var path = API_ROOT_URL + "/users/" + this.user_id + "/snapshots/" + this.timestamp;

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
            this.setState({ topics: data });
    })   
    .catch(error => {
            this.setState({ errorMessage: error.toString() });
            console.log(error.toString());
            //console.error('There was an error!', error);
        });  


    }

    render() {
    var not_loaded = (<div>Waiting for snapshot's data to load...</div>);
    var topics = this.state.topics;
    if(!topics) {
        return not_loaded;
    }

    var result = [];
    result.push(
      <div className="App">
        <Header title={"Snapshot by User #"+this.user_id} />
        available topics are: {String(this.state.topics)}
      </div>
    );

    var data; 
    var topic;
    for (var i = 0; i < topics.length; i++) {
        topic = topics[i];
        data = get_topic(this.user_id, this.timestamp, topic);
        if(!data) {
            return not_loaded;
        }
        result.push(<div>{String(data)}</div>);
    }

    return (result);
    }

}

export default SnapshotPage;
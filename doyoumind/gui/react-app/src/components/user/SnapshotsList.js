import React, { Component } from 'react';
import {API_ROOT_URL} from '../../constants';

export function snaps_block(snaps_list, user_id) {
   
   //sorting the users list by increasing timestamp
    snaps_list.sort();
    var result = [];
    for (var i = 0; i < snaps_list.length; i++) {
        result.push(<SingleSnapshot user_id={user_id} index={i+1} timestamp={snaps_list[i]}/>);
    }
    return result;
}

class SingleSnapshot extends Component {
    render() {
        var timestamp = this.props.timestamp;
        var index = this.props.index;
        var date = new Date(timestamp*1000);
        var user_id = this.props.user_id;
        return (
        <div>
        {/** <a href={"/users/"+user_id+"/"+timestamp}> #{val} - {date.toString()}</a> */}
        <a href={"/users/"+user_id+"/"+timestamp}> #{index} - {date.toString()}</a>
        <br />
        </div>
        );
    }
}

class SnapshotsList extends Component {
    state = {snaps: null};
    id = this.props.user_id;


    componentDidMount() {
    // Runs after the first render() lifecycle
    var path = API_ROOT_URL + "/users/" + this.id + "/snapshots";
    
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
            this.setState({ snaps: data });

    })   
    .catch(error => {
            this.setState({ errorMessage: error.toString() });
            console.error('There was an error!', error);
        });  
    }


    render() {
    var snaps = this.state.snaps;
    if (!snaps) {
        return (<div>Waiting for snapshots list to load...</div>);
    }
    return (
      <div className="App">
        {snaps_block(snaps, this.id)}
      </div>
    );
    }
}
/**
class SingleSnapshot extends Component {

    render() {
        var user = this.props.user;
        var user_id = user['user_id'];
        var username = user['username'];
        return (
        <div>
        <a href={"/users/"+user_id}> User {'#'+user_id}'s page- {username}</a>
        <br />
        </div>
        );
    }
}*/

/**
export function users_index(users_list) {
   //sorting the users list by increasing user ID
    users_list.sort((u1, u2) => u1['user_id']-u2['user_id']);
    var result = [];
    for (var i = 0; i < users_list.length; i++) {
        result.push(<SingleUser user={users_list[i]}/>);
    }
    return result;
}*/

export default SnapshotsList;
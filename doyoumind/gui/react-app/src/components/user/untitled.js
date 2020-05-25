import React, { Component } from 'react';


class SnapshotsList extends Component {
    state = {snaps: null};
    render() {
        
    }
}
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
}

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
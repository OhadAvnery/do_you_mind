import React, { Component } from 'react';
//import logo from './logo.svg';
import Header from '../main/Header';
import {API_ROOT_URL} from '../../constants';
import './UsersPage.css';

class SingleUser extends Component {
    render() {
        var user = this.props.user;
        var user_id = user['user_id'];
        var username = user['username'];
        return (
        <div>
        <a href={"/users/"+user_id}> User {'#'+user_id}- {username}</a>
        <br />
        </div>
        );
    }
}

function users_index(users_list) {
    //sorting the users list by increasing user ID
    users_list.sort((u1, u2) => u1['user_id']-u2['user_id']);
    var result = [];
    for (var i = 0; i < users_list.length; i++) {
        result.push(<SingleUser user={users_list[i]}/>);
    }
    return result;
}
class UsersPage extends Component {
    state = {users: null};
    
    componentDidMount() {
    // Runs after the first render() lifecycle
    var path = API_ROOT_URL + "/users";
    
    fetch(path)
    .then(async response => {
            const data = await response.json();

            // check for error response
            if (!response.ok) {
                // get error message from body or default to response statusText
                const error = (data && data.message) || response.statusText;
                return Promise.reject(error);
            }
            this.setState({ users: data });
    })   
    .catch(error => {
            this.setState({ errorMessage: error.toString() });
            console.error('There was an error!', error);
        });  
    }
    

  render() {
    var users_list = this.state.users;
    if (!users_list) {
        return (<div>Waiting for users list to load...</div>);
    }
    return (
      <div className="App">
        <Header title="Users Page" />
        <a href="/">Go back to the main page</a> <br /> <br />
        Here are all the users: <br /> 
        {users_index(users_list)}
      </div>
    );
  }
}

export default UsersPage;
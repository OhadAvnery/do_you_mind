import React, { Component } from 'react';
import Header from '../main/Header';
import SnapshotsList from './SnapshotsList';
import {API_ROOT_URL} from '../../constants';
import './UserPage.css';

function calculate_age(birthday) {
    /*
    Given a Date object representing the person's birthday, 
    return their age.
    Source: https://stackoverflow.com/a/21984136/8477065
    */
    var ageDifMs = Date.now() - birthday.getTime();
    var ageDate = new Date(ageDifMs); // miliseconds from epoch
    return Math.abs(ageDate.getUTCFullYear() - 1970);
}
class UserPage extends Component {
    state = {user_data: null};

    id = this.props.match.params.user_id;
    componentDidMount() {
    // Runs after the first render() lifecycle
    var path = API_ROOT_URL + "/users/" + this.id;

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
            this.setState({ user_data: data });
    })   
    .catch(error => {
            this.setState({ errorMessage: error.toString() });
            console.log(error.toString());
            //console.error('There was an error!', error);
        });  
    }

    render() {
    //var id = this.props.match.params.user_id;
    var user_data = this.state.user_data;
    if (!user_data) {
        return (<div>Waiting for user's data to load...</div>);
    }
    var username = user_data['username'];
    var birthday = user_data['birthday'];
    var date = new Date(birthday*1000);
    //var current_year = Date.now().getFullYear();
    //var age = current_year -date.getFullYear();
    var gender = user_data['gender'];
    var gender_path = `${process.env.PUBLIC_URL}/imgs/genders/${gender}.png`;
    console.log('gender_path: '+gender_path);
    return (
      <div className="App">
        <Header title={"User #"+this.id} />
        <a href="/users">Go back to users page</a><br /><br />
        <h2>Who is user {'#'+this.id} anyway?</h2>
        USERNAME - {username} <br />
        BIRTHDAY- {date.toDateString()} ({calculate_age(date)} years old)<br />
        GENDER- {gender} 
        <img class='gender' src={gender_path} alt={gender} title={gender}/><br /> <br/>
        <h2>And what are his snapshots?</h2>
        {<SnapshotsList user_id={this.id} />} 


      </div>
    );
    }
}

export default UserPage;
//export {UserPage};
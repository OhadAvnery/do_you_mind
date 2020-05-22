import React, { Component } from 'react';
import Header from '../main/Header';
import './UserPage.css';

class UserPage extends Component {
  render() {
    var id = this.props.match.params.user_id;
    return (
      <div className="App">
        <Header title={"User #"+id} />
        Here's the info about the user:
      </div>
    );
  }
}

export default UserPage;
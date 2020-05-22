import React, { Component } from 'react';
import '../../App.css';

class Header extends Component {
  render() {
    return (

        <div className="App-header">
          <img className="App-logo" src={`${process.env.PUBLIC_URL}/imgs/logo.png`} width="150" height="150"/>
          <h1>{this.props.title}</h1>
        </div>
    );
  }
}

export default Header;
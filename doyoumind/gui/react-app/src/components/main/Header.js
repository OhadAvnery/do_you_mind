import React, { Component } from 'react';
import '../../App.css';
//import logo from '/imgs/logo.png';

class Header extends Component {
  render() {
    return (
        <div className="App-header">
          <img className="App-logo" src='/imgs/logo.png'
          alt="logo" title="hello, future visitors!" width="150" height="150"/>
          <h1>{this.props.title}</h1>
        </div>
    );
  }
}

export default Header;
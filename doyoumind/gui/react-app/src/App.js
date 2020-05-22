import React, { Component } from 'react';
//import logo from './logo.svg';
import RandomVideo from './components/RandomVideo';
import './App.css';

var videos = [
    'http://www.youtube.com/embed/ehB6462JHog', //mind
    'http://www.youtube.com/embed/49FB9hhoO6c', //where is my mind
    'http://www.youtube.com/embed/ibZdil-Kbjw', //boingo- grey matter
    'http://www.youtube.com/embed/bVYXWVs0Prc', //mind games
    'http://www.youtube.com/embed/BgK_Er7WZVg', //mind mischief
    'http://www.youtube.com/embed/BhYKN21olBw', //brain damage
];

class App extends Component {
  render() {
    return (
      <div className="App">
        <div className="App-header">
          {/*<img src={logo} className="App-logo" alt="logo" />*/}
          <img className="App-logo" src={`${process.env.PUBLIC_URL}/imgs/logo.png`} width="150" height="150"/>
          <h2>Do You Mind?</h2>
        </div>
        <p className="App-intro">
          Welcome to the new generation! <br />
          A tool, that reads your mind and parses it! <br />
          How wonderful! <br />
        </p>
        <a href="/users">List of users</a> 
        <br/><br/><br/><br/>
        <h2>Mind music:</h2>
        <RandomVideo links={videos}/>

      </div>


    );
  }
}


      
//

export default App;

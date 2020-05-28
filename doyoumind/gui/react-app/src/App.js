import React, { Component } from 'react';
//import logo from './logo.svg';
import RandomVideo from './components/RandomVideo';
import Header from './components/main/Header';
import './App.css';

var videos = [
    'http://www.youtube.com/embed/ehB6462JHog', //talking heads- mind
    'http://www.youtube.com/embed/PK-k0kCSJcM', //yoko ono- mind train
    'http://www.youtube.com/embed/49FB9hhoO6c', //where is my mind?
    'http://www.youtube.com/embed/7TUPAXliAIM', //prodigy- mindfields
    'http://www.youtube.com/embed/bVYXWVs0Prc', //mind games
    'http://www.youtube.com/embed/BgK_Er7WZVg', //mind mischief
];

class App extends Component {
  render() {
    return (
      <div className="App">
        <Header title="Do You Mind?" />


        <p className="App-intro">
          Welcome to the new generation! <br />
          A tool, that reads your mind and parses it! <br />
          How wonderful! <br />
        </p>
        <a href="/users">List of users</a> 
        <br/><br/><br/><br/>
        <h2>Mind music:</h2>
        <RandomVideo links={videos} text='new song'/>

      </div>


    );
  }
}


export default App;

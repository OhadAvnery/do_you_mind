import React, { Component } from 'react';
import './RandomVideo.css';



/*<div class="video_container">
        <iframe class='video' src={links[index]}></iframe>*/

function refreshPage(){
    window.location.reload();
} 

class RandomVideo extends Component {
    

  render() {
    var links = this.props.links;
    var index = Math.floor(Math.random() * links.length);
    return (       
        <div>
        <button type="submit" font-size="50px" onClick={refreshPage}>Reload</button>
        <br/>
        <iframe height='450' width='800' src={links[index]}></iframe>
        </div>
    );
  }
}


export default RandomVideo;

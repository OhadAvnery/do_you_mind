import React, { Component } from 'react';
import './render_topic.css';

function round_floats_dict(dict, num_digits=4) {
    /*given a dictionary with floats as values,
    rounds all the values up to num_digits significant digits.
    */
    for(var ind in dict) {
        var val = dict[ind];
        dict[ind] = +(val).toPrecision(num_digits);
    }
}

class FeelsImg extends Component {
    render() {
        /*
        num- a float between -1 and 1 (1 is the best).
        Convert it to a number between 1-6, and return an appropiate path
        for an image representing the feel.
        */
        console.log("calling feelsImg");
        var feels = [null, 'awful', 'real bad', 'bad', 'meh', 'good', 'great'];
        var num = this.props.num;
        var n = Math.floor(num*3) + 4; //an int between 1 and 7, inclusive
        if(n===7) {n -= 1;} //handling the odd case where num==1
        var path = `${process.env.PUBLIC_URL}/imgs/feelings/${n}.png`;
        console.log(path);
        return (<img src={path} alt={feels[n]} title={feels[n]}/>);
    }
}

function render_feelings(data) {
    round_floats_dict(data);
    var table = (<table>
        <tr>
    <th>feeling →</th>
    <th>hunger</th> 
    <th>thirst</th>
    <th>exhaustion</th> 
    <th>happiness</th>
  </tr>
  <tr>
    <th>value (-1 to 1)</th>
    <td>{data.hunger}</td> 
    <td>{data.thirst}</td>
    <td>{data.exhaustion}</td>
    <td>{data.happiness}</td>
  </tr>
  <tr>
    <th>visual</th>
    <td><FeelsImg num={data.hunger} /></td> 
    <td><FeelsImg num={data.thirst} /></td>
    <td><FeelsImg num={data.exhaustion} /></td> 
    <td><FeelsImg num={data.happiness} /></td>
  </tr></table>);
    return (
        <div>
        <h2 class="feelings">FEELINGS</h2>
        {table}
        </div>
        );
}

function render_pose(data) {
    var trans = data.translation;
    round_floats_dict(trans);
    var rot = data.rotation;
    round_floats_dict(rot);
    var table = (
    <table>
    <tr>
    <th>field ↓</th>
    <th>x</th> 
    <th>y</th>
    <th>z</th> 
    <th>w</th>
    </tr>
    <tr>
    <th>translation</th>
    <td>{trans.x}</td>
    <td>{trans.y}</td>
    <td>{trans.z}</td>
    <td class='unavailable'>X</td>
    </tr>
  <tr>
    <th>rotation</th>
    <td>{rot.x}</td>
    <td>{rot.y}</td>
    <td>{rot.z}</td>
    <td>{rot.w}</td>
  </tr></table>);

 return (
    <div>
    <h2 class="pose">POSE</h2>
    {table}
    </div>
    );
}

function render_color_image(data) {
    return (
        <div>
        <h2 class="color_image">COLOR IMAGE</h2>
        <img class="color_image" src={data} />
        </div>
        );
}

function render_depth_image(data) {
    return (
        <div>
        <h2 class="depth_image">DEPTH IMAGE</h2>
        <img class="depth_image" src={data} />
        </div>
        );

}

var renders = ({'feelings': render_feelings, 'pose': render_pose, 
    'color_image': render_color_image, 'depth_image': render_depth_image})

export function renderTopic(topic, data) {
    return renders[topic](data);
}

//import JSON;
import React, { Component } from 'react';

function render_feelings(data) {
    return(<div>{JSON.stringify(data)}</div>);
}

function render_pose(data) {
    return(<div>{JSON.stringify(data)}</div>);
}

function render_color_image(data) {
    return(<div><img width="500" height="500" src={data} /></div>);
}

function render_depth_image(data) {
    //var url = JSON.stringify(data);
    return(<div><img src={data} /></div>);

}

var renders = ({'feelings': render_feelings, 'pose': render_pose, 
    'color_image': render_color_image, 'depth_image': render_depth_image})

export function renderTopic(topic, data) {
    return renders[topic](data);
}

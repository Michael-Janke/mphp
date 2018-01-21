import React, { Component } from "react";

export default class RunDescription extends Component {
  render() {
    const { algorithms, algorithm } = this.props;
    return (
      <div>
        parameters: <span>{Object.keys(algorithm.parameters).map((param) => algorithms[algorithm.key].parameters[param].name + ":" + algorithm.parameters[param]).join(', ')}</span> |
        cancer types: <span>{algorithm.cancerTypes.join(', ')}</span> |
        healthy tissue: <span>{algorithm.healthyTissueTypes.join(', ')}</span> |
        sick tissue: <span>{algorithm.sickTissueTypes.join(', ')}</span> 
      </div>
    );
  }
}
import React, { Component } from "react";

export default class Evaluation extends Component {
  render() {
    console.log(this.props);
    return (
      <div>
        <h3>Evaluation</h3>
        <p>{`Precision for sick classification with selected genes: ${
          this.props.sick.classification.decisionTree.precision.mean
        }`}</p>
      </div>
    );
  }
}

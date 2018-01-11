import React, { Component } from "react";
import styled from "styled-components";

export default class Parameters extends Component {
  render() {
    const { selectedAlgorithm, algorithms } = this.props;
    const parameters = algorithms.find(x => x.key === selectedAlgorithm.key)
      .parameters;
    return (
      <div>
        {Object.keys(selectedAlgorithm.parameters).map(param => {
          return (
            <div key={param}>
              {parameters.find(x => x.key === param).name}
              : {selectedAlgorithm.parameters[param]}
            </div>
          );
        })}
      </div>
    );
  }
}

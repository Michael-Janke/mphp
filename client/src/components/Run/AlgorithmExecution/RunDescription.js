import React, { Component } from "react";
import styled from "styled-components";

export default class RunDescription extends Component {
  render() {
    const { algorithms, algorithm } = this.props;
    return (
      <StyledContent>
        parameters: <span>{Object.keys(algorithm.parameters).map((param) => algorithms[algorithm.key].parameters[param].name + ":" + algorithm.parameters[param]).join(', ')}</span> |
        cancer types: <span>{algorithm.cancerTypes.join(', ')}</span> |
        healthy tissue: <span>{algorithm.healthyTissueTypes.join(', ')}</span> |
        sick tissue: <span>{algorithm.sickTissueTypes.join(', ')}</span> 
      </StyledContent>
    );
  }
}

const StyledContent = styled.div`
  margin-left: 16px;
  margin-right: 16px;
`;

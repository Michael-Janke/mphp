import React, { Component } from "react";
import styled from "styled-components";

export default class RunDescription extends Component {
  render() {
    const { algorithms, algorithm } = this.props;
    return (
      <StyledContent>
        {Object.keys(algorithm.parameters).map(param => (
          <span key={param}>
            <StyledText>
              {algorithms[algorithm.key].parameters[param].name}
            </StyledText>
            {": " + algorithm.parameters[param] + " "}
          </span>
        ))}
        <StyledText>Cancer types: </StyledText>
        <span>{algorithm.cancerTypes.join(", ")}</span>
        {Object.keys(algorithm.healthyTissueTypes).length !== 0 ? (
          <span>
            <StyledText> Healthy tissue: </StyledText>
            {algorithm.healthyTissueTypes.join(", ")}
          </span>
        ) : null}
        {Object.keys(algorithm.sickTissueTypes).length !== 0 ? (
          <span>
            <StyledText> Sick tissue: </StyledText>
            {algorithm.sickTissueTypes.join(", ")}
          </span>
        ) : null}
      </StyledContent>
    );
  }
}

const StyledContent = styled.div`
  margin-left: 16px;
  margin-right: 16px;
  font-size: 0.8em;
`;

const StyledText = styled.span`
  color: ${props => props.theme.darkGray};
`;

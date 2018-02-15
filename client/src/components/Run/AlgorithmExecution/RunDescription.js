import React, { Component } from "react";
import styled from "styled-components";

export default class RunDescription extends Component {
  render() {
    const { algorithms, algorithm, datasets, dataset } = this.props;
    return (
      <StyledContent>
        <Row>
          <GrayText>Dataset: </GrayText>
          {datasets[dataset]}
          <GrayText>, Cancer types: </GrayText>
          <span>{algorithm.cancerTypes.join(", ")}</span>
          {Object.keys(algorithm.healthyTissueTypes).length !== 0 ? (
            <span>
              <GrayText>, Healthy tissue: </GrayText>
              {algorithm.healthyTissueTypes.join(", ")}
            </span>
          ) : null}
          {Object.keys(algorithm.sickTissueTypes).length !== 0 ? (
            <span>
              <GrayText>, Sick tissue: </GrayText>
              {algorithm.sickTissueTypes.join(", ")}
            </span>
          ) : null}
        </Row>
        <Row>
          {algorithms[algorithm.key].parameters.map((param, index) => (
            <span key={param.key}>
              <GrayText>
                {`${index === 0 ? "" : ", "}${
                  param.name
                  }: `}
              </GrayText>
              {algorithm.parameters[param.key]}
            </span>
          ))}
          {this.props.oneAgainstRest ? <GrayText>, </GrayText> : null}
          {this.props.oneAgainstRest ? "One against rest" : ""}
        </Row>
      </StyledContent>
    );
  }
}

const StyledContent = styled.div`
  margin-left: 16px;
  margin-right: 16px;
  font-size: 0.8em;
  display: flex;
  flex-direction: column;
`;

const Row = styled.div`
  margin-top: ${props => props.theme.smallSpace};
`;

const GrayText = styled.span`
  color: ${props => props.theme.darkGray};
`;

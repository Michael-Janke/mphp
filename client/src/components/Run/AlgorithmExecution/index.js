import React, { Component } from "react";
import RaisedButton from "material-ui/RaisedButton";
import styled from "styled-components";

import DataSelection from "./DataSelection";
import AlgorithmSelection from "./AlgorithmSelection";

export default class AlgorithmExecution extends Component {
  render() {
    const isRunnable = this.isRunnable();
    return (
      <div>
        <AlgorithmSelection {...this.props} />
        <DataSelection {...this.props} />
        <CardActions>
          {this.props.disabled ? null : (
            <StyledButton
              title={
                isRunnable
                  ? `Run ${this.props.algorithm.name}`
                  : `Please select an algorithm`
              }
              label="Run"
              primary={true}
              onClick={() => {
                this.executeAlgorithm();
              }}
              disabled={!isRunnable}
            />
          )}
        </CardActions>
      </div>
    );
  }

  isRunnable() {
    return typeof this.props.algorithm.key !== "undefined";
  }

  executeAlgorithm() {
    this.props.runAlgorithm(this.props.runId, this.props.algorithm);
  }
}

const CardActions = styled.div`
  margin-top: ${props => props.theme.smallSpace};
  display: flex;
  flex-direction: row-reverse;
`;

const StyledButton = styled(RaisedButton)`
  && {
    margin: 12px;
  }
  button {
    background: ${props => props.theme.boringBlue} !important;
  }
  button:disabled {
    background: ${props => props.theme.lightGray} !important;
  }
`;

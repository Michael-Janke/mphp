import React, { Component } from "react";
import RaisedButton from "material-ui/RaisedButton";
import styled from "styled-components";

import DataSelection from "./DataSelection";
import AlgorithmSelection from "./AlgorithmSelection";

export default class AlgorithmExecution extends Component {
  render() {
    const { statistics, tcgaTokens, tissueTypes } = this.props;
    const selectedAlgorithm = this.getSelectedAlgorithm();
    const isRunnable = this.isRunnable();
    return (
      <div>
        <AlgorithmSelection
          selectedAlgorithm={selectedAlgorithm}
          isRunnable={isRunnable}
          {...this.props}
        />
        <DataSelection {...{ statistics, tcgaTokens, tissueTypes }} />
        <CardActions>
          <StyledButton
            title={
              isRunnable
                ? `Run ${selectedAlgorithm.name}`
                : `Please select an algorithm`
            }
            label="Run"
            primary={true}
            onClick={() => {
              this.executeAlgorithm();
            }}
            disabled={!isRunnable}
          />
        </CardActions>
      </div>
    );
  }

  isRunnable() {
    return this.getSelectedAlgorithm() !== null;
  }

  getSelectedAlgorithm() {
    const { key } = this.props.algorithm;
    return !key
      ? null
      : this.props.algorithms.find(algorithm => algorithm.key === key);
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

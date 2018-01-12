import React, { Component } from "react";
import styled from "styled-components";

import Plot from "./Plot";
import Evaluation from "./Evaluation";
import GeneExploration from "./GeneExplorationContainer";

export default class Results extends Component {
  render() {
    const { result, runId } = this.props;
    return (
      <div>
        {!result.isError ? (
          <StyledContent>
            <Plot {...result} />
            <Evaluation />
            <GeneExploration runId={runId} result={result} />
          </StyledContent>
        ) : (
          <div>Server error</div>
        )}
      </div>
    );
  }
}

const StyledContent = styled.div`
  margin: 16px;
`;

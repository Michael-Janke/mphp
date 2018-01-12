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
        <StyledContent>
          <Plot {...result} />
          <Evaluation />
          <GeneExploration runId={runId} result={result} />
        </StyledContent>
      </div>
    );
  }
}

const StyledContent = styled.div`
  margin: 16px;
`;

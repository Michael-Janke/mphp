import React, { Component } from "react";
import styled from "styled-components";

import Card from "../Card";
import Plot from "../Results/Plot";
import Evaluation from "../Results/Evaluation";
import GeneExploration from "../Results/GeneExplorationContainer";

export default class Results extends Component {
  render() {
    return (
      <StyledRoot>
        {Object.keys(this.props.runs).map(runId => {
          const run = this.props.runs[runId];
          return (
            <StyledCard
              title={`Results for ${run.params.name}`}
              isLoading={!run.result}
              isError={run.result && run.result.isError}
              key={`run-${runId}`}
            >
              <StyledContent>
                <Plot {...run.result} />
                <Evaluation />
                <GeneExploration result={run.result} />
              </StyledContent>
            </StyledCard>
          );
        })}
      </StyledRoot>
    );
  }
}

const StyledCard = styled(Card)`
  flex: 1;
`;

const StyledRoot = styled.div`
  width: 100%;
`;

const StyledContent = styled.div`
  margin: 16px;
`;

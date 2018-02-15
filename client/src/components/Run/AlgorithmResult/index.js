import React, { Component } from "react";
import styled from "styled-components";
import { Tabs, Tab } from "material-ui/Tabs";
import { FormattedMessage } from "react-intl";

import Plot from "./Plot";
import Evaluation from "./Evaluation";
import GeneExploration from "./GeneExplorationContainer";
import EvaluationValue from "./EvaluationValue";
import { sunYellow, slightlyBoringBlue } from "../../../config/colors";

export default class Results extends Component {
  render() {
    const { result } = this.props;
    return (
      <Container>
        {!result.isError ? this.renderContent() : <div>Server error</div>}
      </Container>
    );
  }

  renderContent() {
    const { result, oneAgainstRest } = this.props;
    const tabData = Object.keys(result)
      .filter(key => key !== "meanFitness")
      .reduce((reduced, key) => ({ ...reduced, [key]: result[key] }), {});
    return oneAgainstRest ? (
      <div>
        <Row>
          <StyledExplanation>{<FormattedMessage id="General.OneAgainstRestResult" />}</StyledExplanation>
          <StyledEvaluationValue
            primaryText={result.meanFitness}
            secondaryText="Mean fitness score"
          />
        </Row>
        <Tabs inkBarStyle={{ backgroundColor: sunYellow }}>
          {Object.keys(tabData).map(label => (
            <Tab
              key={`tab-${label}`}
              label={label}
              style={{ backgroundColor: slightlyBoringBlue }}
            >
              {this.renderResult(tabData[label], label)}
            </Tab>
          ))}
        </Tabs>
      </div>
    ) : (
        this.renderResult(result)
      );
  }

  renderResult(result, label = "") {
    // skip evaluation score
    if (typeof result === "number") return null;

    const { runId, oneAgainstRest } = this.props;
    return (
      <StyledContent>
        <Columns>
          <Plot
            {...result}
            oneAgainstRest={oneAgainstRest}
            cancerType={label}
          />
          <Evaluation {...result.evaluation} />
        </Columns>
        <GeneExploration
          runId={runId}
          oneAgainstRest={oneAgainstRest}
          cancerType={label}
          {...result}
        />
      </StyledContent>
    );
  }
}

const Container = styled.div`
  padding: ${props => props.theme.mediumSpace};
`;

const Row = styled.div`
  display: flex;
  flex-direction: row;
`;

const StyledExplanation = styled.div`
  font-size: 14px;  
  margin-right: 50px;
`;

// remove background on hover
const StyledEvaluationValue = styled(EvaluationValue) `
  background: none !important;
  div {
    padding-left: 0 !important;
    padding-top: 0 !important;
    cursor: default !important;
  }
  text-align: right;
`;

const StyledContent = styled.div`
  margin: 16px;
`;

const Columns = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-around;
`;

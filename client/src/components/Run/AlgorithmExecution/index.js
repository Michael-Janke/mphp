import React, { Component } from "react";
import RaisedButton from "material-ui/RaisedButton";
import styled from "styled-components";
import { FormattedMessage } from "react-intl";
import HelpIcon from "material-ui/svg-icons/action/help-outline";

import TooltipBox from "../../TooltipBox";
import DataSelection from "./DataSelection";
import AlgorithmSelection from "./AlgorithmSelection";
import SubsetSelection from "./SubsetSelection";
import RunDescription from "./RunDescription";

export default class AlgorithmExecution extends Component {
  render() {
    const isRunnable = this.isRunnable();
    return (
      <div>
        {!this.props.disabled ? (
          <Row>
            <AlgorithmSelection {...this.props} />
            <SubsetSelection {...this.props} />
            <DataSelection {...this.props} />
          </Row>
        ) : (
            <RunDescription {...this.props} />
          )}
        <CardActions>
          {this.props.disabled ? null : (
            <StyledButtonContainer>
              <TooltipBox
                text={<FormattedMessage id="General.Run" />}
                position="top"
              >
                <HelpIcon />
              </TooltipBox>
              <StyledButton
                title={
                  isRunnable
                    ? `Run ${this.props.algorithm.name}`
                    : `Please select appropriate parameters`
                }
                label="Run"
                primary={true}
                onClick={() => {
                  this.executeAlgorithm();
                }}
                disabled={!isRunnable}
              />
            </StyledButtonContainer>
          )}
        </CardActions>
      </div>
    );
  }

  isRunnable() {
    const algorithm = this.props.algorithm;
    const statistics = this.props.statistics[this.props.dataset];

    const algorithmSelected = typeof algorithm.key !== "undefined";
    const cancerTypeSelected = algorithm.cancerTypes.length !== 0;
    const tissueTypeSelected =
      algorithm.healthyTissueTypes.length !== 0 ||
      algorithm.sickTissueTypes.length !== 0;

    // some algorithms (norm, relief, sfs, ea) need at least one healthy and one sick tissue type
    var oneTissueTypeRunnable = true;
    if (algorithm.key !== "basic" && algorithm.key !== "tree") {
      oneTissueTypeRunnable = algorithm.healthyTissueTypes.length !== 0 && algorithm.sickTissueTypes.length !== 0;
    }

    var enoughSamples = true;
    if (!this.props.oversampling) {
      // test if there are more than 10 healthy samples for each cancer type (but only if healthy types are selected)
      if (algorithm.healthyTissueTypes.length !== 0) {
        algorithm.cancerTypes.forEach(cancerType => {
          var sum = 0;
          algorithm.healthyTissueTypes.forEach(tissueType => {
            sum += statistics.counts[cancerType][tissueType];
          });
          if (sum < 10) {
            enoughSamples = false;
          }
        });
      }
      // test if there are more than 10 sick samples for each cancer type (but only if sick types are selected)
      if (algorithm.sickTissueTypes.length !== 0) {
        algorithm.cancerTypes.forEach(cancerType => {
          var sum = 0;
          algorithm.sickTissueTypes.forEach(tissueType => {
            sum += statistics.counts[cancerType][tissueType];
          });
          if (sum < 10) {
            enoughSamples = false;
          }
        });
      }
    }

    var oneCancerTypeRunnable = true;
    // if only one cancer type is selected, only some algorithms (feature selection + decision tree) are allowed and
    // at least 10 healthy samples and 10 sick samples are necessary
    if (algorithm.cancerTypes.length === 1) {
      const currentAlgorithm = algorithm.key;
      const currentCancerType = algorithm.cancerTypes[0];
      var sumHealthy = 0;
      algorithm.healthyTissueTypes.forEach(x => {
        sumHealthy += statistics.counts[currentCancerType][x];
      });
      var sumSick = 0;
      algorithm.sickTissueTypes.forEach(x => {
        sumSick += statistics.counts[currentCancerType][x];
      });
      oneCancerTypeRunnable =
        (currentAlgorithm === "basic" || currentAlgorithm === "tree") &&
        sumHealthy >= 10 &&
        sumSick >= 10;
    }

    return (
      algorithmSelected &&
      cancerTypeSelected &&
      tissueTypeSelected &&
      oneTissueTypeRunnable &&
      enoughSamples &&
      oneCancerTypeRunnable
    );
  }

  executeAlgorithm() {
    this.props.startRun(
      this.props.runId,
      this.props.oneAgainstRest,
      this.props.oversampling,
      {
        ...this.props.algorithm,
        dataset: this.props.dataset
      }
    );
  }
}

const Row = styled.div`
  display: flex;
  flex-direction: row;
`;

const CardActions = styled.div`
  margin-top: ${props => props.theme.smallSpace};
  display: flex;
  flex-direction: row-reverse;
`;

const StyledButtonContainer = styled.div`
  display: flex;
  align-items: center;
`;

const StyledButton = styled(RaisedButton) `
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

import React, { Component } from "react";
import { List } from "material-ui/List";
import styled from "styled-components";
import { FormattedMessage } from "react-intl";
import EvaluationValue from "./EvaluationValue";
import TooltipBox from "../../TooltipBox";
import HelpIcon from "material-ui/svg-icons/action/help-outline";
import KeyboardArrowDown from "material-ui/svg-icons/hardware/keyboard-arrow-down";

export default class Evaluation extends Component {
  constructor(props) {
    super(props);
    this.state = { openScore: null };
  }

  render() {
    const { fitness, sick, healthy } = this.props;
    const hasHealthy = fitness && sick && healthy;
    return hasHealthy ? (
      <List>
        {this.renderFitnessScore(0)}
        {this.renderSickScore(1)}
        {this.renderHealthyScore(2)}
      </List>
    ) : (
        <List>
          {this.renderScore(
            this.classificationScoreParameters(
              this.props.classification.decisionTree
            )
          )}
        </List>
      );
  }

  renderFitnessScore(index) {
    const {
      combinedFitness,
      clusteringFitness,
      classificationFitness,
      sickVsHealthyFitness
    } = this.props.fitness;

    const parameters = {
      primaryText: combinedFitness,
      secondaryText: "Fitness",
      description: "CombinedFitness",
      nestedItems: [
        {
          key: "classification-fitness",
          primaryText: classificationFitness,
          secondaryText: "Classification fitness"
        },
        {
          key: "clustering-fitness",
          primaryText: clusteringFitness,
          secondaryText: "Clustering fitness"
        },
        {
          key: "sickVsHealthy-fitness",
          primaryText: sickVsHealthyFitness,
          secondaryText: "Sick vs. healthy fitness"
        }
      ],
      index
    };

    return this.renderScore(parameters);
  }

  renderSickScore(index) {
    const scores = this.props.sick.classification.decisionTree;
    const parameters = {
      ...this.classificationScoreParameters(scores, "for sick", "Sick"),
      index
    };
    return this.renderScore(parameters);
  }

  renderHealthyScore(index) {
    const scores = this.props.healthy.classification.decisionTree;
    const parameters = {
      ...this.classificationScoreParameters(scores, "for healthy", "Healthy"),
      index
    };
    return this.renderScore(parameters);
  }

  classificationScoreParameters(scores, postfix = "", descriptionPostifx) {
    return {
      primaryText: scores.f1.mean,
      secondaryText: `F1 score ${postfix}`,
      description: `F1${descriptionPostifx}`,
      nestedItems: [
        {
          key: "precision",
          primaryText: scores.precision.mean,
          secondaryText: "Precision"
        },
        {
          key: "recall",
          primaryText: scores.recall.mean,
          secondaryText: "Recall"
        }
      ]
    };
  }

  renderScore(parameters) {
    const {
      index,
      primaryText,
      secondaryText,
      nestedItems,
      description
    } = parameters;
    return (
      <EvaluationValue
        open={this.state.openScore === index}
        primaryText={primaryText}
        secondaryText={secondaryText}
        rightAvatar={
          <StyledTooltipBox
            text={<FormattedMessage id={`Evaluation.${description}`} />}
          >
            <HelpIcon />
            <KeyboardArrowDown />
          </StyledTooltipBox>
        }
        onNestedListToggle={() => this.toggleOpenScore(index)}
        nestedItems={nestedItems.map(nestedItem => (
          <EvaluationValue {...nestedItem} />
        ))}
      />
    );
  }

  toggleOpenScore(index) {
    const openScore = this.state.openScore === index ? null : index;
    this.setState({ openScore });
  }
}

const StyledTooltipBox = styled(TooltipBox) `
  float: right;
`;

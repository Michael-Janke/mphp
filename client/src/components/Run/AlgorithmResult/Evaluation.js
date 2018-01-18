import React, { Component } from "react";
import { List } from "material-ui/List";
import EvaluationValue from "./EvaluationValue";

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
      <List>{this.renderScores(this.props)}</List>
    );
  }

  renderFitnessScore(index) {
    const {
      combinedFitness,
      clusteringFitness,
      classificationFitness
    } = this.props.fitness;

    const parameters = {
      primaryText: combinedFitness,
      secondaryText: "Fitness",
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
        }
      ],
      index
    };

    return this.renderScore(parameters);
  }

  renderSickScore(index) {
    const scores = this.props.sick.classification.decisionTree;
    const parameters = {
      ...this.classificationScoreParameters(scores, "for sick"),
      index
    };
    return this.renderScore(parameters);
  }

  renderHealthyScore(index) {
    const scores = this.props.healthy.classification.decisionTree;
    const parameters = {
      ...this.classificationScoreParameters(scores, "for healthy"),
      index
    };
    return this.renderScore(parameters);
  }

  classificationScoreParameters(scores, postfix = "") {
    return {
      primaryText: scores.f1.mean,
      secondaryText: `F1 score ${postfix}`,
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
    const { index, primaryText, secondaryText, nestedItems } = parameters;
    return (
      <EvaluationValue
        open={this.state.openScore === index}
        primaryText={primaryText}
        secondaryText={secondaryText}
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

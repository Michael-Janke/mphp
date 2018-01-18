import React, { Component } from "react";
import { List } from "material-ui/List";
import EvaluationValue from "./EvaluationValue";

export default class Evaluation extends Component {
  render() {
    const { fitness, sick, healthy } = this.props;
    const hasHealthy = fitness && sick && healthy;
    return hasHealthy ? (
      <List>
        {this.renderFitnessScore()}
        {this.renderScores(sick, " of sick data")}
        {this.renderScores(healthy, " of heahlthy data")}
      </List>
    ) : (
      <List>{this.renderScores(this.props)}</List>
    );
  }

  renderFitnessScore() {
    const {
      combinedFitness,
      clusteringFitness,
      classificationFitness
    } = this.props.fitness;
    return (
      <EvaluationValue
        primaryText={combinedFitness}
        secondaryText="Fitness"
        nestedItems={[
          <EvaluationValue
            key="classification-fitness"
            primaryText={classificationFitness}
            secondaryText="Classification fitness"
          />,
          <EvaluationValue
            key="clustering-fitness"
            primaryText={clusteringFitness}
            secondaryText="Clustering fitness"
          />
        ]}
      />
    );
  }

  renderScores({ classification, clustering }, secondaryTextPostfix = "") {
    const { f1, precision, recall } = classification.decisionTree;
    return (
      <div>
        <EvaluationValue
          primaryText={f1.mean}
          secondaryText={`F1 score${secondaryTextPostfix}`}
          nestedItems={[
            <EvaluationValue
              key="precision"
              primaryText={precision.mean}
              secondaryText="Precision"
            />,
            <EvaluationValue
              key="recall"
              primaryText={recall.mean}
              secondaryText="Recall"
            />
          ]}
        />
      </div>
    );
  }
}

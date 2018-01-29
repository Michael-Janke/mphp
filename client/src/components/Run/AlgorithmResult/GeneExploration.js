import React, { Component } from "react";

import ExpressionTable from "./utils/ExpressionTable";

export default class GeneExploration extends Component {
  constructor(props) {
    super(props);
    if (!props.runs[props.runId].geneResults) {
      // trigger the gene test once in the beginning
      this.props.testGenes(props.runId, { genes: props.genes });
    }
  }

  render() {
    const { genes, geneNames, expressionMatrix } = this.props;

    const geneResults = this.props.runs[this.props.runId].geneResults
      ? this.props.runs[this.props.runId].geneResults
      : null;

    return (
      <div>
        <h3>
          {!expressionMatrix ? "Gene Exploration" : "Gene Expression Levels"}
        </h3>
        <p>
          The following genes were especially relevant for discriminating the
          clusters:
        </p>
        <ExpressionTable
          data={{
            expressionMatrix,
            genes,
            geneNames,
            geneResults
          }}
        />
      </div>
    );
  }
}

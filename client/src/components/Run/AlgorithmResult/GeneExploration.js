import React, { Component } from "react";

import ExpressionTable from "./utils/ExpressionTable";

export default class GeneExploration extends Component {
  constructor(props) {
    super(props);
    const { runId, genes, oneAgainstRest, cancerType, testGenes } = this.props;

    if (!this.geneResults()) {
      // trigger the gene test once in the beginning
      testGenes(runId, {
        genes,
        oneAgainstRest,
        cancerType
      });
    }
  }

  render() {
    const { genes, geneNames, expressionMatrix } = this.props;

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
          {...this.props}
          data={{
            expressionMatrix,
            genes,
            geneNames,
            geneResults: this.geneResults()
          }}
        />
      </div>
    );
  }

  geneResults() {
    const { runs, runId, oneAgainstRest, cancerType } = this.props;
    const results = runs[runId].geneResults;

    if (oneAgainstRest) {
      return results && results[cancerType] ? results[cancerType] : null;
    } else {
      return results;
    }
  }
}

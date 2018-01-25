import React, { Component } from "react";
import styled from "styled-components";

import ExpressionMatrix from "./utils/ExpressionMatrix";

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

    const geneExplorationList = genes.map((gene, i) => (
      <StyledGene key={gene}>
        <a href={`https://www.proteinatlas.org/${gene}`} target="_blank">
          {geneNames[i]}
        </a>
        {geneResults && geneResults[gene].score}
      </StyledGene>
    ));

    return (
      <div>
        <h3>
          {!expressionMatrix ? "Gene Exploration" : "Gene Expression Levels"}
        </h3>
        <p>
          The following genes were especially relevant for discriminating the
          clusters:
        </p>
        {expressionMatrix ? (
          <ExpressionMatrix
            data={{
              expressionMatrix,
              genes,
              geneNames,
              geneExplorationList
            }}
          />
        ) : (
          <StyledList>{geneExplorationList}</StyledList>
        )}
      </div>
    );
  }
}

const StyledList = styled.div`
  display: flex;
  flex-wrap: wrap;
`;

const StyledGene = styled.span`
  margin: 5px;
  display: flex;
  flex-direction: column;
`;

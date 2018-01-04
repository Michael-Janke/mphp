import React, { Component } from "react";
import styled from "styled-components";

export default class GeneExploration extends Component {
  render() {
    const { genes, geneNames } = this.props.result;
    return (
      <div>
        <h3>Gene Exploration</h3>
        <p>
          The following genes were especially relevant for discriminating the
          clusters:
        </p>
        <StyledList>
          {
            genes.map((gene, i) => (
            <StyledItem key={gene}>
              <a
                href={`https://www.proteinatlas.org/${gene}`}
                target="_blank"
              >
                {geneNames[i]}
              </a>
            </StyledItem>
          ))}
        </StyledList>
      </div>
    );
  }
}

const StyledList = styled.div`
  display: flex;
  flex-wrap: wrap;
`;

const StyledItem = styled.span`
  margin: 5px;
`;

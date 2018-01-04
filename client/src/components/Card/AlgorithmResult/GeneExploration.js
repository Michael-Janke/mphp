import React, { Component } from "react";
import styled from "styled-components";

export default class GeneExploration extends Component {
  render() {
    return (
      <div>
        <h3>Gene Exploration</h3>
        <p>
          The following genes were especially relevant for discriminating the
          clusters:
        </p>
        <StyledList>
          {this.props.result.genes.map(gene => (
            <StyledItem key={gene}>
              <a
                href={`https://www.proteinatlas.org/search/${gene}`}
                target="_blank"
              >
                {gene}
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

import React, { Component } from "react";
import styled from "styled-components";
import {
  Table,
  TableBody,
  TableHeader,
  TableHeaderColumn,
  TableRow,
  TableRowColumn
} from "material-ui/Table";

export default class GeneExploration extends Component {
  constructor(props) {
    super(props);
    if (!props.runs[props.runId].geneResults) {
      this.props.testGenes(props.runId, { genes: props.result.genes });
    }
  }

  render() {
    const { genes, geneNames, expressionMatrix } = this.props.result;
    console.log(this.props.runs[this.props.runId].geneResults);

    return (
      <div>
        <h3>
          {!expressionMatrix ? "Gene Exploration" : "Gene Expression Levels"}
        </h3>
        <p>
          The following genes were especially relevant for discriminating the
          clusters:
        </p>
        {!expressionMatrix ? (
          <StyledList>
            {genes.map((gene, i) => (
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
        ) : (
          <Table bodyStyle={{ overflow: "visible" }}>
            <TableHeader displaySelectAll={false} adjustForCheckbox={false}>
              <TableRow>
                <TableHeaderColumn />
                {genes.map((gene, i) => (
                  <TableHeaderColumn key={gene}>
                    <a
                      href={`https://www.proteinatlas.org/${gene}`}
                      target="_blank"
                    >
                      {geneNames[i]}
                    </a>
                  </TableHeaderColumn>
                ))}
              </TableRow>
            </TableHeader>
            <TableBody displayRowCheckbox={false}>
              {Object.entries(expressionMatrix).map(
                ([cancerType, expressions]) => {
                  return (
                    <TableRow key={cancerType}>
                      <TableHeaderColumn>{cancerType}</TableHeaderColumn>
                      {expressions.map((item, index) => {
                        return (
                          <TableRowColumn key={`${cancerType}-${index}`}>
                            {item
                              .replace("unchanged", "o")
                              .replace("mid-lower", "-")
                              .replace("mid-higher", "+")
                              .replace("lower", "--")
                              .replace("higher", "++")}
                          </TableRowColumn>
                        );
                      })}
                    </TableRow>
                  );
                }
              )}
            </TableBody>
          </Table>
        )}
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

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
  render() {
    const { genes, geneNames, expressionMatrix } = this.props.result;

    return (
      <div>
        <h3>
          {expressionMatrix === null
            ? "Gene Exploration"
            : "Gene Expression Levels"}
        </h3>
        <p>
          The following genes were especially relevant for discriminating the
          clusters:
        </p>
        {expressionMatrix === null ? (
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
                  <TableHeaderColumn>
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
                    <TableRow>
                      <TableHeaderColumn>{cancerType}</TableHeaderColumn>
                      {expressions.map(item => {
                        return (
                          <TableRowColumn>
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

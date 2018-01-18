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
import Color from "tinycolor2";

import { lightGray, slightlyBoringBlue } from "../../../config/colors";

export default class GeneExploration extends Component {
  render() {
    const { genes, geneNames, expressionMatrix } = this.props.result;

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
          <Table
            style={{ tableLayout: "auto" }}
            fixedHeader={false}
            bodyStyle={{ overflow: "visible" }}
          >
            <TableHeader displaySelectAll={false} adjustForCheckbox={false}>
              <TableRow>
                <TableHeaderColumn />
                {genes.map((gene, i) => (
                  <StyledTableHeaderColumn key={gene} title={geneNames[i]}>
                    <a
                      href={`https://www.proteinatlas.org/${gene}`}
                      target="_blank"
                    >
                      {geneNames[i]}
                    </a>
                  </StyledTableHeaderColumn>
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
                        let bgColor, title;
                        if (item.startsWith("cant compute - ")) {
                          bgColor = lightGray;
                          title =
                            "This is not statistically significant because there are not enough values.";
                        } else {
                          switch (item) {
                            case "unchanged":
                              bgColor = Color(slightlyBoringBlue)
                                .lighten(18)
                                .toString();
                              break;
                            case "less":
                              bgColor = Color(slightlyBoringBlue)
                                .lighten(25)
                                .toString();
                              break;
                            case "greater":
                              bgColor = Color(slightlyBoringBlue)
                                .lighten(10)
                                .toString();
                              break;
                            default:
                              break;
                          }
                        }
                        item = item
                          .replace("cant compute - ", "*")
                          .replace("unchanged", "o")
                          .replace("less", "–")
                          .replace("greater", "+");
                        return (
                          <StyledTableRowColumn
                            key={`${cancerType}-${index}`}
                            background={bgColor}
                            title={title}
                          >
                            {item}
                          </StyledTableRowColumn>
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

const StyledTableHeaderColumn = styled(TableHeaderColumn)`
  text-align: center !important;
  min-width: 60px;
  padding-left: 0 !important;
  padding-right: 0 !important;
  overflow: hidden;
  text-overflow: ellipsis;
`;

const StyledTableRowColumn = styled(TableRowColumn)`
  background: ${props => props.background} !important;
  text-align: center !important;
  font-size: 1em !important;
  border-left: solid 1px white;
  min-width: 60px;
  padding-left: 0 !important;
  padding-right: 0 !important;
`;

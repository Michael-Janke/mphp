import React from "react";
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

import { lightGray, slightlyBoringBlue } from "../../../../config/colors";

const ExpressionMatrix = ({ data }) => {
  const { expressionMatrix, genes, geneNames, geneExplorationList } = data;
  return (
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
              {geneExplorationList[i]}
            </StyledTableHeaderColumn>
          ))}
        </TableRow>
      </TableHeader>
      <TableBody displayRowCheckbox={false}>
        {Object.entries(expressionMatrix).map(([cancerType, expressions]) => {
          return (
            <TableRow key={cancerType}>
              <TableHeaderColumn>{cancerType}</TableHeaderColumn>
              {expressions.map((item, index) => {
                const {
                  bgColor,
                  title,
                  correctedItem
                } = computeTableEntryStyles(item, index);
                return (
                  <StyledTableRowColumn
                    key={`${cancerType}-${index}`}
                    background={bgColor}
                    title={title}
                  >
                    {correctedItem}
                  </StyledTableRowColumn>
                );
              })}
            </TableRow>
          );
        })}
      </TableBody>
    </Table>
  );
};

const computeTableEntryStyles = (item, index, cancerType) => {
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

  return { bgColor, title, correctedItem: item };
};

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

export default ExpressionMatrix;

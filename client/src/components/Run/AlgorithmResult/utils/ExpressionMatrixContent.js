import React from "react";
import styled from "styled-components";
import Color from "tinycolor2";

import { lightGray, slightlyBoringBlue } from "../../../../config/colors";

const ExpressionMatrixContent = ({ expressionMatrix }) => {
  return Object.entries(expressionMatrix).map(([cancerType, expressions]) => {
    return (
      <tr key={cancerType}>
        <StyledTableHeaderColumn>{cancerType}</StyledTableHeaderColumn>
        {expressions.map((item, index) => {
          const { bgColor, title, correctedItem } = computeTableEntryStyles(
            item
          );
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
      </tr>
    );
  });
};

const computeTableEntryStyles = item => {
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

const StyledTableHeaderColumn = styled.th`
  text-align: center;
  min-width: 60px;
  overflow: hidden;
  text-overflow: ellipsis;
  height: 56px;
  font-size: 12px;
  color: ${props => props.theme.deepGray};
`;

const StyledTableRowColumn = styled.td`
  background: ${props => props.background} !important;
  text-align: center !important;
  font-size: 1em !important;
  border-left: solid 1px white;
  min-width: 60px;
  padding: 0;
  height: 56px !important;
`;

export default ExpressionMatrixContent;

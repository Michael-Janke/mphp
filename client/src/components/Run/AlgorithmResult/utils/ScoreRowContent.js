import React from "react";
import styled from "styled-components";

const ScoreRowContent = ({
  geneId,
  index,
  entryWasFound,
  link,
  providerName
}) => {
  const content = entryWasFound ? "+" : "-";

  return (
    <StyledTableRowColumn
      key={`${providerName}-${index}`}
      entryWasFound={entryWasFound}
      title={`${providerName}-${geneId}`}
    >
      <StyledLink href={link} target="_blank">
        {content}
      </StyledLink>
    </StyledTableRowColumn>
  );
};

const StyledTableRowColumn = styled.td`
  background: ${props =>
    props.entryWasFound ? props.theme.leafGreen : props.theme.lightGray};
  text-align: center;
  font-size: 1em;
  border-left: solid 1px white;
  min-width: 60px;
  padding: 0;
  height: 56px;
`;

const StyledLink = styled.a`
  width: 100%;
  height: 100%;
  display: block;
  text-decoration: none;
  color: black;
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  font-size: 1em;
  &:visited {
    text-decoration: inherit;
    color: inherit;
  }
`;

export default ScoreRowContent;

import React from "react";
import styled from "styled-components";

const ScoreRowContent = ({
  geneId,
  index,
  entryFound,
  name,
  entryFoundName,
  link,
  linkCoexpressed,
  providerName,
  coexpressed
}) => {
  const content = entryFound ? "+" : "-";
  coexpressed = entryFound !== geneId;
  return entryFound && coexpressed ? (
    <SplitWrapperWrapper>
      <SplitWrapper>
        <SplitStyledTableRowColumn
          key={`${providerName}-${index}-1`}
          isLeft={true}
          title={name}
        >
          <StyledLink href={link} target="_blank">
            -
          </StyledLink>
        </SplitStyledTableRowColumn>
        <SplitStyledTableRowColumn
          key={`${providerName}-${index}-2`}
          isLeft={false}
          title={entryFoundName}
        >
          <StyledLink href={linkCoexpressed} target="_blank">
            +
          </StyledLink>
        </SplitStyledTableRowColumn>
      </SplitWrapper>
    </SplitWrapperWrapper>
  ) : (
      <StyledTableRowColumn
        key={`${providerName}-${index}`}
        entryFound={entryFound}
        title={
          entryFound
            ? entryFoundName
            : name
        }
        coexpressed={coexpressed}
      >
        <StyledLink href={link} target="_blank">
          {content}
        </StyledLink>
      </StyledTableRowColumn>
    );
};

const SplitWrapperWrapper = styled.td`
  border-left: solid 1px white;
  padding: 0;
  min-width: 70px;
`;

const SplitWrapper = styled.div`
  display: flex;
  flex-direction: row;
  padding: 0;
  height: 58px;
`;

const SplitStyledTableRowColumn = styled.div`
  background: ${props =>
    props.isLeft ? props.theme.lightGray : props.theme.leafGreen};
  text-align: center;
  font-size: 1em;
  flex: 1;
`;

const StyledTableRowColumn = styled.td`
  background: ${props =>
    props.entryFound ? props.theme.leafGreen : props.theme.lightGray};
  text-align: center;
  font-size: 1em;
  border-left: solid 1px white;
  min-width: 70px;
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

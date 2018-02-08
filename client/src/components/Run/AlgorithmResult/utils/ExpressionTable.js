import React from "react";
import styled from "styled-components";

import Spinner from "../../../Spinner.js";
import ScoreRowContent from "./ScoreRowContent";
import ExpressionMatrixContent from "./ExpressionMatrixContent";

const ExpressionTable = props => {
  const { expressionMatrix, genes, geneNames, geneResults } = props.data;

  return (
    <StyledRoot>
      <StyledTable>
        <thead>
          <tr>
            <th />
            {genes.map((gene, i) => (
              <th key={gene} title={geneNames[i]}>
                <StyledGene key={gene}>{geneNames[i]}</StyledGene>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {expressionMatrix && [
            <TableLabel key="cancer_data_label">
              <TableLabelContent key="cancer_data_label_content">
                Over- or underexpression in different cancer types
              </TableLabelContent>
            </TableLabel>,
            <ExpressionMatrixContent
              key="expressionMatrix"
              expressionMatrix={expressionMatrix}
            />
          ]}
          {geneResults && [
            <TableLabel key="gene_score_label">
              <TableLabelContent key="gene_score_label_content">
                Cancer related according to:
              </TableLabelContent>
            </TableLabel>,
            <BreakingTableRow key="proteinAtlas">
              <StyledTableHeaderColumn>Protein Atlas</StyledTableHeaderColumn>
              {genes.map((key, index) => {
                return (
                  geneResults[key] && (
                    <ScoreRowContent
                      geneId={key}
                      key={key}
                      providerName="ProteinAtlas"
                      index={index}
                      entryWasFound={geneResults[key].proteinAtlas}
                      link={`https://www.proteinatlas.org/${key}`}
                    />
                  )
                );
              })}
            </BreakingTableRow>,
            <tr key="DisGeNet">
              <StyledTableHeaderColumn>DisGeNet</StyledTableHeaderColumn>
              {genes.map((key, index) => {
                return (
                  geneResults[key] && (
                    <ScoreRowContent
                      geneId={key}
                      key={key}
                      providerName="DisGeNet"
                      index={index}
                      entryWasFound={geneResults[key].disgenet}
                      link={`http://www.disgenet.org/web/DisGeNET/menu/search?0#${
                        geneNames[index]
                      }`}
                    />
                  )
                );
              })}
            </tr>,
            <tr key="CancerGeneCensus">
              <StyledTableHeaderColumn>
                Cancer Gene Census
              </StyledTableHeaderColumn>
              {genes.map((key, index) => {
                return (
                  geneResults[key] && (
                    <ScoreRowContent
                      geneId={key}
                      key={key}
                      providerName="Cancer Gene Census"
                      index={index}
                      entryWasFound={geneResults[key].cancer_gene_census}
                      link={`http://cancer.sanger.ac.uk/census`}
                    />
                  )
                );
              })}
            </tr>,
            <tr key="EntrezGeneSummary">
              <StyledTableHeaderColumn>
                Entrez Gene Summary
              </StyledTableHeaderColumn>
              {genes.map((key, index) => {
                return (
                  geneResults[key] && (
                    <ScoreRowContent
                      geneId={key}
                      key={key}
                      providerName="Entrez Gene Summary"
                      index={index}
                      entryWasFound={geneResults[key].entrezGeneSummary}
                      link={`https://www.proteinatlas.org/${key}`}
                    />
                  )
                );
              })}
            </tr>,
            <tr key="Scores">
              <StyledTableHeaderColumn>Total Scores</StyledTableHeaderColumn>
              {genes.map((key, index) => {
                return (
                  geneResults[key] && (
                    <StyledTableRowColumn
                      key={`score-${index}`}
                      background="white"
                      title={`Score-${key}`}
                    >
                      {geneResults[key].score}
                    </StyledTableRowColumn>
                  )
                );
              })}
            </tr>
          ]}
        </tbody>
      </StyledTable>
      {!geneResults && <Spinner />}
    </StyledRoot>
  );
};

const StyledTable = styled.table`
  border-collapse: collapse;
`;

const TableLabelContent = styled.td`
  max-width: 100px;
  font-size: 12px;
`;

const TableLabel = styled.tr`
  position: absolute;
  left: 0;
`;

const StyledRoot = styled.div`
  padding-left: 100px;
  position: relative;
  overflow: auto;
`;

const BreakingTableRow = styled.tr`
  border-top: 2px solid black;
`;

const StyledTableHeaderColumn = styled.th`
  text-align: center;
  min-width: 60px;
  overflow: hidden;
  text-overflow: ellipsis;
  height: 56px;
  font-size: 12px;
  color: ${props => props.theme.deepGray};
`;

const StyledGene = styled.span`
  margin: 5px;
  display: flex;
  flex-direction: column;
  font-size: 11px;
  white-space: nowrap;
  text-overflow: ellipsis;
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

export default ExpressionTable;

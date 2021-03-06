import React, { PureComponent } from "react";
import styled from "styled-components";
import { FormattedMessage } from "react-intl";
import HelpIcon from "material-ui/svg-icons/action/help-outline";
import FlatButton from "material-ui/FlatButton";

import Spinner from "../../../Spinner.js";
import ScoreRowContent from "./ScoreRowContent";
import ExpressionMatrixContent from "./ExpressionMatrixContent";
import TooltipBox from "../../../TooltipBox";

export default class ExpressionTable extends PureComponent {
  state = { loading: false };

  render() {
    const { expressionMatrix, genes, geneNames, geneResults } = this.props.data;
    const { runId, oneAgainstRest, cancerType, fullTestGenes } = this.props;

    const fullRun = geneResults && "proteinAtlas" in geneResults[genes[0]];

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
                  <div>Expression levels</div>
                  <StyledTooltipBox
                    text={<FormattedMessage id={`GeneExpression.General`} />}
                    position="top right"
                  >
                    <HelpIcon />
                  </StyledTooltipBox>
                </TableLabelContent>
              </TableLabel>,
              <ExpressionMatrixContent
                key="expressionMatrix"
                expressionMatrix={expressionMatrix}
              />
            ]}
            {geneResults && [
              <TableLabel key="gene_total_score_label">
                <TableLabelContent key="gene_total_score_label_content">
                  Cancer related according to:
                  <StyledTooltipBox
                    text={
                      <FormattedMessage
                        id={`GeneExpression.GeneScoreExplanation`}
                      />
                    }
                    position="top right"
                  >
                    <HelpIcon />
                  </StyledTooltipBox>
                </TableLabelContent>
              </TableLabel>,
              <BreakingTableRow key="OpenTarget">
                <StyledTableHeaderColumn title="The Open Targets Platform is a comprehensive and robust data integration for access to and visualisation of potential drug targets associated with disease. It brings together multiple data types and aims to assist users to identify and prioritise targets for further investigation.">
                  OpenTarget
                </StyledTableHeaderColumn>
                {genes.map((key, index) => {
                  return (
                    geneResults[key] && (
                      <ScoreRowContent
                        geneId={key}
                        key={key}
                        providerName="openTarget"
                        index={index}
                        geneResult={geneResults[key].openTarget}
                        name={geneNames[index]}
                        link={`https://www.targetvalidation.org/target/${key}/associations`}
                        linkCoexpressed={`https://www.targetvalidation.org/target/${
                          geneResults[key].openTarget.coexpressed
                        }/associations`}
                      />
                    )
                  );
                })}
              </BreakingTableRow>
            ]}
            {fullRun && [
              <tr key="proteinAtlas">
                <StyledTableHeaderColumn
                  title={
                    "The Human Protein Atlas is a Swedish-based program initiated in 2003 with the aim to map all the human proteins in cells, tissues and organs using integration of various omics technologies, including antibody-based imaging, mass spectrometry-based proteomics, transcriptomics and systems biology."
                  }
                >
                  Protein Atlas
                </StyledTableHeaderColumn>
                {genes.map((key, index) => {
                  return (
                    geneResults[key] && (
                      <ScoreRowContent
                        geneId={key}
                        key={key}
                        providerName="ProteinAtlas"
                        index={index}
                        geneResult={geneResults[key].proteinAtlas}
                        name={geneNames[index]}
                        link={`https://www.proteinatlas.org/${key}`}
                        linkCoexpressed={`https://www.proteinatlas.org/${
                          geneResults[key].proteinAtlas.coexpressed
                        }`}
                      />
                    )
                  );
                })}
              </tr>,
              <tr key="DisGeNet">
                <StyledTableHeaderColumn title="The DisGeNET database integrates human gene-disease associations (GDAs) from various expert curated databases and text-mining derived associations including Mendelian, complex and environmental diseases.">
                  DisGeNet
                </StyledTableHeaderColumn>
                {genes.map((key, index) => {
                  return (
                    geneResults[key] && (
                      <ScoreRowContent
                        geneId={key}
                        key={key}
                        providerName="DisGeNet"
                        index={index}
                        geneResult={geneResults[key].disgenet}
                        name={geneNames[index]}
                        link={`http://www.disgenet.org/web/DisGeNET/menu/search`}
                        linkCoexpressed={`http://www.disgenet.org/web/DisGeNET/menu/search`}
                      />
                    )
                  );
                })}
              </tr>,
              <tr key="CancerGeneCensus">
                <StyledTableHeaderColumn title="The Cancer Gene Census (CGC) is an ongoing effort to catalogue those genes which contain mutations that have been causally implicated in cancer.">
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
                        geneResult={geneResults[key].cancerGeneCensus}
                        name={geneNames[index]}
                        link={`http://cancer.sanger.ac.uk/census`}
                        linkCoexpressed={`http://cancer.sanger.ac.uk/census`}
                      />
                    )
                  );
                })}
              </tr>,
              <tr key="EntrezGeneSummary">
                <StyledTableHeaderColumn title="Entrez Gene is NCBI's database for gene-specific information. Entrez Gene includes records from genomes that have been completely sequenced, that have an active research community to contribute gene-specific information or that are scheduled for intense sequence analysis.">
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
                        geneResult={geneResults[key].entrezGeneSummary}
                        name={geneNames[index]}
                        link={`https://www.proteinatlas.org/${key}`}
                        linkCoexpressed={`https://www.proteinatlas.org/${
                          geneResults[key].entrezGeneSummary
                        }`}
                      />
                    )
                  );
                })}
              </tr>,
              <TableLabel key="gene_score_label">
                <TableLabelContent key="gene_score_label_content">
                  <div>Total calculated Scores</div>
                  <StyledTooltipBox
                    text={
                      <FormattedMessage id={`GeneExpression.TotalScores`} />
                    }
                    position="top right"
                  >
                    <HelpIcon />
                  </StyledTooltipBox>
                </TableLabelContent>
              </TableLabel>,
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
        {!geneResults && (
          <span>
            Loading Gene Results
            <Spinner />
          </span>
        )}
        {geneResults &&
          !fullRun && (
            <StyledTooltipBox
              text="Note: This loads information from external services and may take a while."
              position="right width"
              width={400}
            >
              <FlatButton
                label="Load more"
                primary={true}
                disabled={this.state.loading}
                onClick={() => {
                  fullTestGenes(runId, {
                    genes,
                    oneAgainstRest,
                    cancerType
                  });
                  this.setState({ loading: true });
                }}
              />
            </StyledTooltipBox>
          )}
      </StyledRoot>
    );
  }
}

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
  padding-bottom: 14px;
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

const StyledTooltipBox = styled(TooltipBox)`
  display: inline-block;
`;

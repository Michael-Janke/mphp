import React, { Component } from "react";
import styled from "styled-components";

export default class GeneExploration extends Component {
  render() {
    const { gene, geneName } = this.props;

    return (
      <div>
        <a href={`https://www.proteinatlas.org/${gene}.xml`} target="_blank">
          {geneName}
        </a>
      </div>
    );
  }
}

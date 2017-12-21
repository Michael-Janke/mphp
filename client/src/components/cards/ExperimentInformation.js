import React, { Component } from "react";
import Card from "../Card";

class SelectDataset extends Component {
  render() {
    return (
      <Card
        title="Experiment Information"
        DataViewer={DataViewer}
        viewerProps={{ ...this.props.data }}
      />
    );
  }
}

class DataViewer extends Component {
  render() {
    return <div>Data Set: {this.props.dataset}</div>;
  }
}

export default SelectDataset;

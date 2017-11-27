import React, { Component } from 'react';
import Card from './_Card';

const ROUTE = "/statistics";
const TITLE = "Statistics";

class Statistics extends Component {
  render() {
    return <Card route={ROUTE} title={TITLE} DataView={DataView} />;
  }
}

class DataView extends Component {
  render() {
    return (
      <p>{JSON.stringify(this.props.data)}</p>
    );
  }
}

export default Statistics;

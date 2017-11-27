import React, { Component } from 'react';
import Card from './_Card';

const ROUTE = "/data";
const TITLE = "Some Data";

class Data extends Component {
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

export default Data;

import React, { Component } from "react";
import { connect } from "react-redux";
import { load } from "../../actions/someDataActions";
import Card from "../Card";

class Data extends Component {
  constructor(props) {
    super(props);
    if (this.props.someData === null) {
      this.props.loadSomeData();
    }
  }

  render() {
    return (
      <Card
        title={"Some Data"}
        DataViewer={DataViewer}
        isLoading={!this.props.someData}
        viewerProps={{ data: this.props.someData }}
      />
    );
  }
}

class DataViewer extends Component {
  render() {
    return <p>{JSON.stringify(this.props.data)}</p>;
  }
}

const mapStateToProps = state => {
  return {
    someData: state.someData
  };
};

const mapDispatchToProps = dispatch => {
  return {
    loadSomeData: () => {
      dispatch(load());
    }
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(Data);

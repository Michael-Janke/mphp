/* global Plotly:true */
import loadScript from "load-script";
import React, { Component } from "react";
import { connect } from "react-redux";
import createPlotlyComponent from "react-plotly.js/factory";
import { withTheme } from "styled-components";

import Card from "../Card";
import { load } from "../../actions/plotActions";

let Plot;
loadScript("https://cdn.plot.ly/plotly-latest.min.js", function(err, script) {
  if (err) {
    // print useful message
  } else {
    // use script
    // note that in IE8 and below loading error wouldn't be reported
    Plot = createPlotlyComponent(Plotly);
  }
});

class InteractivePlot extends Component {
  constructor(props) {
    super(props);
    if (this.props.plot === null) {
      this.props.loadPlot();
    }
  }

  rerender() {
    this.forceUpdate();
  }

  render() {
    return (
      <Card
        title={"Interactive Plots"}
        DataViewer={withTheme(DataViewer)}
        viewerProps={{ data: this.props.plot }}
        isLoading={!this.props.plot}
      />
    );
  }
}

class DataViewer extends Component {
  render() {
    const plotData = this.props.data;
    let data = [];
    Object.keys(plotData.data).forEach((key, index) => {
      const newDataObject = {
        type: "scatter3d",
        mode: "markers",
        name: key,
        x: plotData.data[key][0],
        y: plotData.data[key][1],
        z: plotData.data[key][2],
        marker: {
          size: 4,
          color: this.props.theme.statisticsColors[index],
          line: {
            color: "black",
            width: 0.1
          },
          opacity: 1
        }
      };
      data.push(newDataObject);
    });
    const layout = {
      margin: {
        l: 0,
        r: 0,
        b: 0,
        t: 0
      },
      scene: {
        xaxis: {
          title: plotData.genes[0]
        },
        yaxis: {
          title: plotData.genes[1]
        },
        zaxis: {
          title: plotData.genes[2]
        }
      },
      legend: {
        yanchor: "middle",
        y: 0.7
      }
    };
    return <Plot data={data} layout={layout} />;
  }
}

const mapStateToProps = state => {
  return {
    plot: state.plot
  };
};

const mapDispatchToProps = dispatch => {
  return {
    loadPlot: () => {
      dispatch(load());
    }
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(InteractivePlot);

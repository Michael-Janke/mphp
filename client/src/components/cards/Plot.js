/* global Plotly:true */
import loadScript from "load-script";
import React, { Component } from "react";
import createPlotlyComponent from "react-plotly.js/factory";

import { statisticsColors } from "../../config/colors";
import Card from "../Card";

let Plot;
loadScript("https://cdn.plot.ly/plotly-latest.min.js", function(err, script) {
  if (err) {
    console.warn(
      "Could not load plotly script from CDN, trying to load local script..."
    );
    loadScript("plotly-1.31.2.min.js", function(err, script) {
      if (err) {
        console.warn("Could not load plotly");
      } else {
        // note that in IE8 and below loading error wouldn't be reported
        Plot = createPlotlyComponent(Plotly);
      }
    });
  } else {
    // use script
    // note that in IE8 and below loading error wouldn't be reported
    Plot = createPlotlyComponent(Plotly);
  }
});

export default class InteractivePlot extends Component {
  constructor(props) {
    super(props);
    this.props.loadPlot(this.props.route, this.props.params);
  }

  rerender() {
    this.forceUpdate();
  }

  render() {
    let layout = {};
    let data = [];
    if (!!this.props.plot) {
      const plotData = this.props.plot;
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
            color: statisticsColors[index],
            line: {
              color: "black",
              width: 0.1
            },
            opacity: 1
          }
        };
        data.push(newDataObject);
      });
      layout = {
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
    }

    return (
      <Card
        title={"Interactive Plots"}
        isLoading={!this.props.plot}
        isError={this.props.plot && this.props.plot.isError}
      >
        {this.props.plot &&
          !this.props.plot.isError && <Plot data={data} layout={layout} />}
      </Card>
    );
  }
}

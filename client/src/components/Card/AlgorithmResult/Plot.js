/* global Plotly:true */
import loadScript from "load-script";
import React, { Component } from "react";
import createPlotlyComponent from "react-plotly.js/factory";

import { statisticsColors } from "../../../config/colors";

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
  rerender() {
    this.forceUpdate();
  }

  render() {
    const { data, genes } = this.props;
    const plotData = Object.keys(data).map((key, index) => {
      return {
        type: "scatter3d",
        mode: "markers",
        name: key,
        x: data[key][0],
        y: data[key][1],
        z: data[key][2],
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
    });
    const plotLayout = {
      margin: {
        l: 0,
        r: 0,
        b: 0,
        t: 0
      },
      scene: {
        xaxis: {
          title: genes[0]
        },
        yaxis: {
          title: genes[1]
        },
        zaxis: {
          title: genes[2]
        }
      },
      legend: {
        yanchor: "middle",
        y: 0.7
      }
    };

    return (
      <div>
        <h3>Visualization</h3>
        <Plot data={plotData} layout={plotLayout} />
      </div>
    );
  }
}

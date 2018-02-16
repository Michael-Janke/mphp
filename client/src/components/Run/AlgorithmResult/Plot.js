/* global Plotly:true */
import loadScript from "load-script";
import React, { Component } from "react";
import createPlotlyComponent from "react-plotly.js/factory";
import Color from "tinycolor2";

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
    let oldCancerType,
      oldColor,
      color,
      colorIndex = 0;
    const { data, geneNames, oneAgainstRest } = this.props;
    let plotData, plotLayout;
    if (data && geneNames) {
      plotData = Object.keys(data).map((key, index) => {
        const cancerType = key.split("-")[0];

        if (oneAgainstRest) {
          const tissueType = key.split("-")[1];
          if (cancerType === this.props.cancerType) {
            color = Color(statisticsColors[5]);
          } else {
            color = Color(statisticsColors[2]);
          }
          color = tissueType === "sick" ? color : color.lighten(7);
        } else if (oldCancerType !== cancerType) {
          color = Color(statisticsColors[colorIndex++]);
          oldCancerType = cancerType;
          oldColor = color;
        } else {
          if (key.split("-")[1].includes("N")) {
            color = oldColor.spin(12).lighten(7);
          } else {
            color = oldColor.spin(-12).darken(7);
          }
          oldColor = color;
        }

        return {
          type: `scatter${geneNames.length > 2 ? "3d" : ""}`,
          mode: "markers",
          name: key,
          x: data[key][0],
          y: data[key][1],
          z: data[key][2],
          marker: {
            size: 5,
            color: color.toString(),
            opacity: 1
          }
        };
      });

      plotLayout =
        geneNames.length > 2
          ? {
              margin: {
                l: 0,
                r: 0,
                b: 0,
                t: 0
              },
              scene: {
                xaxis: {
                  title: geneNames[0]
                },
                yaxis: {
                  title: geneNames[1]
                },
                zaxis: {
                  title: geneNames[2]
                }
              },
              legend: {
                yanchor: "middle",
                y: 0.7
              }
            }
          : {
              margin: {
                l: 0,
                r: 0,
                b: 0,
                t: 0
              },
              xaxis: {
                title: geneNames[0]
              },
              yaxis: {
                title: geneNames[1]
              },
              legend: {
                yanchor: "middle",
                y: 0.7
              }
            };
    }

    return (
      <div>
        {plotData && plotLayout && <Plot data={plotData} layout={plotLayout} />}
      </div>
    );
  }
}

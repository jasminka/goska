String.prototype.format = function () {
    var args = arguments;
    return this.replace(/\{\{|\}\}|\{(\d+)\}/g, function (m, n) {
        if (m == "{{ ") {
            return "{";
        }
        if (m == "}}") {
            return "}";
        }
        return args[n];
    });
};

$(".chosen-select").chosen({no_results_text: "Oops, nothing found!"});

$(document).ready(function () {
    var img = $("#prj"),
        last = 0,
        data;

    $('#accordion').hide();
    $('#panelOsnovni').hide();
    $('#panelSklopi').hide();

    var sklopi;
    $.getJSON( "/sklopi/", function( data ) {
        sklopi = data;
    });

    img.click(function (e) {
        var offset = $(this).offset();
        var ix = e.pageX - offset.left,
            iy = e.pageY - offset.top,
            iwidth = img.width(),
            iheight = img.height(),
            xMin = 375209.19,
            yMin = 30853.2,
            xMax = 624065.31,
            yMax = 193270.41;

        var x = ix / iwidth * (xMax - xMin) + xMin;
        var y = (yMax) - iy / iheight * (yMax - yMin);

        //$("#sum").html("ix/iy: " + ix + "/" + iy + " x/y: " + x + "/" + y)

        $.get("/coor/?x=" + x + "&y=" + y, function (data) {
            var select_id = (last === 0) ? '#select-1' : '#select-2';//izbereš 1. ali 2. gumb iz html-ja, da ga boš napolnil
            last = (last + 1) % 2;

            $(select_id + ' option[value="' + data.id + '"]').attr('selected', 'selected');
            $(select_id).chosen().change();
            $(select_id).trigger("chosen:updated");
        });
    });

    $('#optionsOsnovni').click(function () {
        if (data) {
            refresh();
        }
    });

    $('#optionsNapredni').click(function () {
        if (data) {
            refresh();
        }
    });

    var drawSklopi = function (group, sklop) {
        var counter = 0;
        $('#' + group).html('');

        if (sklop && sklopi) {
            $.each(data.kazalniki, function (index, value) {
                $.each(value.attributes, function (index, attribute) {
                    if (sklopi[sklop].kazalniki.indexOf(attribute.id) != -1) {
                        console.log(attribute);
                        var min = attribute.min_name;
                        if (min.length > 7){
                            min = attribute.min_name.substring(0,7) + '...'
                        };
                        var max = attribute.max_name;
                        if (max.length > 7){
                            max = attribute.max_name.substring(0,7) + '...'
                        };
                        var data = [
                            [min, attribute.min],
                            ['POVPRECJE', attribute.mean],
                            [max, attribute.max],
                            [attribute.o1_name, attribute.o1_real],
                            [attribute.o2_name, attribute.o2_real]
                        ];

                        var id = group + '-' + counter.toString();
                        var a = attribute.attribute;
                        if (a.length > 20) {
                            a = a.substring(0, 20) + '...'
                        }

                        //var ticks = ['Min', 'Max', 'Mean', 'Kranjska gora', 'Ljubljana'];
                        $('#' + group).append('<div id="' + id + '" style="height:300px;"></div>');
                        $.jqplot(id, [data], {
                            // Tell the plot to stack the bars.
                            captureRightClick: true,
                              seriesDefaults:{
                              renderer:$.jqplot.BarRenderer,
                              rendererOptions: {
                                  // Put a 30 pixel margin between bars.
                                  barMargin: 7,
                                  varyBarColor : true,
                                            // Highlight bars when mouse button pressed.
                                  // Disables default highlighting on mouse over.
                                  highlightMouseDown: true

                              },
                              pointLabels: {
                              show: true,
                              edgeTolerance: -5

                              }
                            },
                            series:[{renderer:$.jqplot.BarRenderer}],
                            axesDefaults: {
                              tickRenderer: $.jqplot.CanvasAxisTickRenderer,
                              tickOptions: {
                                angle: -70,
                                fontSize: '7pt',

                                drawBaseline: false
                              }
                            },
                            axes: {
                                xaxis: {
                                    renderer: $.jqplot.CategoryAxisRenderer,
                                    tickOptions: {
                                  labelPosition: 'end',
                                  showGridline: false,

                                  fontSize: '11pt'
                                  }
                                },
                                yaxis: {
                                    tickRenderer: $.jqplot.CanvasAxisTickRenderer,
                                    tickOptions: {
                                        labelPosition: 'start',
                                        formatString: '%3.1f',
                                        angle: 0
                                    },
                                    label: a,
                                    labelRenderer: $.jqplot.CanvasAxisLabelRenderer
                                }
                            },
                            legend: {
                              show: false,
                              location: 'e',
                              placement: 'outside'
                            },
                              grid: {
                              background: '#ffffff',
                              borderWidth: 0.0,
                              shadow: false
                            }
                        });
                        counter++;
                    }
                });
            });
        }
    };

    $('#sklop-1').chosen().change(function (evt, combo) {
        var sklop = combo.selected;
        drawSklopi('grafi-1', sklop);
    });

    $('#sklop-2').chosen().change(function (evt, combo) {
        var sklop = combo.selected;
        drawSklopi('grafi-2', sklop);
    });

    $('#sklop-3').chosen().change(function (evt, combo) {
        var sklop = combo.selected;
        drawSklopi('grafi-3', sklop);
    });

    function refresh() {
        $("#sum").html(data.povzetek);
        $("#opis").html(data.opis);

        var kazalniki = "",
            d = [[]],
            counter = 0;

        if ($("input:radio[name=optionsRadios]:checked").val() === 'osnovni') {
            $("#panelSklopi").hide();
            $("#panelOsnovni").show();
            $.each(data.kazalniki, function (index, value) {
                kazalniki += "<div class=\"row\">";
                kazalniki += "<div style=\"text-align:right; font-size:10px\">RAZLIKA<br/>(100%: največja razlika med občinami) <br/></div>";
                kazalniki += "<div class=\"col-md-4\"><strong>{0}</strong></div>".format(value['group'])
                kazalniki += "<div id=\"chart_{0}\" class=\"col-md-6\"></div>".format(counter);
                kazalniki += "<div class=\"col-md-2 text-right\"><strong>{0}</strong> %</div><br/><br/>".format(Math.round(value['value']));
                kazalniki += "</div>";
                counter += 1;

                $.each(value.attributes, function (index, value) {
                    kazalniki += "<div class=\"row\">";
                    kazalniki += "<div class=\"col-md-4\">{0}</div>".format(value['attribute']);
                    kazalniki += "<div id=\"chart_{0}\" class=\"col-md-6\"></div>".format(counter);
                    kazalniki += "<div class=\"col-md-2 text-right\">{0} %</div>".format(Math.round(value['value']));
                    kazalniki += "</div>";
                    d[0].push({axis: value['attribute'], value: value['value']});
                    counter += 1;
                });
            });
            $("#kazalniki").html(kazalniki); //Funkcija, ki razredu #kazalniki dodaš vsebino

            //d[0].sort(function(a, b) {return b.value - a.value});
            //RadarChart.draw("#chart", d);

            function chosenChart(c, value) {
                var margin = {top: 15, right: 40, bottom: 15, left: 20},
                    width = 500 - margin.left - margin.right,
                    height = 47 - margin.top - margin.bottom;
                var chart = d3.bullet()
                    .width(width)
                    .height(height);

                var ddd = [
                    {
                        "o": [
                            {"name": value['o1_name'], "value": value['o1']},
                            {"name": value['o2_name'], "value": value['o2']}
                        ],
                        "ranges": [value['o1'], value['o2'], 100],
                        "measures": [0, 0],
                        "markers": [value['mean']],
                        "real": {
                            0: value['min'],
                            100: value['max']
                        }
                    }
                ];

                ddd[0]["real"][value['o1']] = value['o1_real'];
                ddd[0]["real"][value['o2']] = value['o2_real'];

                var svg = d3.select("#chart_" + c).selectAll("svg")
                    .data(ddd)
                    .enter().append("svg")
                    .attr("class", "bullet")
                    .attr("width", width + margin.left + margin.right)
                    .attr("height", height + margin.top + margin.bottom)
                    .append("g")
                    .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
                    .call(chart);
            }

            function barChart(c, value) {
                var plot = $.jqplot('chart_' + c, [[[value.o2_real, 1]], [[value.o1_real, 2]], [[value.max, 3]], [[value.mean, 4]], [[value.min, 5]]], {
                    seriesDefaults: {
                        renderer:$.jqplot.BarRenderer,
                        // Show point labels to the right ('e'ast) of each bar.
                        // edgeTolerance of -15 allows labels flow outside the grid
                        // up to 15 pixels.  If they flow out more than that, they
                        // will be hidden.
                        pointLabels: { show: true, location: 'e', edgeTolerance: -15 },
                        // Here's where we tell the chart it is oriented horizontally.
                        rendererOptions: {
                            barDirection: 'horizontal'
                        },
                        shadow: false
                    },
                    axes: {
                        yaxis: {
                            renderer: $.jqplot.CategoryAxisRenderer,
                            tickOptions:{
                                showGridline: false,
                                mark: false
                            },
                            ticks: [value.o2_name, value.o1_name, 'MAX', 'POVPREČJE', 'MIN']
                        }
                    },
                    grid:{
                        shadow: false,
                        borderWidth: 0,
                        background: '#ffffff'
                    }
                });
            }
            counter = 0;
            $.each(data.kazalniki, function (index, value) {
                counter += 1;
                $.each(value.attributes, function (index, value) {
                    barChart(counter, value);
                    counter += 1;
                });
            });
        } else {
            $("#panelOsnovni").hide();
            $("#panelSklopi").show();
        }
    }

    var btnsum = $("#btnsum");
    btnsum.click(function () {
        btnsum.button('loading');
        $.get("/compare/?o1=" + $('#select-1').val() + "&o2=" + $('#select-2').val(),function (_data) {
            $('#accordion').show();
            data = _data;
            refresh();

        }).always(function () {
            btnsum.button('reset');
        });

        return false;
    });
});
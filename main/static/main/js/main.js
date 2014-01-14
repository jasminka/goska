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
        last = 0;

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
    var btnsum = $("#btnsum");
    btnsum.click(function () {
        btnsum.button('loading');
        $.get("/compare/?o1=" + $('#select-1').val() + "&o2=" + $('#select-2').val(),function (data) {
            $("#sum").html(data.povzetek);
            $("#opis").html(data.opis);

            var kazalniki = "",
                d = [
                    []
                ],
                counter = 0;

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
            var radar = "<strong>Graf razlik med izbranima občinama od največje do najmanše razlike</strong></br></br></br>"
            var naslov = "<strong>Opis razlik</strong>"
            var legenda = ""
            $("#kazalniki").html(kazalniki); //Funkcija, ki razredu #kazalniki dodaš vsebino
            d[0].sort(function(a, b) {return b.value - a.value});
            $("#chart").html(radar);
            RadarChart.draw("#chart", d);
            $("#naslov").html(naslov);
            $("#legenda").html(legenda);

            counter = 0;
            $.each(data.kazalniki, function (index, value) {
                counter += 1;
                $.each(value.attributes, function (index, value) {
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

                    var svg = d3.select("#chart_" + counter).selectAll("svg")
                        .data(ddd)
                        .enter().append("svg")
                        .attr("class", "bullet")
                        .attr("width", width + margin.left + margin.right)
                        .attr("height", height + margin.top + margin.bottom)
                        .append("g")
                        .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
                        .call(chart);
                    counter += 1;
                });
            });

        }).always(function () {
                btnsum.button('reset');
            });
        return false;
    });
});
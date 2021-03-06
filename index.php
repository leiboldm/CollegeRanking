<html>
    <head>
        <title>National University Ranking</title>
	<base href="/CollegeRanking/">
        <link href="ranking.css" rel="stylesheet" type="text/css"/>
    </head>
    <body style="padding: 0; margin: 0;">
        <header id="header" style="height: 100%">
            <img id="headerBackground" src="images/UniversityofMichiganLawLibrarySmall.jpg"
            alt="University of Michigan Law Library" />
            <div class="headerTextContainer">
                <h1>MattLeibold.com National University Ranking</h1>
                <div id="description" style="text-align:center; padding-left: 20%; padding-right: 20%;">
                    <h2>A comprehensive ranking of all 4 year, degree-granting universities in the US.
                    </h2>
                    <h4>This ranking considers many important factors including cost of attendance, difficulty of admission, quality of instruction, student body demographics, and student success to create the most comprehensive of ranking of the best universities in the country.
                    </h4>
                </div>
            </div>
        </header>
        <div id="loader">Loading data ...</div>
        <div id="table_wrapper" style="padding: 5px; display: none;">
            <div id="upper_scrollbar" style="overflow-x: scroll; width: 100%;">
                <div id="upper_scrollbar_inner" style="height: 1px;"></div>
            </div>
            <div id="table_holder" style="width: 100%; overflow-x: scroll">
                <table id="myTable" class="display" style="width: 100%">
		<?php 
			include "rankingTable.html"
		?>
                </table>
            </div>
        </div>
        <div class="after_info">
            This ranking is based on data from the <a href="http://nces.ed.gov/ipeds/datacenter/">National Center For Education Statistics</a>.  Missing data is replaced with the national average except for SAT scores, admission rate, and matriculation rate which are replaced with the national minimum (1100, 100%, and 0% respectively). The data for this ranking is from 2014.  The algorithm for producing this ranking can be found at <a href="http://github.com/leiboldm/CollegeRanking">github.com/leiboldm/CollegeRanking</a>.
        </div>
        <footer style="text-align: center; color: #777">
             Copyright mattleibold.com June, 2016.
        </footer>
        <script type="text/javascript" src="jquery-1.12.3.js"></script>
        <script type="text/javascript" src="jquery.dataTables.min.js"></script>
        <link href="jquery.dataTables.min.css" rel="stylesheet" type="text/css"/>
        <script>
            /*  Resize the header to match the viewport height */
            function resizeHeaderHeight() {
                $("#header").css("height", window.innerHeight + "px");
            }
            $(window).resize(function(e) {
                /*  Chrome for android has address bar that appears and disappers 
                    causing the window to resize.  Only resize the header if
                    the window resizes substantially (ex: in the case of an 
                    orientation change) 
                */
                if (Math.abs($("#header").height() - window.innerHeight) > 200) {
                    resizeHeaderHeight();
                }
                var BK_WIDTH = 4288;
                var BK_HEIGHT = 2848;
                var width_scale = $('header').height() / BK_WIDTH;
                var new_height = 100 * BK_HEIGHT / $('header').height() * width_scale;
                if (new_height >= 100) {
                    $('#headerBackground').css("height", new_height.toString() + "%");
                    $('#headerBackground').css("width", "100%");
                    $('#headerBackground').css("left", "0%");
                } else {
                    var new_width = 10000 / new_height;
                    $('#headerBackground').css("left", "-" + ((new_width - 100) / 2) + "%");
                    $('#headerBackground').css("height", "100%");
                    $('#headerBackground').css("width",  new_width.toString() + "%");
                }
            });
            $(document).ready(function() {
                $('#loader').hide();
                $('#table_wrapper').show();
                resizeHeaderHeight();
                var highResHeader = new Image();
                highResHeader.onload = function() {
                    $('#headerBackground').attr("src",this.src);
                }
                highResHeader.src = "images/UniversityofMichiganLawLibrary.jpg";
		        $("#myTable").DataTable({ "pageLength": 25 });
	            $('#upper_scrollbar_inner').width($('#myTable').width());	
            });

            $('#upper_scrollbar').scroll(function() {
                $('#table_holder').scrollLeft($('#upper_scrollbar').scrollLeft());
            });
            $('#table_holder').scroll(function() {
                $('upper_scrollbar').scrollLeft($('#table_holder').scrollLeft());
            });
        </script>
    </body>
</html>

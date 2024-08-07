<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Insights Report</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background: #f4f4f4;
        }
        .container {
            width: 80%;
            margin: auto;
            overflow: hidden;
        }
        header {
            background: #333;
            color: #fff;
            padding-top: 30px;
            min-height: 70px;
            border-bottom: #77d42a 3px solid;
        }
        header a {
            color: #fff;
            text-decoration: none;
            text-transform: uppercase;
            font-size: 16px;
        }
        #main {
            padding: 20px;
            background: #fff;
            margin-top: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        footer {
            text-align: center;
            padding: 20px;
            background: #333;
            color: #fff;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>AI Insights Report</h1>
        </div>
    </header>
    <div id="main" class="container">
        <h2>Introduction</h2>
        <p>{{ introduction }}</p>

        <h2>AI Solutions</h2>
        <p>{{ ai_solutions }}</p>

        <h2>Detailed Analysis and Recommendations</h2>
        <p>{{ analysis }}</p>

        <h2>Graphs and Forecasts</h2>
        <div id="graphs">
            <img src="{{ graph1 }}" alt="Graph 1">
            <img src="{{ graph2 }}" alt="Graph 2">
        </div>

        <h2>Conclusion</h2>
        <p>{{ conclusion }}</p>
    </div>
    <footer>
        <p>&copy; 2024 AI Consulting Services</p>
    </footer>
</body>
</html>

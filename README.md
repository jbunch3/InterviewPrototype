# InterviewPrototype
Task: Implement a Financial Reporting System 

### Without Flask
Run hard coded request with JSON-like string. Run noflask.py
The request looks like this

`request = '"request_name": "Monthly Report", "client": "1", "report_template": "standard", "report_metric": "performance", "asset_restrictons": "wind", "start": "2022-01-01"'`

### With Flask

Start Application

`flask --app main run`

Send a Request that looks something like this:

`curl -XGET -H "Content-type: application/json" -d '{"request_name": "Monthly Report", "client": "1", "report_template": "standard", "report_metric": "performance", "asset_restrictons": "wind", "start": "2022-01-01"}' 'http://127.0.0.1:5000/reportgenerator'`


## Development

1. Create a virtual environment:

    `$ python3 -m venv .venv`

2. Activate the created environment:

    `$ source .venv/bin/activate`

3. Upgrade `pip`:

    `$ python3 -m pip install --upgrade pip`

4. Install the requirements:

    `$ pip install --upgrade -r requirements.txt`
    
5. Mark the main package as Sources Root.

6. Install the stack dependencies:

    `$ python3 install.py`

7. Try to synthesise the CloudFormation template:

    `$ cdk synth` 

## Test

1. Install the testing requirements:

    `$ pip install --upgrade -r requirements-test.txt`
    
2. Run all tests in package `tests`

import setuptools


with open('version', 'r') as version:

    setuptools.setup(
        name='data_processing_stack',
        version=version.readline(),
        author='Alessio Vierti',
        packages=setuptools.find_packages(exclude=['tests']),
        install_requires=[
            'aws-cdk.core==1.71.0',
            'aws-cdk.aws-dynamodb==1.71.0',
            'aws-cdk.aws-events==1.71.0',
            'aws-cdk.aws-events-targets==1.71.0',
            'aws-cdk.aws-lambda==1.71.0',
            'aws-cdk.aws-lambda-event-sources==1.71.0',
            'aws-cdk.aws-logs==1.71.0',
            'aws-cdk.aws-sns==1.71.0',
            'aws-cdk.aws-sqs==1.71.0',
            'aws-cdk.aws_apigateway==1.71.0'
        ],
        python_requires='>=3.6'
    )

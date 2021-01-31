#!/usr/bin/env python3

from aws_cdk import (
    core,
    aws_dynamodb as dynamodb
)

from data_processing_stack import DataProcessingStack, MongoDBConfiguration, AccessKeysConfiguration, ImportedAssetsConfiguration


class MockDataMiningStack(core.Stack):

    def __init__(self, scope: core.Construct, id_: str, **kwargs):

        super().__init__(scope, id_, **kwargs)

        self.property_table = dynamodb.Table(
            self,
            'Property',
            table_name='Property',
            partition_key=dynamodb.Attribute(
                name='id',
                type=dynamodb.AttributeType.STRING
            ),
            stream=dynamodb.StreamViewType.NEW_IMAGE
        )


app = core.App()
mock_data_mining_stack = MockDataMiningStack(app, 'MockDataMiningStack')
data_processing_stack = DataProcessingStack(
    app,
    'DataProcessingStack',
    mongodb_config=MongoDBConfiguration(
        uri='MockUri',
        max_page_size='10',
        database='timeSeriesDB',
        collection='properties'
    ),
    access_keys_config=AccessKeysConfiguration(
        geocoding='MockAccessKey'
    ),
    imported_assets_config=ImportedAssetsConfiguration(
        table_property=mock_data_mining_stack.property_table
    )
)
app.synth()

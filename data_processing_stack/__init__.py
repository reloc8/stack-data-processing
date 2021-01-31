from aws_cdk import (
    aws_sns as sns,
    aws_sns_subscriptions as sns_subscriptions,
    aws_lambda as lambda_,
    aws_logs as logs,
    aws_apigateway as api_gateway,
    aws_lambda_event_sources as event_sources,
    aws_dynamodb as dynamodb,
    core
)
from dataclasses import dataclass
from typing import AnyStr


DEFAULT_LAMBDA_HANDLER = 'main.lambda_handler'
DEFAULT_LAMBDA_RUNTIME = lambda_.Runtime.PYTHON_3_8
DEFAULT_LAMBDA_LOG_RETENTION = logs.RetentionDays.ONE_WEEK


@dataclass
class MongoDBConfiguration:

    uri: AnyStr
    max_page_size: AnyStr


@dataclass
class AccessKeysConfiguration:

    geocoding: AnyStr


@dataclass
class ImportedAssetsConfiguration:

    table_property: dynamodb.Table


class DataProcessingStack(core.Stack):

    def __init__(self, scope: core.Construct, id_: str,
                 imported_assets_config: ImportedAssetsConfiguration,
                 mongodb_config: MongoDBConfiguration,
                 access_keys_config: AccessKeysConfiguration,
                 **kwargs):

        super().__init__(scope, id_, **kwargs)

        # LAMBDAS DEFINITIONS

        lambda_dispatch_stream = lambda_.Function(
            self,
            'DispatchStream',
            code=lambda_.AssetCode('stack/lambda/dispatch_stream/1.0.0/python/dispatch_stream'),
            timeout=core.Duration.seconds(10),
            description='',
            function_name='DispatchStream',
            reserved_concurrent_executions=10,
            handler=DEFAULT_LAMBDA_HANDLER,
            runtime=DEFAULT_LAMBDA_RUNTIME,
            log_retention=DEFAULT_LAMBDA_LOG_RETENTION,
            memory_size=128,
            retry_attempts=0,
            dead_letter_queue_enabled=False
        )

        lambda_geocode_property = lambda_.Function(
            self,
            'GeocodeProperty',
            code=lambda_.AssetCode('stack/lambda/geocode_property/1.0.0/python/geocode_property'),
            timeout=core.Duration.seconds(15),
            description='',
            function_name='GeocodeProperty',
            reserved_concurrent_executions=10,
            handler=DEFAULT_LAMBDA_HANDLER,
            runtime=DEFAULT_LAMBDA_RUNTIME,
            log_retention=DEFAULT_LAMBDA_LOG_RETENTION,
            memory_size=128,
            retry_attempts=0,
            dead_letter_queue_enabled=True
        )

        lambda_fetch_properties = lambda_.Function(
            self,
            'FetchProperties',
            code=lambda_.AssetCode('stack/lambda/fetch_properties/1.0.0/python/fetch_properties'),
            timeout=core.Duration.seconds(10),
            description='',
            function_name='FetchProperties',
            reserved_concurrent_executions=10,
            handler=DEFAULT_LAMBDA_HANDLER,
            runtime=DEFAULT_LAMBDA_RUNTIME,
            log_retention=DEFAULT_LAMBDA_LOG_RETENTION,
            memory_size=128,
            retry_attempts=0,
            dead_letter_queue_enabled=True
        )

        # LAYERS DEFINITIONS

        layer_dispatch_stream = lambda_.LayerVersion(
            self,
            'DispatchStreamLibs',
            code=lambda_.Code.from_asset('stack/lambda/dispatch_stream/1.0.0/'),
            description='',
            layer_version_name='DispatchStreamLibs',
            compatible_runtimes=[DEFAULT_LAMBDA_RUNTIME]
        )

        layer_geocode_property = lambda_.LayerVersion(
            self,
            'GeocodePropertyLibs',
            code=lambda_.Code.from_asset('stack/lambda/geocode_property/1.0.0/'),
            description='',
            layer_version_name='GeocodePropertyLibs',
            compatible_runtimes=[DEFAULT_LAMBDA_RUNTIME]
        )

        layer_fetch_properties = lambda_.LayerVersion(
            self,
            'FetchPropertiesLibs',
            code=lambda_.Code.from_asset('stack/lambda/fetch_properties/1.0.0/'),
            description='',
            layer_version_name='FetchPropertiesLibs',
            compatible_runtimes=[DEFAULT_LAMBDA_RUNTIME]
        )

        # CLOUDWATCH RULES DEFINITIONS
        # -

        # SQS QUEUES DEFINITIONS
        # -

        # SNS TOPICS DEFINITIONS

        topic_new_properties = sns.Topic(
            self,
            'NewProperties',
            display_name='',
            topic_name='NewProperties'
        )

        # API GATEWAYS
        api_gateway_graphql = api_gateway.LambdaRestApi(
            self,
            'GraphQLApi',
            handler=lambda_fetch_properties,
            rest_api_name='GraphQLApi',
            description='GraphQL API',
            cloud_watch_role=True
        )
        api_gateway_graphql.root.add_resource('graphql').add_method('POST')

        # DYNAMODB PERMISSIONS
        lambda_dispatch_stream.add_event_source(event_sources.DynamoEventSource(
            table=imported_assets_config.table_property,
            starting_position=lambda_.StartingPosition.LATEST,
            batch_size=10,
            max_batching_window=core.Duration.seconds(30),
            parallelization_factor=10,
            retry_attempts=0
        ))

        # CLOUDWATCH SCHEDULING RULES
        # -

        # SQS PERMISSIONS
        # -

        # SNS PERMISSIONS

        topic_new_properties.grant_publish(lambda_dispatch_stream)
        topic_new_properties.add_subscription(sns_subscriptions.LambdaSubscription(lambda_geocode_property))

        # LAYERS ASSIGNMENTS

        lambda_dispatch_stream.add_layers(layer_dispatch_stream)
        lambda_geocode_property.add_layers(layer_geocode_property)
        lambda_fetch_properties.add_layers(layer_fetch_properties)

        # ENVIRONMENT VARIABLES

        lambda_geocode_property.add_environment(key='MONGODB_URI', value=mongodb_config.uri)
        lambda_geocode_property.add_environment(
            key='API_ACCESS_TOKEN_GEOCODING', value=access_keys_config.geocoding
        )
        lambda_fetch_properties.add_environment(key='MONGODB_URI', value=mongodb_config.uri)
        lambda_fetch_properties.add_environment(key='MONGODB_MAX_PAGE_SIZE', value=mongodb_config.max_page_size)

        # EXPOSED ENTITIES
        # -

"""
Copyright 2018-2019 Skyscanner Ltd

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
from datetime import date
from typing import Dict

import pytest

from pycfmodel import parse
from pycfmodel.resolver import resolve


@pytest.mark.parametrize(
    "function, expected_output", [({"Ref": "abc"}, "ABC"), ({"Ref": "potato"}, "UNDEFINED_PARAM_potato")]
)
def test_ref(function, expected_output):
    parameters = {"abc": "ABC"}
    mappings = {}
    conditions = {}

    assert resolve(function, parameters, mappings, conditions) == expected_output


@pytest.mark.parametrize(
    "function, expected_output",
    [({"Fn::ImportValue": "abc"}, "ABC"), ({"Fn::ImportValue": "potato"}, "UNDEFINED_PARAM_potato")],
)
def test_import_value(function, expected_output):
    parameters = {"abc": "ABC"}
    mappings = {}
    conditions = {}

    assert resolve(function, parameters, mappings, conditions) == expected_output


@pytest.mark.parametrize(
    "function, expected_output",
    [
        ({"Fn::Join": ["", []]}, ""),
        ({"Fn::Join": ["", ["aws"]]}, "aws"),
        (
            {"Fn::Join": ["", ["arn:", "aws", ":s3:::elasticbeanstalk-*-", "1234567890"]]},
            "arn:aws:s3:::elasticbeanstalk-*-1234567890",
        ),
    ],
)
def test_join(function, expected_output):
    parameters = {}
    mappings = {}
    conditions = {}

    assert resolve(function, parameters, mappings, conditions) == expected_output


@pytest.mark.parametrize(
    "function, expected_output",
    [
        ({"Fn::FindInMap": ["RegionMap", "eu-west-1", "HVM64"]}, "UNDEFINED_MAPPING_RegionMap_eu-west-1_HVM64"),
        ({"Fn::FindInMap": ["RegionMap", "us-east-1", "HVM128"]}, "UNDEFINED_MAPPING_RegionMap_us-east-1_HVM128"),
        ({"Fn::FindInMap": ["RegionMap", "us-east-1", "HVM64"]}, "ami-0ff8a91507f77f867"),
    ],
)
def test_find_in_map(function, expected_output):
    parameters = {}
    mappings = {"RegionMap": {"us-east-1": {"HVM64": "ami-0ff8a91507f77f867"}}}
    conditions = {}

    assert resolve(function, parameters, mappings, conditions) == expected_output


@pytest.mark.parametrize(
    "function, expected_output",
    [
        ({"Fn::Sub": "www.skyscanner.net"}, "www.skyscanner.net"),
        ({"Fn::Sub": ["www.${Domain}", {"Domain": "skyscanner.net"}]}, "www.skyscanner.net"),
        ({"Fn::Sub": "---${abc}---"}, "---ABC---"),
        ({"Fn::Sub": ["--${abc}-${def}--", {"def": "DEF"}]}, "--ABC-DEF--"),
    ],
)
def test_sub(function, expected_output):
    parameters = {"abc": "ABC"}
    mappings = {}
    conditions = {}

    assert resolve(function, parameters, mappings, conditions) == expected_output


@pytest.mark.parametrize(
    "function, expected_output",
    [
        ({"Fn::Select": ["0", ["apples", "grapes", "oranges", "mangoes"]]}, "apples"),
        ({"Fn::Select": ["1", ["apples", "grapes", "oranges", "mangoes"]]}, "grapes"),
        ({"Fn::Select": ["2", ["apples", "grapes", "oranges", "mangoes"]]}, "oranges"),
    ],
)
def test_select(function, expected_output):
    parameters = {}
    mappings = {}
    conditions = {}

    assert resolve(function, parameters, mappings, conditions) == expected_output


@pytest.mark.parametrize(
    "function, expected_output",
    [
        ({"Fn::Split": ["|", "a|b"]}, ["a", "b"]),
        ({"Fn::Split": ["|", "a|b|c|"]}, ["a", "b", "c", ""]),
        ({"Fn::Split": ["|", "|"]}, ["", ""]),
    ],
)
def test_split(function, expected_output):
    parameters = {}
    mappings = {}
    conditions = {}

    assert resolve(function, parameters, mappings, conditions) == expected_output


@pytest.mark.parametrize(
    "function, expected_output", [({"Fn::If": ["A", "a", "b"]}, "a"), ({"Fn::If": ["B", "a", "b"]}, "b")]
)
def test_if(function, expected_output):
    parameters = {}
    mappings = {}
    conditions = {"A": True, "B": False}

    assert resolve(function, parameters, mappings, conditions) == expected_output


@pytest.mark.parametrize(
    "function, expected_output",
    [
        ({"Fn::And": [True, True]}, True),
        ({"Fn::And": [False, True]}, False),
        ({"Fn::And": [True, False]}, False),
        ({"Fn::And": [False, False]}, False),
    ],
)
def test_and(function, expected_output):
    parameters = {}
    mappings = {}
    conditions = {}

    assert resolve(function, parameters, mappings, conditions) == expected_output


@pytest.mark.parametrize(
    "function, expected_output",
    [
        ({"Fn::Or": [True, True]}, True),
        ({"Fn::Or": [False, True]}, True),
        ({"Fn::Or": [True, False]}, True),
        ({"Fn::Or": [False, False]}, False),
    ],
)
def test_or(function, expected_output):
    parameters = {}
    mappings = {}
    conditions = {}

    assert resolve(function, parameters, mappings, conditions) == expected_output


@pytest.mark.parametrize("function, expected_output", [({"Fn::Not": [True]}, False), ({"Fn::Not": [False]}, True)])
def test_not(function, expected_output):
    parameters = {}
    mappings = {}
    conditions = {}

    assert resolve(function, parameters, mappings, conditions) == expected_output


@pytest.mark.parametrize(
    "function, expected_output",
    [
        ({"Fn::Equals": ["a", "a"]}, True),
        ({"Fn::Equals": ["a", "b"]}, False),
        ({"Fn::Equals": ["1123456789", 1123456789]}, True),
        ({"Fn::Equals": ["2019-12-10", date(2019, 12, 10)]}, True),
        ({"Fn::Equals": ["0.3", 0.3]}, True),
    ],
)
def test_equals(function, expected_output):
    parameters = {}
    mappings = {}
    conditions = {}

    assert resolve(function, parameters, mappings, conditions) == expected_output


@pytest.mark.parametrize("function, expected_output", [({"Fn::Base64": "holap :)"}, "aG9sYXAgOik=")])
def test_base64(function, expected_output):
    parameters = {}
    mappings = {}
    conditions = {}

    assert resolve(function, parameters, mappings, conditions) == expected_output


@pytest.mark.parametrize(
    "function, expected_output", [({"Fn::GetAtt": ["logicalNameOfResource", "attributeName"]}, "GETATT")]
)
def test_get_attr(function, expected_output):
    parameters = {}
    mappings = {}
    conditions = {}

    assert resolve(function, parameters, mappings, conditions) == expected_output


@pytest.mark.parametrize("function, expected_output", [({"Fn::GetAZs": ""}, "GETAZS")])
def test_get_azs(function, expected_output):
    parameters = {}
    mappings = {}
    conditions = {}

    assert resolve(function, parameters, mappings, conditions) == expected_output


@pytest.mark.parametrize("function, expected_output", [({"Condition": "SomeOtherCondition"}, True)])
def test_condition(function, expected_output):
    parameters = {}
    mappings = {}
    conditions = {"SomeOtherCondition": True}

    assert resolve(function, parameters, mappings, conditions) == expected_output


def test_select_and_ref():
    parameters = {"DbSubnetIpBlocks": ["10.0.48.0/24", "10.0.112.0/24", "10.0.176.0/24"]}
    mappings = {}
    conditions = {}
    function = {"Fn::Select": ["0", {"Ref": "DbSubnetIpBlocks"}]}

    assert resolve(function, parameters, mappings, conditions) == "10.0.48.0/24"


def test_join_and_ref():
    parameters = {"Partition": "patata", "AWS::AccountId": "1234567890"}
    mappings = {}
    conditions = {}
    function = {
        "Fn::Join": ["", ["arn:", {"Ref": "Partition"}, ":s3:::elasticbeanstalk-*-", {"Ref": "AWS::AccountId"}]]
    }
    assert resolve(function, parameters, mappings, conditions) == "arn:patata:s3:::elasticbeanstalk-*-1234567890"


def test_sub_and_ref():
    parameters = {"RootDomainName": "skyscanner.net"}
    mappings = {}
    conditions = {}
    function = {"Fn::Sub": ["www.${Domain}", {"Domain": {"Ref": "RootDomainName"}}]}

    assert resolve(function, parameters, mappings, conditions) == "www.skyscanner.net"


def test_select_and_split():
    parameters = {"AccountSubnetIDs": "id1,id2,id3"}
    mappings = {}
    conditions = {}
    function = {"Fn::Select": ["2", {"Fn::Split": [",", {"Ref": "AccountSubnetIDs"}]}]}

    assert resolve(function, parameters, mappings, conditions) == "id3"


def test_find_in_map_and_ref():
    parameters = {"AWS::Region": "us-east-1"}
    mappings = {"RegionMap": {"us-east-1": {"HVM64": "ami-0ff8a91507f77f867"}}}
    conditions = {}
    function = {"Fn::FindInMap": ["RegionMap", {"Ref": "AWS::Region"}, "HVM64"]}

    assert resolve(function, parameters, mappings, conditions) == "ami-0ff8a91507f77f867"


def test_template_conditions():
    template = {
        "Conditions": {
            "Bool": True,
            "BoolStr": "True",
            "IsEqualNum": {"Fn::Equals": [123456, 123456]},
            "IsEqualStr": {"Fn::Equals": ["a", "a"]},
            "IsEqualStr": {"Fn::Equals": [True, True]},
            "IsEqualRef": {"Fn::Equals": [{"Ref": "AWS::AccountId"}, "123"]},
            "Not": {"Fn::Not": [False]},
        },
        "Resources": {},
    }
    model = parse(template).resolve(extra_params={"AWS::AccountId": "123"})
    assert isinstance(model.Conditions, Dict)
    assert all(isinstance(cv, bool) for cv in model.Conditions.values())


def test_resolve_scenario_1():
    template = {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Parameters": {"StarParameter": {"Type": "String", "Default": "*", "Description": "Star Param"}},
        "Resources": {
            "rootRole": {
                "Type": "AWS::IAM::Role",
                "Properties": {
                    "AssumeRolePolicyDocument": {
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Effect": "Allow",
                                "Principal": {"AWS": {"Fn::Sub": "arn:aws:iam::${AWS::AccountId}:root"}},
                                "Action": ["sts:AssumeRole"],
                            }
                        ],
                    },
                    "Path": "/",
                    "Policies": [
                        {
                            "PolicyName": "root",
                            "PolicyDocument": {
                                "Version": "2012-10-17",
                                "Statement": [
                                    {
                                        "Effect": "Allow",
                                        "Action": {"Ref": "StarParameter"},
                                        "Resource": {"Ref": "StarParameter"},
                                    }
                                ],
                            },
                        }
                    ],
                },
            }
        },
    }

    model = parse(template).resolve(extra_params={"AWS::AccountId": "123"})
    role = model.Resources["rootRole"]
    policy = role.Properties.Policies[0]
    statement = policy.PolicyDocument.Statement[0]

    assert statement.Action == "*"
    assert statement.Resource == "*"
    assert role.Properties.AssumeRolePolicyDocument.Statement[0].Principal == {"AWS": "arn:aws:iam::123:root"}


def test_resolve_scenario_2():
    template = {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Description": "IAM role for Lambda",
        "Parameters": {"LambdaFunctionName": {"Description": "Name of the lambda function", "Type": "String"}},
        "Resources": {
            "lambdaRole": {
                "Properties": {
                    "AssumeRolePolicyDocument": {
                        "Statement": [
                            {
                                "Action": ["sts:AssumeRole"],
                                "Effect": "Allow",
                                "Principal": {"Service": ["lambda.amazonaws.com"]},
                            }
                        ],
                        "Version": "2012-10-17",
                    },
                    "Path": "/",
                    "Policies": [
                        {
                            "PolicyDocument": {
                                "Statement": [
                                    {
                                        "Action": ["lambda:*"],
                                        "Effect": "Allow",
                                        "Resource": [
                                            {
                                                "Fn::Sub": (
                                                    "arn:aws:lambda:*:${AWS::AccountId}:function:${LambdaFunctionName}"
                                                )
                                            }
                                        ],
                                    }
                                ],
                                "Version": "2012-10-17",
                            },
                            "PolicyName": "lambda_permissions",
                        },
                        {
                            "PolicyDocument": {
                                "Statement": [
                                    {
                                        "Action": ["xray:PutTraceSegments", "xray:PutTelemetryRecords"],
                                        "Effect": "Allow",
                                        "Resource": ["*"],
                                    }
                                ],
                                "Version": "2012-10-17",
                            },
                            "PolicyName": "AWSXrayWriteOnlyAccess",
                        },
                        {
                            "PolicyDocument": {
                                "Statement": [
                                    {
                                        "Action": ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"],
                                        "Effect": "Allow",
                                        "Resource": ["*"],
                                    }
                                ],
                                "Version": "2012-10-17",
                            },
                            "PolicyName": "Logging",
                        },
                    ],
                    "RoleName": {"Fn::Sub": "${LambdaFunctionName}-role"},
                },
                "Type": "AWS::IAM::Role",
            }
        },
    }
    model = parse(template).resolve(extra_params={"AWS::AccountId": "123", "LambdaFunctionName": "test-lambda"})
    assert (
        model.Resources["lambdaRole"].Properties.Policies[0].PolicyDocument.Statement[0].Resource[0]
        == "arn:aws:lambda:*:123:function:test-lambda"
    )
    assert model.Resources["lambdaRole"].Properties.RoleName == "test-lambda-role"

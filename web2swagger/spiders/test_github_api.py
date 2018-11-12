# -*- coding: utf-8 -*-
import pytest
from scrapy_tdd import *
from scrapy.selector import Selector

from api_swagger import ApiSwagger


def response_from(file_name, encoding="latin"):
    return mock_response_from_sample_file(my_path(__file__) + "/samples", file_name, encoding=encoding)

def describe_github_api_extraction():
    config_file = os.path.join(my_path(__file__), '..', 'config', 'github_back_to_back.py')

    to_test = ApiSwagger(config_file=config_file)

    def describe_github_api_for_releases():
        resp = response_from('Releases _ GitHub Developer Guide.html')
        result = to_test.parse_paths(resp)

        def it_should_extract_three_operations_on_release_ids():
            assert "/repos/{owner}/{repo}/releases/{release_id}" in result
            assert len(result["/repos/{owner}/{repo}/releases/{release_id}"]) == 3
            assert ['delete', 'get', 'patch'] == sorted(result["/repos/{owner}/{repo}/releases/{release_id}"].keys())

        def describe_get_operation():
            operation_result = result["/repos/{owner}/{repo}/releases/{release_id}"]['get']

            def it_has_3_in_path_parameters():
                assert len(operation_result['parameters']) == 3
 
            def it_has_one_response_code():
                assert len(operation_result['responses']) == 1
                assert "OK" == operation_result['responses']['200']['description']

        def describe_patch_operation():
            operation_result = result["/repos/{owner}/{repo}/releases/{release_id}"]['patch']

            def it_has_7_parameters(): # TODO: check indirection / level in structure
                #assert len(operation_result['parameters']) == 6
                print operation_result['parameters'][0]['schema']['properties']
                assert len(operation_result['parameters'][0]['schema']['properties']) == 6

            def it_has_one_response_code():
                assert len(operation_result['responses']) == 1
                assert "OK" == operation_result['responses']['200']['description']

        def describe_delete_operation():
            operation_result = result["/repos/{owner}/{repo}/releases/{release_id}"]['delete']

            def it_has_3_in_path_parameters():
                assert len(operation_result['parameters']) == 3

            def it_has_one_response_code():
                assert len(operation_result['responses']) == 1
                assert "No Content" == operation_result['responses']['204']['description']
# -*- coding: utf-8 -*-
from scrapy.utils.test import get_crawler
from scrapy_tdd import *
import pytest
import os

from swagger_helpers import *

def describe_swagger_helpers():

    def describe_split_json():

        def should_split_even_one_json_string():
            json_string = '[{"user": "jen"}, {"group": "developer"}]'
            collected_json = split_separated_json(json_string)

            assert len(collected_json) == 1
            assert collected_json[0] == '[{"user":"jen"}, {"group":"developer"}]'

            json_string = '{"self": "http://www.example.com/jira/rest/api/2/user?username=fred","name": "fred", "avatarUrls": { "24x24": "http://www.example.com/jira/secure/useravatar?size=small&ownerId=fred", "16x16": "http://www.example.com/jira/secure/useravatar?size=xsmall&ownerId=fred"}, "displayName": "Fred F. User", "active": false}'
            collected_json = split_separated_json(json_string)
            assert len(collected_json) == 1
            assert collected_json[0] == '{"self":"http://www.example.com/jira/rest/api/2/user?username=fred","name":"fred","avatarUrls": {"24x24":"http://www.example.com/jira/secure/useravatar?size=small&ownerId=fred","16x16":"http://www.example.com/jira/secure/useravatar?size=xsmall&ownerId=fred"},"displayName":"Fred F. User","active": false}'

        def should_split_proper_json_string_where_dict_ends_with_comma():
            json_string = '{ \" name \" : \" The Spencer Davis Group \" , }'
            collected_json = split_separated_json(json_string)

            assert len(collected_json) == 1
            assert collected_json[0] == '{"name":"The Spencer Davis Group"}'

        def should_split_json_strings_separated_by_or():
            json_string = "{ \"user\" : [\"admin\"] } or { \"group\" : [\"jira-developers\"] }"
            collected_json = split_separated_json(json_string)

            assert len(collected_json) == 2
            assert collected_json[0] == '{"user": ["admin"] }'
            assert collected_json[1] == '{"group": ["jira-developers"] }'

        def should_split_json_strings_separated_by_space():
            json_string = "{ \"user\" : [\"admin\"] } { \"group\" : [\"jira-developers\"] }"
            collected_json = split_separated_json(json_string)

            assert len(collected_json) == 2
            assert collected_json[0] == '{"user": ["admin"] }'
            assert collected_json[1] == '{"group": ["jira-developers"] }'

        def should_split_json_strings_even_subtypes_json():
            json_string = '{ "user": {"name": "jen"}, "group": ["admin", "developer"]} and {"info": "just a test"} {"all_groups": ["admin", "member", "developer"]}'
            collected_json = split_separated_json(json_string)

            assert len(collected_json) == 3
            assert '{"user": {"name":"jen"},"group": ["admin","developer"]}' in collected_json
            assert '{"all_groups": ["admin","member","developer"]}' in collected_json
            assert '{"info":"just a test"}' in collected_json

    def describe_convert_to_valid_types():

        def should_convert_to_integer():
            assert convert_to_valid_type('Uint32') == 'integer'
            assert convert_to_valid_type('float64') == 'integer'
            assert convert_to_valid_type('decimal') == 'integer'
            assert convert_to_valid_type('Int64') == 'integer'

        def should_convert_to_bool():
            assert convert_to_valid_type('Boolean') == 'boolean'
            assert convert_to_valid_type('bool') == 'boolean'

        def should_convert_to_string():
            assert convert_to_valid_type('String') == 'string'
            assert convert_to_valid_type('List') == 'string'
            assert convert_to_valid_type('MemberSelector') == 'string'

    def describe_fixSchemaDefinitions():
        json_data = {
                        "title": "Content Body", 
                        "id": "https://docs.atlassian.com/jira/REST/schema/content-body#", 
                        "additionalProperties": False, 
                        "definitions": {
                            "html-string": {
                                "type": "object", 
                                "title": "Html String"
                            }, 
                            "person": {
                                "anyOf": [
                                    {
                                        "$ref": "#/definitions/anonymous"
                                    }, 
                                    {
                                        "$ref": "#/definitions/known-user"
                                    }, 
                                    {
                                        "$ref": "#/definitions/unknown-user"
                                    }, 
                                    {
                                        "$ref": "#/definitions/user"
                                    }
                                ], 
                                "type": "object", 
                                "title": "Person"
                            }, 
                            "content-representation": {
                                "type": "object", 
                                "title": "Content Representation"
                            }, 
                            "unknown-user": {
                                "additionalProperties": False, 
                                "type": "object", 
                                "properties": {
                                    "username": {
                                        "type": "string"
                                    }, 
                                    "displayName": {
                                        "type": "string"
                                    }, 
                                    "profilePicture": {
                                        "$ref": "#/definitions/icon"
                                    }
                                }, 
                                "title": "Unknown User"
                            }, 
                            "content": {
                                "additionalProperties": False, 
                                "type": "object", 
                                "properties": {
                                    "status": {
                                        "type": "object", 
                                        "title": "Content Status"
                                    }, 
                                    "operations": {
                                        "items": {
                                            "additionalProperties": False, 
                                            "type": "object", 
                                            "properties": {
                                                "operation": {
                                                    "$ref": "#/definitions/operation-key"
                                                }
                                            }, 
                                            "title": "Operation Check Result"
                                        }, 
                                        "type": "array"
                                    }, 
                                    "ancestors": {
                                        "items": {
                                            "$ref": "#/definitions/content"
                                        }, 
                                        "type": "array"
                                    }, 
                                    "container": {
                                        "items": {
                                            "type": "object", 
                                            "title": "Container"
                                        }, 
                                        "type": "array"
                                    }, 
                                    "space": {
                                        "items": {
                                            "additionalProperties": False, 
                                            "type": "object", 
                                            "properties": {
                                                "description": {
                                                    "additionalProperties": False, 
                                                    "patternProperties": {
                                                        ".+": {
                                                            "additionalProperties": False, 
                                                            "type": "object", 
                                                            "properties": {
                                                                "webresource": {
                                                                    "items": {
                                                                        "$ref": "#/definitions/web-resource-dependencies"
                                                                    }, 
                                                                    "type": "array"
                                                                }, 
                                                                "value": {
                                                                    "type": "string"
                                                                }, 
                                                                "representation": {
                                                                    "$ref": "#/definitions/content-representation"
                                                                }
                                                            }, 
                                                            "title": "Formatted Body"
                                                        }
                                                    }, 
                                                    "type": "object"
                                                }, 
                                                "type": {
                                                    "type": "object", 
                                                    "title": "Space Type"
                                                }, 
                                                "name": {
                                                    "type": "string"
                                                }, 
                                                "key": {
                                                    "type": "string"
                                                }, 
                                                "metadata": {
                                                    "additionalProperties": False, 
                                                    "patternProperties": {
                                                        ".+": {}
                                                    }, 
                                                    "type": "object"
                                                }, 
                                                "homepage": {
                                                    "items": {
                                                        "$ref": "#/definitions/content"
                                                    }, 
                                                    "type": "array"
                                                }, 
                                                "id": {
                                                    "type": "integer"
                                                }, 
                                                "icon": {
                                                    "items": {
                                                        "$ref": "#/definitions/icon"
                                                    }, 
                                                    "type": "array"
                                                }
                                            }, 
                                            "title": "Space"
                                        }, 
                                        "type": "array"
                                    }, 
                                    "descendants": {
                                        "additionalProperties": False, 
                                        "patternProperties": {
                                            ".+": {
                                                "items": {
                                                    "$ref": "#/definitions/content"
                                                }, 
                                                "type": "array"
                                            }
                                        }, 
                                        "type": "object"
                                    }, 
                                    "title": {
                                        "type": "string"
                                    }, 
                                    "body": {
                                        "additionalProperties": False, 
                                        "patternProperties": {
                                            ".+": {
                                                "additionalProperties": False, 
                                                "type": "object", 
                                                "properties": {
                                                    "content": {
                                                        "items": {
                                                            "$ref": "#/definitions/content"
                                                        }, 
                                                        "type": "array"
                                                    }, 
                                                    "webresource": {
                                                        "items": {
                                                            "$ref": "#/definitions/web-resource-dependencies"
                                                        }, 
                                                        "type": "array"
                                                    }, 
                                                    "value": {
                                                        "type": "string"
                                                    }, 
                                                    "representation": {
                                                        "$ref": "#/definitions/content-representation"
                                                    }
                                                }, 
                                                "title": "Content Body"
                                            }
                                        }, 
                                        "type": "object"
                                    }, 
                                    "children": {
                                        "additionalProperties": False, 
                                        "patternProperties": {
                                            ".+": {
                                                "items": {
                                                    "$ref": "#/definitions/content"
                                                }, 
                                                "type": "array"
                                            }
                                        }, 
                                        "type": "object"
                                    }, 
                                    "version": {
                                        "items": {
                                            "$ref": "#/definitions/version"
                                        }, 
                                        "type": "array"
                                    }, 
                                    "extensions": {
                                        "additionalProperties": False, 
                                        "patternProperties": {
                                            ".+": {}
                                        }, 
                                        "type": "object"
                                    }, 
                                    "restrictions": {
                                        "additionalProperties": False, 
                                        "patternProperties": {
                                            ".+": {
                                                "additionalProperties": False, 
                                                "type": "object", 
                                                "properties": {
                                                    "content": {
                                                        "items": {
                                                            "$ref": "#/definitions/content"
                                                        }, 
                                                        "type": "array"
                                                    }, 
                                                    "restrictions": {
                                                        "items": {
                                                            "additionalProperties": False, 
                                                            "type": "object", 
                                                            "properties": {
                                                                "group": {
                                                                    "items": {
                                                                        "additionalProperties": False, 
                                                                        "type": "object", 
                                                                        "properties": {
                                                                            "name": {
                                                                                "type": "string"
                                                                            }
                                                                        }, 
                                                                        "title": "Group"
                                                                    }, 
                                                                    "type": "array"
                                                                }, 
                                                                "user": {
                                                                    "items": {
                                                                        "$ref": "#/definitions/user"
                                                                    }, 
                                                                    "type": "array"
                                                                }
                                                            }, 
                                                            "title": "Subject Restrictions"
                                                        }, 
                                                        "type": "array"
                                                    }, 
                                                    "operation": {
                                                        "$ref": "#/definitions/operation-key"
                                                    }
                                                }, 
                                                "title": "Content Restriction"
                                            }
                                        }, 
                                        "type": "object"
                                    }, 
                                    "metadata": {
                                        "additionalProperties": False, 
                                        "patternProperties": {
                                            ".+": {}
                                        }, 
                                        "type": "object"
                                    }, 
                                    "type": {
                                        "type": "object", 
                                        "title": "Content Type"
                                    }, 
                                    "id": {
                                        "type": "object", 
                                        "title": "Content Id"
                                    }, 
                                    "history": {
                                        "items": {
                                            "additionalProperties": False, 
                                            "required": [
                                                "latest"
                                            ], 
                                            "type": "object", 
                                            "properties": {
                                                "contributors": {
                                                    "items": {
                                                        "additionalProperties": False, 
                                                        "type": "object", 
                                                        "properties": {
                                                            "publishers": {
                                                                "items": {
                                                                    "additionalProperties": False, 
                                                                    "type": "object", 
                                                                    "properties": {
                                                                        "userKeys": {
                                                                            "items": {
                                                                                "type": "string"
                                                                            }, 
                                                                            "type": "array"
                                                                        }, 
                                                                        "users": {
                                                                            "items": {
                                                                                "$ref": "#/definitions/person"
                                                                            }, 
                                                                            "type": "array"
                                                                        }
                                                                    }, 
                                                                    "title": "Contributor Users"
                                                                }, 
                                                                "type": "array"
                                                            }
                                                        }, 
                                                        "title": "Contributors"
                                                    }, 
                                                    "type": "array"
                                                }, 
                                                "nextVersion": {
                                                    "items": {
                                                        "$ref": "#/definitions/version"
                                                    }, 
                                                    "type": "array"
                                                }, 
                                                "lastUpdated": {
                                                    "items": {
                                                        "$ref": "#/definitions/version"
                                                    }, 
                                                    "type": "array"
                                                }, 
                                                "previousVersion": {
                                                    "items": {
                                                        "$ref": "#/definitions/version"
                                                    }, 
                                                    "type": "array"
                                                }, 
                                                "createdBy": {
                                                    "$ref": "#/definitions/person"
                                                }, 
                                                "createdDate": {
                                                    "type": "string"
                                                }, 
                                                "latest": {
                                                    "type": "boolean"
                                                }
                                            }, 
                                            "title": "History"
                                        }, 
                                        "type": "array"
                                    }
                                }, 
                                "title": "Content"
                            }, 
                            "known-user": {
                                "additionalProperties": False, 
                                "type": "object", 
                                "properties": {
                                    "username": {
                                        "type": "string"
                                    }, 
                                    "status": {
                                        "items": {
                                            "type": "object", 
                                            "title": "User Status"
                                        }, 
                                        "type": "array"
                                    }, 
                                    "displayName": {
                                        "type": "string"
                                    }, 
                                    "profilePicture": {
                                        "$ref": "#/definitions/icon"
                                    }
                                }, 
                                "title": "Known User"
                            }, 
                            "web-resource-dependencies": {
                                "additionalProperties": False, 
                                "type": "object", 
                                "properties": {
                                    "keys": {
                                        "items": {
                                            "type": "string"
                                        }, 
                                        "type": "array"
                                    }, 
                                    "contexts": {
                                        "items": {
                                            "type": "string"
                                        }, 
                                        "type": "array"
                                    }, 
                                    "superbatch": {
                                        "items": {
                                            "additionalProperties": False, 
                                            "type": "object", 
                                            "properties": {
                                                "metatags": {
                                                    "items": {
                                                        "$ref": "#/definitions/html-string"
                                                    }, 
                                                    "type": "array"
                                                }, 
                                                "uris": {
                                                    "additionalProperties": False, 
                                                    "patternProperties": {
                                                        ".+": {
                                                            "items": {
                                                                "type": "string", 
                                                                "format": "uri"
                                                            }, 
                                                            "type": "array"
                                                        }
                                                    }, 
                                                    "type": "object"
                                                }, 
                                                "tags": {
                                                    "additionalProperties": False, 
                                                    "patternProperties": {
                                                        ".+": {
                                                            "$ref": "#/definitions/html-string"
                                                        }
                                                    }, 
                                                    "type": "object"
                                                }
                                            }, 
                                            "title": "Super Batch Web Resources"
                                        }, 
                                        "type": "array"
                                    }, 
                                    "uris": {
                                        "additionalProperties": False, 
                                        "patternProperties": {
                                            ".+": {
                                                "items": {
                                                    "type": "string", 
                                                    "format": "uri"
                                                }, 
                                                "type": "array"
                                            }
                                        }, 
                                        "type": "object"
                                    }, 
                                    "tags": {
                                        "additionalProperties": False, 
                                        "patternProperties": {
                                            ".+": {
                                                "$ref": "#/definitions/html-string"
                                            }
                                        }, 
                                        "type": "object"
                                    }
                                }, 
                                "title": "Web Resource Dependencies"
                            }, 
                            "version": {
                                "additionalProperties": False, 
                                "required": [
                                    "number", 
                                    "minorEdit", 
                                    "hidden"
                                ], 
                                "type": "object", 
                                "properties": {
                                    "syncRev": {
                                        "type": "string"
                                    }, 
                                    "when": {
                                        "type": "string"
                                    }, 
                                    "number": {
                                        "type": "integer"
                                    }, 
                                    "by": {
                                        "$ref": "#/definitions/person"
                                    }, 
                                    "content": {
                                        "items": {
                                            "$ref": "#/definitions/content"
                                        }, 
                                        "type": "array"
                                    }, 
                                    "message": {
                                        "type": "string"
                                    }, 
                                    "hidden": {
                                        "type": "boolean"
                                    }, 
                                    "minorEdit": {
                                        "type": "boolean"
                                    }
                                }, 
                                "title": "Version"
                            }, 
                            "operation-key": {
                                "type": "object", 
                                "title": "Operation Key"
                            }, 
                            "user": {
                                "additionalProperties": False, 
                                "type": "object", 
                                "properties": {
                                    "username": {
                                        "type": "string"
                                    }, 
                                    "displayName": {
                                        "type": "string"
                                    }, 
                                    "profilePicture": {
                                        "$ref": "#/definitions/icon"
                                    }
                                }, 
                                "title": "User"
                            }, 
                            "anonymous": {
                                "additionalProperties": False, 
                                "type": "object", 
                                "properties": {
                                    "type": {
                                        "type": "string"
                                    }, 
                                    "displayName": {
                                        "type": "string"
                                    }, 
                                    "profilePicture": {
                                        "$ref": "#/definitions/icon"
                                    }
                                }, 
                                "title": "Anonymous"
                            }, 
                            "icon": {
                                "additionalProperties": False, 
                                "required": [
                                    "width", 
                                    "height", 
                                    "isDefault"
                                ], 
                                "type": "object", 
                                "properties": {
                                    "path": {
                                        "type": "string"
                                    }, 
                                    "height": {
                                        "type": "integer"
                                    }, 
                                    "isDefault": {
                                        "type": "boolean"
                                    }, 
                                    "width": {
                                        "type": "integer"
                                    }
                                }, 
                                "title": "Icon"
                            }
                        }, 
                        "type": "object", 
                        "properties": {
                            "content": {
                                "items": {
                                    "$ref": "#/definitions/content"
                                }, 
                                "type": "array"
                            }, 
                            "webresource": {
                                "items": {
                                    "$ref": "#/definitions/web-resource-dependencies"
                                }, 
                                "type": "array"
                            }, 
                            "value": {
                                "type": "string"
                            }, 
                            "representation": {
                                "$ref": "#/definitions/content-representation"
                            }
                        }
                    }

        fixed_schema = fixSchemaDefinition(json_data)
        definitions = json_data.get('definitions')

        def should_fix_type_to_string_for_missing_object_properties():
            assert fixed_schema['definitions']['html-string']['type'] == 'string'
            assert fixed_schema['definitions']['content-representation']['type'] == 'string'

        def should_not_convert_type_to_string_for_existing_object_properties():
            assert fixed_schema['definitions']['unknown-user']['type'] == 'object'

        # def should_be_valid_schema():
        #     is_valid = False
        #     try:
        #         json.loads(str(fixed_schema))
        #         is_valid = True
        #     except:
        #         pass

        #     assert is_valid

        # def should_set_definitions_in_parameter_ref():
        #     assert '$ref' not in fixed_schema["properties"]["content"]["items"]
        #     assert fixed_schema["properties"]["content"]["items"] == definitions["content"]
        #     assert '$ref' not in fixed_schema["properties"]["webresource"]["items"]
        #     assert fixed_schema["properties"]["webresource"]["items"] == definitions["web-resource-dependencies"]
        
        # def should_remove_definitions():
        #     assert 'definitions' not in fixed_schema

        # def should_remove_id():
        #     assert 'id' not in fixed_schema

    def describe_extraction_of_definitions_from_schema():
        json_data = {
                        "title": "Content Body", 
                        "id": "https://docs.atlassian.com/jira/REST/schema/content-body#", 
                        "additionalProperties": False, 
                        "definitions": {
                            "html-string": {
                                "type": "object", 
                                "title": "Html String"
                            }, 
                            "person": {
                                "anyOf": [
                                    {
                                        "$ref": "#/definitions/anonymous"
                                    }, 
                                    {
                                        "$ref": "#/definitions/known-user"
                                    }, 
                                    {
                                        "$ref": "#/definitions/unknown-user"
                                    }, 
                                    {
                                        "$ref": "#/definitions/user"
                                    }
                                ], 
                                "type": "object", 
                                "title": "Person"
                            }, 
                            "content-representation": {
                                "type": "object", 
                                "title": "Content Representation"
                            }, 
                            "unknown-user": {
                                "additionalProperties": False, 
                                "type": "object", 
                                "properties": {
                                    "username": {
                                        "type": "string"
                                    }, 
                                    "displayName": {
                                        "type": "string"
                                    }, 
                                    "profilePicture": {
                                        "$ref": "#/definitions/icon"
                                    }
                                }, 
                                "title": "Unknown User"
                            }, 
                            "content": {
                                "additionalProperties": False, 
                                "type": "object", 
                                "properties": {
                                    "status": {
                                        "type": "object", 
                                        "title": "Content Status"
                                    }, 
                                    "operations": {
                                        "items": {
                                            "additionalProperties": False, 
                                            "type": "object", 
                                            "properties": {
                                                "operation": {
                                                    "$ref": "#/definitions/operation-key"
                                                }
                                            }, 
                                            "title": "Operation Check Result"
                                        }, 
                                        "type": "array"
                                    }, 
                                    "ancestors": {
                                        "items": {
                                            "$ref": "#/definitions/content"
                                        }, 
                                        "type": "array"
                                    }, 
                                    "container": {
                                        "items": {
                                            "type": "object", 
                                            "title": "Container"
                                        }, 
                                        "type": "array"
                                    }, 
                                    "space": {
                                        "items": {
                                            "additionalProperties": False, 
                                            "type": "object", 
                                            "properties": {
                                                "description": {
                                                    "additionalProperties": False, 
                                                    "patternProperties": {
                                                        ".+": {
                                                            "additionalProperties": False, 
                                                            "type": "object", 
                                                            "properties": {
                                                                "webresource": {
                                                                    "items": {
                                                                        "$ref": "#/definitions/web-resource-dependencies"
                                                                    }, 
                                                                    "type": "array"
                                                                }, 
                                                                "value": {
                                                                    "type": "string"
                                                                }, 
                                                                "representation": {
                                                                    "$ref": "#/definitions/content-representation"
                                                                }
                                                            }, 
                                                            "title": "Formatted Body"
                                                        }
                                                    }, 
                                                    "type": "object"
                                                }, 
                                                "type": {
                                                    "type": "object", 
                                                    "title": "Space Type"
                                                }, 
                                                "name": {
                                                    "type": "string"
                                                }, 
                                                "key": {
                                                    "type": "string"
                                                }, 
                                                "metadata": {
                                                    "additionalProperties": False, 
                                                    "patternProperties": {
                                                        ".+": {}
                                                    }, 
                                                    "type": "object"
                                                }, 
                                                "homepage": {
                                                    "items": {
                                                        "$ref": "#/definitions/content"
                                                    }, 
                                                    "type": "array"
                                                }, 
                                                "id": {
                                                    "type": "integer"
                                                }, 
                                                "icon": {
                                                    "items": {
                                                        "$ref": "#/definitions/icon"
                                                    }, 
                                                    "type": "array"
                                                }
                                            }, 
                                            "title": "Space"
                                        }, 
                                        "type": "array"
                                    }, 
                                    "descendants": {
                                        "additionalProperties": False, 
                                        "patternProperties": {
                                            ".+": {
                                                "items": {
                                                    "$ref": "#/definitions/content"
                                                }, 
                                                "type": "array"
                                            }
                                        }, 
                                        "type": "object"
                                    }, 
                                    "title": {
                                        "type": "string"
                                    }, 
                                    "body": {
                                        "additionalProperties": False, 
                                        "patternProperties": {
                                            ".+": {
                                                "additionalProperties": False, 
                                                "type": "object", 
                                                "properties": {
                                                    "content": {
                                                        "items": {
                                                            "$ref": "#/definitions/content"
                                                        }, 
                                                        "type": "array"
                                                    }, 
                                                    "webresource": {
                                                        "items": {
                                                            "$ref": "#/definitions/web-resource-dependencies"
                                                        }, 
                                                        "type": "array"
                                                    }, 
                                                    "value": {
                                                        "type": "string"
                                                    }, 
                                                    "representation": {
                                                        "$ref": "#/definitions/content-representation"
                                                    }
                                                }, 
                                                "title": "Content Body"
                                            }
                                        }, 
                                        "type": "object"
                                    }, 
                                    "children": {
                                        "additionalProperties": False, 
                                        "patternProperties": {
                                            ".+": {
                                                "items": {
                                                    "$ref": "#/definitions/content"
                                                }, 
                                                "type": "array"
                                            }
                                        }, 
                                        "type": "object"
                                    }, 
                                    "version": {
                                        "items": {
                                            "$ref": "#/definitions/version"
                                        }, 
                                        "type": "array"
                                    }, 
                                    "extensions": {
                                        "additionalProperties": False, 
                                        "patternProperties": {
                                            ".+": {}
                                        }, 
                                        "type": "object"
                                    }, 
                                    "restrictions": {
                                        "additionalProperties": False, 
                                        "patternProperties": {
                                            ".+": {
                                                "additionalProperties": False, 
                                                "type": "object", 
                                                "properties": {
                                                    "content": {
                                                        "items": {
                                                            "$ref": "#/definitions/content"
                                                        }, 
                                                        "type": "array"
                                                    }, 
                                                    "restrictions": {
                                                        "items": {
                                                            "additionalProperties": False, 
                                                            "type": "object", 
                                                            "properties": {
                                                                "group": {
                                                                    "items": {
                                                                        "additionalProperties": False, 
                                                                        "type": "object", 
                                                                        "properties": {
                                                                            "name": {
                                                                                "type": "string"
                                                                            }
                                                                        }, 
                                                                        "title": "Group"
                                                                    }, 
                                                                    "type": "array"
                                                                }, 
                                                                "user": {
                                                                    "items": {
                                                                        "$ref": "#/definitions/user"
                                                                    }, 
                                                                    "type": "array"
                                                                }
                                                            }, 
                                                            "title": "Subject Restrictions"
                                                        }, 
                                                        "type": "array"
                                                    }, 
                                                    "operation": {
                                                        "$ref": "#/definitions/operation-key"
                                                    }
                                                }, 
                                                "title": "Content Restriction"
                                            }
                                        }, 
                                        "type": "object"
                                    }, 
                                    "metadata": {
                                        "additionalProperties": False, 
                                        "patternProperties": {
                                            ".+": {}
                                        }, 
                                        "type": "object"
                                    }, 
                                    "type": {
                                        "type": "object", 
                                        "title": "Content Type"
                                    }, 
                                    "id": {
                                        "type": "object", 
                                        "title": "Content Id"
                                    }, 
                                    "history": {
                                        "items": {
                                            "additionalProperties": False, 
                                            "required": [
                                                "latest"
                                            ], 
                                            "type": "object", 
                                            "properties": {
                                                "contributors": {
                                                    "items": {
                                                        "additionalProperties": False, 
                                                        "type": "object", 
                                                        "properties": {
                                                            "publishers": {
                                                                "items": {
                                                                    "additionalProperties": False, 
                                                                    "type": "object", 
                                                                    "properties": {
                                                                        "userKeys": {
                                                                            "items": {
                                                                                "type": "string"
                                                                            }, 
                                                                            "type": "array"
                                                                        }, 
                                                                        "users": {
                                                                            "items": {
                                                                                "$ref": "#/definitions/person"
                                                                            }, 
                                                                            "type": "array"
                                                                        }
                                                                    }, 
                                                                    "title": "Contributor Users"
                                                                }, 
                                                                "type": "array"
                                                            }
                                                        }, 
                                                        "title": "Contributors"
                                                    }, 
                                                    "type": "array"
                                                }, 
                                                "nextVersion": {
                                                    "items": {
                                                        "$ref": "#/definitions/version"
                                                    }, 
                                                    "type": "array"
                                                }, 
                                                "lastUpdated": {
                                                    "items": {
                                                        "$ref": "#/definitions/version"
                                                    }, 
                                                    "type": "array"
                                                }, 
                                                "previousVersion": {
                                                    "items": {
                                                        "$ref": "#/definitions/version"
                                                    }, 
                                                    "type": "array"
                                                }, 
                                                "createdBy": {
                                                    "$ref": "#/definitions/person"
                                                }, 
                                                "createdDate": {
                                                    "type": "string"
                                                }, 
                                                "latest": {
                                                    "type": "boolean"
                                                }
                                            }, 
                                            "title": "History"
                                        }, 
                                        "type": "array"
                                    }
                                }, 
                                "title": "Content"
                            }, 
                            "known-user": {
                                "additionalProperties": False, 
                                "type": "object", 
                                "properties": {
                                    "username": {
                                        "type": "string"
                                    }, 
                                    "status": {
                                        "items": {
                                            "type": "object", 
                                            "title": "User Status"
                                        }, 
                                        "type": "array"
                                    }, 
                                    "displayName": {
                                        "type": "string"
                                    }, 
                                    "profilePicture": {
                                        "$ref": "#/definitions/icon"
                                    }
                                }, 
                                "title": "Known User"
                            }, 
                            "web-resource-dependencies": {
                                "additionalProperties": False, 
                                "type": "object", 
                                "properties": {
                                    "keys": {
                                        "items": {
                                            "type": "string"
                                        }, 
                                        "type": "array"
                                    }, 
                                    "contexts": {
                                        "items": {
                                            "type": "string"
                                        }, 
                                        "type": "array"
                                    }, 
                                    "superbatch": {
                                        "items": {
                                            "additionalProperties": False, 
                                            "type": "object", 
                                            "properties": {
                                                "metatags": {
                                                    "items": {
                                                        "$ref": "#/definitions/html-string"
                                                    }, 
                                                    "type": "array"
                                                }, 
                                                "uris": {
                                                    "additionalProperties": False, 
                                                    "patternProperties": {
                                                        ".+": {
                                                            "items": {
                                                                "type": "string", 
                                                                "format": "uri"
                                                            }, 
                                                            "type": "array"
                                                        }
                                                    }, 
                                                    "type": "object"
                                                }, 
                                                "tags": {
                                                    "additionalProperties": False, 
                                                    "patternProperties": {
                                                        ".+": {
                                                            "$ref": "#/definitions/html-string"
                                                        }
                                                    }, 
                                                    "type": "object"
                                                }
                                            }, 
                                            "title": "Super Batch Web Resources"
                                        }, 
                                        "type": "array"
                                    }, 
                                    "uris": {
                                        "additionalProperties": False, 
                                        "patternProperties": {
                                            ".+": {
                                                "items": {
                                                    "type": "string", 
                                                    "format": "uri"
                                                }, 
                                                "type": "array"
                                            }
                                        }, 
                                        "type": "object"
                                    }, 
                                    "tags": {
                                        "additionalProperties": False, 
                                        "patternProperties": {
                                            ".+": {
                                                "$ref": "#/definitions/html-string"
                                            }
                                        }, 
                                        "type": "object"
                                    }
                                }, 
                                "title": "Web Resource Dependencies"
                            }, 
                            "version": {
                                "additionalProperties": False, 
                                "required": [
                                    "number", 
                                    "minorEdit", 
                                    "hidden"
                                ], 
                                "type": "object", 
                                "properties": {
                                    "syncRev": {
                                        "type": "string"
                                    }, 
                                    "when": {
                                        "type": "string"
                                    }, 
                                    "number": {
                                        "type": "integer"
                                    }, 
                                    "by": {
                                        "$ref": "#/definitions/person"
                                    }, 
                                    "content": {
                                        "items": {
                                            "$ref": "#/definitions/content"
                                        }, 
                                        "type": "array"
                                    }, 
                                    "message": {
                                        "type": "string"
                                    }, 
                                    "hidden": {
                                        "type": "boolean"
                                    }, 
                                    "minorEdit": {
                                        "type": "boolean"
                                    }
                                }, 
                                "title": "Version"
                            }, 
                            "operation-key": {
                                "type": "object", 
                                "title": "Operation Key"
                            }, 
                            "user": {
                                "additionalProperties": False, 
                                "type": "object", 
                                "properties": {
                                    "username": {
                                        "type": "string"
                                    }, 
                                    "displayName": {
                                        "type": "string"
                                    }, 
                                    "profilePicture": {
                                        "$ref": "#/definitions/icon"
                                    }
                                }, 
                                "title": "User"
                            }, 
                            "anonymous": {
                                "additionalProperties": False, 
                                "type": "object", 
                                "properties": {
                                    "type": {
                                        "type": "string"
                                    }, 
                                    "displayName": {
                                        "type": "string"
                                    }, 
                                    "profilePicture": {
                                        "$ref": "#/definitions/icon"
                                    }
                                }, 
                                "title": "Anonymous"
                            }, 
                            "icon": {
                                "additionalProperties": False, 
                                "required": [
                                    "width", 
                                    "height", 
                                    "isDefault"
                                ], 
                                "type": "object", 
                                "properties": {
                                    "path": {
                                        "type": "string"
                                    }, 
                                    "height": {
                                        "type": "integer"
                                    }, 
                                    "isDefault": {
                                        "type": "boolean"
                                    }, 
                                    "width": {
                                        "type": "integer"
                                    }
                                }, 
                                "title": "Icon"
                            }
                        }, 
                        "type": "object", 
                        "properties": {
                            "content": {
                                "items": {
                                    "$ref": "#/definitions/content"
                                }, 
                                "type": "array"
                            }, 
                            "webresource": {
                                "items": {
                                    "$ref": "#/definitions/web-resource-dependencies"
                                }, 
                                "type": "array"
                            }, 
                            "value": {
                                "type": "string"
                            }, 
                            "representation": {
                                "$ref": "#/definitions/content-representation"
                            }
                        }
                    }

        def it_should_extract_definitions():
            definitions = extract_schema_definitions(json_data)

            assert definitions
            assert 'html-string' in definitions
            assert 'person' in definitions
            assert 'content-representation' in definitions
            assert 'unknown-user' in definitions
            assert 'content' in definitions
            assert 'known-user' in definitions
            assert 'web-resource-dependencies' in definitions
            assert 'version' in definitions
            assert 'operation-key' in definitions
            assert 'user' in definitions
            assert 'anonymous' in definitions
            assert 'icon' in definitions

    def should_find_key_value():
        assert is_value_exists_in_list_of_dicts(
            [{'required': True, 'in': 'path', 'type': u'string', 'name': u'projectIdOrKey', 'description': u'the project id or project key'}],
            'name', 'projectIdOrKey')

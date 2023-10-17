import io
from textwrap import dedent

import pytest
import json
from typing import Dict, Any

from mm2csv import MindMeisterExtractor


@pytest.fixture
def data() -> Dict[str, Any]:
    map = """
    {
      "map_version": "3.0",
      "root": {
        "id": 2997460696,
        "title": "root",
        "rank": null,
        "pos": [
          null,
          null
        ],
        "icon": null,
        "style": null,
        "created_at": "2023-10-17T20:49:22.000Z",
        "updated_at": "2023-10-17T20:49:37.000Z",
        "note": null,
        "link": null,
        "task": {
          "from": null,
          "until": null,
          "resource": null,
          "effort": null,
          "notify": 1
        },
        "external_task": null,
        "attachments": [],
        "image": null,
        "children": [
          {
            "id": 2997460697,
            "title": "level 1",
            "rank": 1,
            "pos": [
              170,
              -63
            ],
            "icon": null,
            "style": null,
            "created_at": "2023-10-17T20:49:22.000Z",
            "updated_at": "2023-10-17T20:49:43.000Z",
            "note": null,
            "link": null,
            "task": {
              "from": null,
              "until": null,
              "resource": null,
              "effort": null,
              "notify": 1
            },
            "external_task": null,
            "attachments": [],
            "image": null,
            "children": [
              {
                "id": 2997460698,
                "title": "sub level 1.1",
                "rank": 1,
                "pos": [
                  null,
                  null
                ],
                "icon": null,
                "style": null,
                "created_at": "2023-10-17T20:49:22.000Z",
                "updated_at": "2023-10-17T20:50:20.000Z",
                "note": null,
                "link": null,
                "task": {
                  "from": null,
                  "until": null,
                  "resource": null,
                  "effort": null,
                  "notify": 1
                },
                "external_task": null,
                "attachments": [],
                "image": null,
                "children": [
                  {
                    "id": 2997462463,
                    "title": "sub sub level 1.1.1",
                    "rank": 1,
                    "pos": [
                      409,
                      -124
                    ],
                    "icon": null,
                    "style": null,
                    "created_at": "2023-10-17T20:51:07.000Z",
                    "updated_at": "2023-10-17T20:51:07.000Z",
                    "note": null,
                    "link": null,
                    "task": {
                      "from": null,
                      "until": null,
                      "resource": null,
                      "effort": null,
                      "notify": 1
                    },
                    "external_task": null,
                    "attachments": [],
                    "image": null,
                    "children": [],
                    "boundary": null,
                    "video": null,
                    "property": {
                      "id": 401124473,
                      "idea_id": 2997462463,
                      "floating": false,
                      "offset_x": 0,
                      "offset_y": 0,
                      "free": false,
                      "layout": null
                    }
                  }
                ],
                "boundary": null,
                "video": null,
                "property": null
              },
              {
                "id": 2997461753,
                "title": "sub level 1.2",
                "rank": 2,
                "pos": [
                  226,
                  -34
                ],
                "icon": null,
                "style": null,
                "created_at": "2023-10-17T20:50:26.000Z",
                "updated_at": "2023-10-17T20:50:29.000Z",
                "note": null,
                "link": null,
                "task": {
                  "from": null,
                  "until": null,
                  "resource": null,
                  "effort": null,
                  "notify": 1
                },
                "external_task": null,
                "attachments": [],
                "image": null,
                "children": [],
                "boundary": null,
                "video": null,
                "property": {
                  "id": 401123949,
                  "idea_id": 2997461753,
                  "floating": false,
                  "offset_x": 0,
                  "offset_y": 0,
                  "free": false,
                  "layout": null
                }
              }
            ],
            "boundary": null,
            "video": null,
            "property": null
          },
          {
            "id": 2997460699,
            "title": "level 2",
            "rank": 2,
            "pos": [
              170,
              7
            ],
            "icon": null,
            "style": null,
            "created_at": "2023-10-17T20:49:22.000Z",
            "updated_at": "2023-10-17T20:50:04.000Z",
            "note": null,
            "link": null,
            "task": {
              "from": null,
              "until": null,
              "resource": null,
              "effort": null,
              "notify": 1
            },
            "external_task": null,
            "attachments": [],
            "image": null,
            "children": [
              {
                "id": 2997460700,
                "title": "sub level 2.1",
                "rank": 1,
                "pos": [
                  null,
                  null
                ],
                "icon": null,
                "style": null,
                "created_at": "2023-10-17T20:49:22.000Z",
                "updated_at": "2023-10-17T20:50:17.000Z",
                "note": null,
                "link": null,
                "task": {
                  "from": null,
                  "until": null,
                  "resource": null,
                  "effort": null,
                  "notify": 1
                },
                "external_task": null,
                "attachments": [],
                "image": null,
                "children": [],
                "boundary": null,
                "video": null,
                "property": null
              },
              {
                "id": 2997461863,
                "title": "sub level 2.2",
                "rank": 2,
                "pos": [
                  226,
                  73
                ],
                "icon": null,
                "style": null,
                "created_at": "2023-10-17T20:50:38.000Z",
                "updated_at": "2023-10-17T20:50:38.000Z",
                "note": null,
                "link": null,
                "task": {
                  "from": null,
                  "until": null,
                  "resource": null,
                  "effort": null,
                  "notify": 1
                },
                "external_task": null,
                "attachments": [],
                "image": null,
                "children": [
                  {
                    "id": 2997461994,
                    "title": "sub sub level 2.2.1",
                    "rank": 1,
                    "pos": [
                      409,
                      73
                    ],
                    "icon": null,
                    "style": null,
                    "created_at": "2023-10-17T20:50:45.000Z",
                    "updated_at": "2023-10-17T20:50:56.000Z",
                    "note": null,
                    "link": null,
                    "task": {
                      "from": null,
                      "until": null,
                      "resource": null,
                      "effort": null,
                      "notify": 1
                    },
                    "external_task": null,
                    "attachments": [],
                    "image": null,
                    "children": [],
                    "boundary": null,
                    "video": null,
                    "property": {
                      "id": 401124151,
                      "idea_id": 2997461994,
                      "floating": false,
                      "offset_x": 0,
                      "offset_y": 0,
                      "free": false,
                      "layout": null
                    }
                  }
                ],
                "boundary": null,
                "video": null,
                "property": {
                  "id": 401124055,
                  "idea_id": 2997461863,
                  "floating": false,
                  "offset_x": 0,
                  "offset_y": 0,
                  "free": false,
                  "layout": null
                }
              }
            ],
            "boundary": null,
            "video": null,
            "property": null
          },
          {
            "id": 2997463567,
            "title": "level 3",
            "rank": 3,
            "pos": [
              94,
              111
            ],
            "icon": null,
            "style": null,
            "created_at": "2023-10-17T20:51:15.000Z",
            "updated_at": "2023-10-17T20:51:15.000Z",
            "note": null,
            "link": null,
            "task": {
              "from": null,
              "until": null,
              "resource": null,
              "effort": null,
              "notify": 1
            },
            "external_task": null,
            "attachments": [],
            "image": null,
            "children": [],
            "boundary": null,
            "video": null,
            "property": {
              "id": 401125150,
              "idea_id": 2997463567,
              "floating": false,
              "offset_x": 0,
              "offset_y": 0,
              "free": false,
              "layout": null
            }
          }
        ],
        "boundary": null,
        "video": null,
        "property": {
          "id": 401123198,
          "idea_id": 2997460696,
          "floating": false,
          "offset_x": 0,
          "offset_y": 0,
          "free": false,
          "layout": "mind_map"
        }
      },
      "attachments": [],
      "connections": [],
      "images": [],
      "theme": {
        "name": "meister",
        "root_style": {
          "id": 1572841377,
          "fonts": [
            {
              "id": 1,
              "name": "Avenir",
              "url": null
            },
            {
              "id": 2,
              "name": "Segoe UI",
              "url": null
            },
            {
              "id": 3,
              "name": "Helvetica",
              "url": null
            },
            {
              "id": 4,
              "name": "Arial",
              "url": null
            },
            {
              "id": 5,
              "name": "sans-serif",
              "url": null
            }
          ],
          "fontSize": 150,
          "boxStyle": 1,
          "color": "3D474D",
          "backgroundColor": null,
          "borderColor": null,
          "bold": true,
          "italic": false,
          "gradient": 0,
          "boxShadow": false,
          "borderWidth": 1,
          "name": null
        },
        "root_children_style": {
          "id": 1572841378,
          "fonts": [
            {
              "id": 1,
              "name": "Avenir",
              "url": null
            },
            {
              "id": 2,
              "name": "Segoe UI",
              "url": null
            },
            {
              "id": 3,
              "name": "Helvetica",
              "url": null
            },
            {
              "id": 4,
              "name": "Arial",
              "url": null
            },
            {
              "id": 5,
              "name": "sans-serif",
              "url": null
            }
          ],
          "fontSize": 120,
          "boxStyle": 1,
          "color": "3D474D",
          "backgroundColor": null,
          "borderColor": null,
          "bold": false,
          "italic": false,
          "gradient": 0,
          "boxShadow": false,
          "borderWidth": 1,
          "name": null
        },
        "nodes_style": {
          "id": 1572841379,
          "fonts": [
            {
              "id": 1,
              "name": "Avenir",
              "url": null
            },
            {
              "id": 2,
              "name": "Segoe UI",
              "url": null
            },
            {
              "id": 3,
              "name": "Helvetica",
              "url": null
            },
            {
              "id": 4,
              "name": "Arial",
              "url": null
            },
            {
              "id": 5,
              "name": "sans-serif",
              "url": null
            }
          ],
          "fontSize": 120,
          "boxStyle": 1,
          "color": "3D474D",
          "backgroundColor": null,
          "borderColor": null,
          "bold": false,
          "italic": false,
          "gradient": 0,
          "boxShadow": false,
          "borderWidth": 1,
          "name": null
        },
        "root_selected_color": "00aaff",
        "root_children_selected_color": "00aaff",
        "nodes_selected_color": "00aaff",
        "background": {
          "image": null,
          "color": "ffffff",
          "repeat": true
        },
        "line": {
          "color": "B4B4B4",
          "style": 2
        },
        "id": 2861357,
        "styles": [],
        "boundary_styles": [],
        "thumbnail": "https://www.mindmeister.com/themes/mm19/meister.svg",
        "colors": [
          "ffffff",
          "B4B4B4",
          "3D474D"
        ]
      },
      "slides": [],
      "layout": 1
    }
    """
    return json.loads(dedent(map))


def test_parse(data: Dict[str, Any]):
    extractor = MindMeisterExtractor(
        print_numbers=True, print_ids=True, print_leaf_nodes=True,
    )
    extractor.output_file = io.StringIO()
    extractor.csv_writer = extractor.init_csv_writer()
    extractor.generate_id = lambda: "id"

    extractor.parse(
        parent_id=extractor.generate_id(),
        depth=0,
        numbers="1",
        node=data["root"],
    )

    output = extractor.output_file.getvalue()
    assert output == (
        "1,id.id,,root\r\n"
        "1.1,id.id,,level 1\r\n"
        "1.1.1,id.id,,sub level 1.1\r\n"
        "1.1.1.1,id.id,L,sub sub level 1.1.1\r\n"
        "1.1.2,id.id,L,sub level 1.2\r\n"
        "1.2,id.id,,level 2\r\n"
        "1.2.1,id.id,L,sub level 2.1\r\n"
        "1.2.2,id.id,,sub level 2.2\r\n"
        "1.2.2.1,id.id,L,sub sub level 2.2.1\r\n"
        "1.3,id.id,L,level 3\r\n"
    )

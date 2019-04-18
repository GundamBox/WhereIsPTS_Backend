# User api readme

[TOC]

## Search by name

### Request

**URL**: `/api/search/<string: name>`
**Method**: `GET`

**Data example**

> GET /api/search/CTI

### Response

**Code** : `200 OK`

**Content example**

```json
[
    {
        "name": "CTI",
        "lat": 25.068847, 
        "lng": 121.583156,
        "address": "store address",
        "news": "CTI TV",
        "switchable": false,
    },
    .....
]
```

## Search by latitude, longtitude

### Request

**URL**: `/api/search/<float: lat>,<float: lng>`
**Method**: `GET`

**Data example**

> GET /api/search/25.069333,121.581300

### Response

**Code** : `200 OK`

**Content example**

```json
[
    {
        "name": "CTI",
        "lat": 25.068847, 
        "lng": 121.583156,
        "address": "store address",
        "news": "CTI TV",
        "switchable": false,
    },
    .....
]
```
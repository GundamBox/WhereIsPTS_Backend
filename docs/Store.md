# User api readme

[TOC]

## Create

### Request

**URL**: `/api/store`
**Method**: `POST`
**Data constraints**

```json
{
    "name": "store name",
    "lat": "store latitude",
    "lng": "store longtitude",
    "address": "store address",
    "news": "tv channel that store played",
    "switchable": "tv channels is switchable?",
}
```

**Data example**

```json
{
    "name": "CTI",
    "lat": 25.068847, 
    "lng": 121.583156,
    "address": "store address",
    "news": "CTI TV",
    "switchable": false,
}
```

### Response

**Code** : `200 OK`

**Content example**

```json
{
    "id": 1
}
```

## Read

### Request

**URL**: `/api/store/<int: store_id>`
**Method**: `GET`

**Data example**

> GET /api/store/1

### Response

**Code** : `200 OK`

**Content example**

```json
{
    "name": "CTI",
    "lat": 25.068847, 
    "lng": 121.583156,
    "address": "store address",
    "news": "CTI TV",
    "switchable": false,
}
```

## Update

### Request

**URL**: `/api/store/<int: store_id>`
**Method**: `PUT`
**Data constraints**

```json
{
    "name": "store name",
    "lat": "store latitude",
    "lng": "store longtitude",
    "address": "store address",
    "news": "tv channel that store played",
    "switchable": "tv channels is switchable?",
}
```

**Data example**

```json
{
    "name": "CTI",
    "lat": 25.068847, 
    "lng": 121.583156,
    "address": "store address",
    "news": "CTI TV",
    "switchable": false,
}
```

### Response

**Code** : `200 OK`

**Content example**

```json
{
    "id": 1
}
```
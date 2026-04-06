# Complete Backend API for Congressional Trading Data

## Overview
This backend API serves as a comprehensive source for real congressional trading data, including detailed functionalities such as search, politician profiles, sector analysis, comparison tools, and a leaderboard.

## API Endpoints

### 1. Get Trading Data
- **Endpoint:** `/api/trading`
- **Method:** GET
- **Description:** Retrieves real trading data for congressional members.
- **Parameters:**
    - `limit` (optional): Number of records to return.
    - `offset` (optional): Number of records to skip.  

### 2. Search Politics
- **Endpoint:** `/api/search`
- **Method:** GET
- **Description:** Searches for politicians based on name or criteria.
- **Parameters:**
    - `query`: The search term.
    - `limit` (optional): Number of results to return.

### 3. Politician Profile
- **Endpoint:** `/api/politician/{id}`
- **Method:** GET
- **Description:** Retrieves detailed profile information for a specific politician.

### 4. Sector Analysis
- **Endpoint:** `/api/sector-analysis`
- **Method:** GET
- **Description:** Analyzes trading data by sector.

### 5. Comparison Tool
- **Endpoint:** `/api/comparison`
- **Method:** POST
- **Description:** Compares trading records between two or more politicians.
- **Body Parameters:**
    - `ids`: Array of politician IDs to compare.

### 6. Leaderboard
- **Endpoint:** `/api/leaderboard`
- **Method:** GET
- **Description:** Displays a leaderboard of top-performing politicians based on trading data.

## Implementation
- Use Flask/Django (or your preferred framework).
- Connect to an authoritative congressional trading data source.

## Example Response

```json
{
    "success": true,
    "data": [
        {
            "name": "John Doe",
            "trades": [...],
            "sector": "Technology",
            "performance": "Top 10%"
        },
        ...
    ]
}
```

## Summary
This API aims to provide users with insightful data and tools to analyze congressional trading activities effectively.
import pytest
from datetime import datetime
from autobyteus_community_tools.google.maps.maps_direction import GoogleMapsDirection
from autobyteus_community_tools.google.maps.models import Route, TransitStep

# Fixtures
@pytest.fixture
def start_address():
    return "Zum kappgraben 18, 13125 berlin"

@pytest.fixture
def destination_address():
    return "Lankwitz, 12247 Berlin"

@pytest.fixture
def maps_direction():
    tool = GoogleMapsDirection()
    yield tool

# Tests
@pytest.mark.asyncio
async def test_basic_route_search(maps_direction, start_address, destination_address):
    """Test basic route search functionality"""
    routes = await maps_direction.execute(
        source=start_address,
        destination=destination_address
    )
    
    assert isinstance(routes, list), "Should return a list of routes"
    assert len(routes) > 0, "Should find at least one route"
    
    first_route = routes[0]
    assert isinstance(first_route, Route)
    assert first_route.total_duration_minutes > 0
    assert isinstance(first_route.departure_time, datetime)
    assert isinstance(first_route.arrival_time, datetime)
    assert len(first_route.steps) > 0
    assert first_route.selected is True

@pytest.mark.asyncio
async def test_route_details(maps_direction, start_address, destination_address):
    """Test detailed route information"""
    routes = await maps_direction._execute(
        source=start_address,
        destination=destination_address
    )
    
    for route in routes:
        assert route.total_duration_minutes > 0
        assert route.departure_time < route.arrival_time
        
        for step in route.steps:
            assert isinstance(step, TransitStep)
            assert step.mode in ["BUS", "TRAIN", "WALK", "UNKNOWN"]
            
            if step.mode != "WALK":
                assert step.line is not None

@pytest.mark.asyncio
async def test_invalid_addresses(maps_direction):
    """Test handling of invalid addresses"""
    with pytest.raises(ValueError):
        await maps_direction._execute(
            source="",
            destination="Lankwitz, 12247 Berlin"
        )
    
    with pytest.raises(ValueError):
        await maps_direction._execute(
            source="Zum kappgraben 18, 13125 berlin",
            destination=""
        )

@pytest.mark.asyncio
async def test_multiple_routes(maps_direction, start_address, destination_address):
    """Test multiple routes structure and ordering"""
    routes = await maps_direction._execute(
        source=start_address,
        destination=destination_address
    )
    
    assert len(routes) > 1, "Should return multiple route options"
    
    selected_routes = [route for route in routes if route.selected]
    assert len(selected_routes) == 1, "Exactly one route should be selected"
    
    for i in range(1, len(routes)):
        assert routes[i].total_duration_minutes >= routes[i-1].total_duration_minutes, \
            "Routes should be ordered by duration"

@pytest.mark.asyncio
async def test_transit_steps(maps_direction, start_address, destination_address):
    """Test transit step details and structure"""
    routes = await maps_direction._execute(
        source=start_address,
        destination=destination_address
    )
    
    for route in routes:
        for step in route.steps:
            assert hasattr(step, 'mode')
            assert hasattr(step, 'line')
            assert hasattr(step, 'line_color')
            
            if step.mode in ["BUS", "TRAIN"]:
                assert step.line is not None, f"Missing line number for {step.mode}"
                if step.line_color:
                    assert step.line_color.startswith('rgb'), \
                        f"Invalid color format for {step.mode}: {step.line_color}"

@pytest.mark.asyncio
async def test_tool_usage(maps_direction):
    """Test tool usage documentation"""
    usage = maps_direction.tool_usage()
    assert isinstance(usage, str)
    assert "GoogleMapsDirection" in usage
    assert "source" in usage
    assert "destination" in usage

@pytest.mark.asyncio
async def test_no_routes_found(maps_direction):
    """Test handling when no routes are found"""
    routes = await maps_direction._execute(
        source="Invalid Address That Doesn't Exist 123",
        destination="Another Invalid Address 456"
    )
    assert len(routes) == 0, "Should return empty list when no routes found"
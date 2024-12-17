import asyncio
from datetime import datetime
from typing import List, Optional
from autobyteus.tools.base_tool import BaseTool
from brui_core.ui_integrator import UIIntegrator

from autobyteus_community_tools.google.maps.models import Route, TransitStep

class GoogleMapsDirection(BaseTool, UIIntegrator):
    def __init__(self):
        BaseTool.__init__(self)
        UIIntegrator.__init__(self)
        
        self.directions_button_selector = 'button[aria-label="Directions"]'
        self.source_input_selector = 'input[aria-label="Starting point Your location"]'
        self.destination_input_selector = 'input[aria-label="Choose destination, or click on the map..."]'
        self.route_item_selector = '.UgZKXd'

    def tool_usage(self) -> str:
        return '''GoogleMapsDirection: Gets transit directions between two locations using Google Maps.
        Usage: <<<GoogleMapsDirection(source="starting address", destination="ending address")>>>,
        Returns a list of possible routes with transit information.'''

    def tool_usage_xml(self) -> str:
        return '''GoogleMapsDirection: Gets transit directions between two locations using Google Maps.
    <command name="GoogleMapsDirection">
        <arg name="source">starting address of the route</arg>
        <arg name="destination">ending address of the route</arg>
    </command>
    Returns a list of possible routes with transit information including duration, departure/arrival times, and transit steps.'''

    async def _wait_for_routes(self, timeout: int = 10) -> bool:
        """Wait for routes to load"""
        try:
            await self.page.wait_for_selector(self.route_item_selector, timeout=timeout * 1000)
            return True
        except Exception as e:
            print(f"Error waiting for routes: {str(e)}")
            return False

    async def _get_route_elements(self) -> List:
        """Get all route elements"""
        try:
            return await self.page.query_selector_all(self.route_item_selector)
        except Exception as e:
            print(f"Error getting route elements: {str(e)}")
            return []

    async def _parse_transit_step(self, step_element) -> TransitStep:
        """Parse a single transit step from the route"""
        try:
            mode_element = await step_element.query_selector('.mTOalf img')
            mode_alt = await mode_element.get_attribute('alt') if mode_element else None
            mode = mode_alt.upper() if mode_alt else "UNKNOWN"

            line_element = await step_element.query_selector('.Bzv5Cd .cukLmd')
            line = await line_element.inner_text() if line_element else None

            color_element = await step_element.query_selector('.Bzv5Cd')
            style = await color_element.get_attribute('style') if color_element else None
            color = style.split('background-color: ')[1].split(';')[0] if style and 'background-color' in style else None

            return TransitStep(
                mode=mode,
                line=line,
                line_color=color
            )
        except Exception as e:
            print(f"Error parsing transit step: {str(e)}")
            return TransitStep(mode="UNKNOWN")

    async def _parse_route(self, route_element, selected: bool = False) -> Optional[Route]:
        """Parse a single route from the results"""
        try:
            # Parse duration
            duration_text = await route_element.query_selector('.Fk3sm')
            duration_str = await duration_text.inner_text() if duration_text else "0 min"
            duration_minutes = int(''.join(filter(str.isdigit, duration_str)))

            # Parse times
            time_range = await route_element.query_selector('.VuCHmb span')
            time_text = await time_range.inner_text() if time_range else ""
            times = time_text.split('—')
            departure_time = datetime.strptime(times[0].strip(), '%I:%M %p')
            arrival_time = datetime.strptime(times[1].strip(), '%I:%M %p')

            # Parse transit steps
            steps_container = await route_element.query_selector('.CMnFh')
            step_elements = await steps_container.query_selector_all('.mTOalf')
            steps = []
            
            for step_element in step_elements:
                step = await self._parse_transit_step(step_element)
                if step and step.mode != "UNKNOWN":  # Only add valid steps
                    steps.append(step)

            # Check if this route is selected
            selected_class = await route_element.get_attribute('class')
            is_selected = 'selected' in (selected_class or '')

            return Route(
                total_duration_minutes=duration_minutes,
                departure_time=departure_time,
                arrival_time=arrival_time,
                steps=steps,
                selected=is_selected
            )
        except Exception as e:
            print(f"Error parsing route: {str(e)}")
            return None

    async def _save_routes_screenshot(self, route_index: int = None) -> str:
        """Save a screenshot of the routes panel"""
        try:
            # Find the main directions div
            directions_div = await self.page.query_selector('div[role="main"][aria-label="Directions"]')
            if not directions_div:
                print("Could not find directions panel")
                return None

            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"routes_screenshot_{timestamp}.png"
            
            # Take screenshot with optimal settings for quality
            # Take screenshot with optimal settings for quality
            await directions_div.screenshot(
                path=filename,
                type='png',
                scale='device',
                animations='disabled',
                caret='hide'
            )
            print(f"Screenshot saved as {filename}")
            return filename
        except Exception as e:
            print(f"Error taking screenshot: {str(e)}")
            return None

    async def _execute(self, **kwargs) -> List[Route]:
        """Execute the Google Maps direction search"""
        source = kwargs.get('source')
        destination = kwargs.get('destination')
        
        if not source or not destination:
            raise ValueError("Both 'source' and 'destination' must be specified")

        await self.initialize()
        routes = []

        try:
            # Navigate to Google Maps
            await self.page.goto('https://www.google.de/maps/preview', wait_until='load', timeout=0)
            
            # Click directions button
            await self.page.click(self.directions_button_selector)
            await asyncio.sleep(1)

            # Enter source and destination
            source_input = self.page.locator(self.source_input_selector)
            await source_input.fill(source)
            await asyncio.sleep(0.5)

            destination_input = self.page.locator(self.destination_input_selector)
            await destination_input.fill(destination)
            await asyncio.sleep(0.5)
            
            await self.page.keyboard.press('Enter')

            # Wait for routes to load
            if not await self._wait_for_routes():
                print("No routes found within timeout period")
                return []

            # Take screenshot of routes
            screenshot_path = await self._save_routes_screenshot()

            # Get all route elements
            route_elements = await self._get_route_elements()
            
            # Parse each route
            for i, route_element in enumerate(route_elements):
                route = await self._parse_route(route_element, i == 0)
                if route:
                    routes.append(route)

            return routes

        except Exception as e:
            print(f"Error executing Google Maps direction search: {str(e)}")
            return []
            
        finally:
            await self.close()
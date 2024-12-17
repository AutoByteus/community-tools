from autobyteus.tools.base_tool import BaseTool
from .google_slides_presentation import GoogleSlidesPresentation

class GoogleSlidesCreator(BaseTool):
    """Main tool class for creating and modifying Google Slides presentations."""

    def __init__(self):
        super().__init__()
        self.presentation = GoogleSlidesPresentation()

    def tool_name(self) -> str:
        return "GoogleSlidesCreator"

    def tool_description(self) -> str:
        return (
            "A tool for creating and modifying Google Slides presentations. "
            "This tool allows you to create new presentations with multiple slides "
            "and add slides to existing presentations."
        )

    def tool_usage(self) -> str:
        usage = (
            "GoogleSlidesCreator: Create and modify Google Slides presentations.\n"
            "Usage:\n"
            "1. Create a complete presentation:\n"
            "   <<<GoogleSlidesCreator(action=\"create_complete_presentation\", title=\"Presentation Title\", slides_data=[{'layout': 'TITLE', 'title': 'Slide 1 Title', 'content': 'Slide 1 Content'}, {'layout': 'TITLE_AND_BODY', 'title': 'Slide 2 Title', 'content': 'Slide 2 Content'}])>>>\n\n"
            "2. Add a slide to an existing presentation:\n"
            "   <<<GoogleSlidesCreator(action=\"add_slide_to_presentation\", presentation_id=\"your_presentation_id\", slide_data={'layout': 'TITLE_AND_BODY', 'title': 'New Slide Title', 'content': 'New Slide Content'})>>>\n"
        )
        return usage

    def tool_usage_xml(self) -> str:
        usage_xml = '''GoogleSlidesCreator: Create and modify Google Slides presentations. This tool allows you to create new presentations with multiple slides and add slides to existing presentations. Usage:
        <command name="GoogleSlidesCreator">
            <arg name="action">Action to perform: "create_complete_presentation" or "add_slide_to_presentation"</arg>
            <arg name="title">Title of the presentation (for create_complete_presentation)</arg>
            <arg name="slides_data">List of dictionaries containing slide data (for create_complete_presentation)</arg>
            <arg name="presentation_id">ID of the existing presentation (for add_slide_to_presentation)</arg>
            <arg name="slide_data">Dictionary containing slide data (for add_slide_to_presentation)</arg>
        </command>
        where "action" specifies the operation to perform, "title" is the presentation title (for create_complete_presentation), "slides_data" is a list of slide information (for create_complete_presentation), "presentation_id" is the ID of an existing presentation (for add_slide_to_presentation), and "slide_data" is the information for a new slide (for add_slide_to_presentation).

        Examples:
        1. Create a new presentation with two slides:
        <command name="GoogleSlidesCreator">
            <arg name="action">create_complete_presentation</arg>
            <arg name="title">My Awesome Presentation</arg>
            <arg name="slides_data">
                [
                    {"layout": "TITLE", "title": "Welcome to My Presentation", "content": "By John Doe"},
                    {"layout": "TITLE_AND_BODY", "title": "Key Points", "content": "• Point 1\\n• Point 2\\n• Point 3"}
                ]
            </arg>
        </command>

        2. Add a new slide to an existing presentation:
        <command name="GoogleSlidesCreator">
            <arg name="action">add_slide_to_presentation</arg>
            <arg name="presentation_id">1234567890abcdefghijklmnopqrstuvwxyz</arg>
            <arg name="slide_data">
                {"layout": "TITLE_AND_BODY", "title": "Conclusion", "content": "Thank you for your attention!"}
            </arg>
        </command>

        3. INCORRECT EXAMPLE - DO NOT USE:
        <command name="GoogleSlidesCreator">
            <arg name="action">unknown_action</arg>
            <arg name="title">My Presentation</arg>
        </command>
        THIS IS ABSOLUTELY WRONG! The action "unknown_action" is not supported. 
        Always use either "create_complete_presentation" or "add_slide_to_presentation" as the action.
        '''
        return usage_xml

    async def _execute(self, **kwargs) -> str:
        action = kwargs.get('action')
        if action == 'create_complete_presentation':
            return self.create_complete_presentation(kwargs.get('title'), kwargs.get('slides_data'))
        elif action == 'add_slide_to_presentation':
            return self.add_slide_to_presentation(kwargs.get('presentation_id'), kwargs.get('slide_data'))
        else:
            raise ValueError(f"Unknown action: {action}")

    def create_complete_presentation(self, title, slides_data):
        try:
            presentation_id = self.presentation.create_presentation(title)
            
            for slide_data in slides_data:
                slide_id = self.presentation.add_slide(slide_data['layout'])
                self.presentation.add_text_to_slide(slide_id, slide_data['title'], slide_data['content'])

            return f"Created presentation with ID: {presentation_id}"
        except Exception as e:
            return f"Failed to create complete presentation: {str(e)}"
    
    def add_slide_to_presentation(self, presentation_id, slide_data):
        """
        Add a specific slide to an existing presentation.
        
        :param presentation_id: ID of the existing presentation
        :param slide_data: Dictionary containing slide data
                           {'layout': 'TITLE_AND_BODY', 'title': 'Slide Title', 'content': 'Slide Content'}
        """
        try:
            self.presentation.open_presentation(presentation_id)
            self.presentation.add_slide(slide_data['layout'])
            # Add title and content to the slide
            # Note: In a real implementation, you'd need to get the slide ID and text box IDs
            # self.presentation.add_text_to_slide(slide_id, slide_data['title'], title_box_id)
            # self.presentation.add_text_to_slide(slide_id, slide_data['content'], content_box_id)
            return f"Added new slide to presentation {presentation_id}"
        except Exception as e:
            return f"Failed to add slide to presentation: {str(e)}"
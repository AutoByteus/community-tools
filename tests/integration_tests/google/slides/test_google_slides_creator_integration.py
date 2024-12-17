import os
import pytest

from autobyteus_community_tools.google.slides.google_slides_creator import GoogleSlidesCreator

@pytest.mark.asyncio
async def test_create_personal_agents_presentation():
    creator = GoogleSlidesCreator()
    
    title = "Building Your Personal Agents with Our Framework and Large Language Model"
    slides_data = [
        {
            "layout": "TITLE",
            "title": title,
            "content": "Presented by Your Company Name"
        },
        {
            "layout": "TITLE_AND_BODY",
            "title": "I. Introduction",
            "content": "• Goal: Demonstrate the power of personal agents\n• Thesis: In the future, everyone will have their own personal agents"
        },
        {
            "layout": "TITLE_AND_BODY",
            "title": "II. Demo: Three Personal Agents",
            "content": "1. Xiaohongshu poster\n2. Weibo poster\n3. General Q&A agent"
        },
        {
            "layout": "TITLE_AND_BODY",
            "title": "III. Under the Hood: Prompts and Large Language Models",
            "content": "• Explain prompts used in the demo\n• Validate performance of open-source models\n• Discuss prompt optimization"
        },
        {
            "layout": "TITLE_AND_BODY",
            "title": "IV. Building Your Own Personal Agents",
            "content": "• Introduce our UI provider and framework\n• Explain ease of building and deploying agents\n• Highlight benefits of our framework"
        },
        {
            "layout": "TITLE_AND_BODY",
            "title": "V. Join Our Agent Course",
            "content": "• Announce our agent course\n• Outline benefits:\n  - Access to private library\n  - Training on prompt optimization\n  - Support for building agents"
        },
        {
            "layout": "TITLE_AND_BODY",
            "title": "VI. Conclusion",
            "content": "• Recap key takeaways\n• Emphasize importance of personal agents\n• Call to action: Start building your own agents!"
        }
    ]

    result = await creator.execute(action="create_complete_presentation", title=title, slides_data=slides_data)

    #assert "Created presentation with ID:" in result, "Failed to create the presentation"
    
    # Extract the presentation ID from the result
    presentation_id = result.split("ID: ")[1]

    # Test adding a new slide to the existing presentation
    new_slide_data = {
        "layout": "TITLE_AND_BODY",
        "title": "Thank You!",
        "content": "Any questions?"
    }

    add_slide_result = await creator.execute(action="add_slide_to_presentation", presentation_id=presentation_id, slide_data=new_slide_data)

    #assert f"Added new slide to presentation {presentation_id}" in add_slide_result, "Failed to add new slide to the presentation"

    print(f"Integration test completed successfully. Presentation ID: {presentation_id}")

@pytest.mark.asyncio
async def test_create_single_slide_presentation():
    creator = GoogleSlidesCreator()
    
    title = "Single Slide Test Presentation"
    slides_data = [
        {
            "layout": "TITLE_AND_BODY",
            "title": "Test Slide",
            "content": "This is a test slide content."
        }
    ]

    result = await creator._execute(action="create_complete_presentation", title=title, slides_data=slides_data)

    assert "Created presentation with ID:" in result, "Failed to create the presentation"
    
    # Extract the presentation ID from the result
    presentation_id = result.split("ID: ")[1]

    # Fetch the created presentation to verify its contents
    presentation = creator.presentation.service.presentations().get(presentationId=presentation_id).execute()
    
    # Verify the number of slides
    assert len(presentation.get('slides', [])) == 1, "Presentation should have exactly one slide"

    # Verify the content of the slide
    slide = presentation['slides'][0]
    title_shape = next((element for element in slide['pageElements'] if element['shape']['shapeType'] == 'TEXT_BOX'), None)
    body_shape = next((element for element in slide['pageElements'] if element['shape']['shapeType'] == 'TEXT_BOX' and element != title_shape), None)

    assert title_shape is not None, "Title shape not found in the slide"
    assert body_shape is not None, "Body shape not found in the slide"

    title_content = title_shape['shape']['text']['textElements'][1]['textRun']['content'].strip()
    body_content = body_shape['shape']['text']['textElements'][1]['textRun']['content'].strip()

    assert title_content == "Test Slide", f"Unexpected title content: {title_content}"
    assert body_content == "This is a test slide content.", f"Unexpected body content: {body_content}"

    print(f"Integration test completed successfully. Presentation ID: {presentation_id}")

    # Clean up: Delete the created presentation
    creator.presentation.service.presentations().delete(presentationId=presentation_id).execute()
    print(f"Deleted test presentation with ID: {presentation_id}")
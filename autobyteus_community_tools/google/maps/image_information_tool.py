import asyncio
import logging
from typing import List, Optional
from autobyteus.agent.agent import StandaloneAgent
from autobyteus.conversation.user_message import UserMessage
from autobyteus.llm.llm_factory import LLMFactory
from autobyteus.prompt.prompt_builder import PromptBuilder
from autobyteus.events.event_types import EventType

logger = logging.getLogger(__name__)

class ImageInformationTool:
    name: str = "image_information_tool"

    def __init__(self, prompt_dir: str):
        self.prompt_file = f"{prompt_dir}/{self.name}.txt"
        self.agent: Optional[StandaloneAgent] = None
        self.response_queue = asyncio.Queue()

    def get_name(self) -> str:
        return self.name

    async def _on_assistant_response(self, *args, **kwargs):
        """Handles the assistant's response."""
        response = kwargs.get('response')
        if response:
            await self.response_queue.put(response)

    def get_prompt(self) -> str:
        try:
            return PromptBuilder.from_file(self.prompt_file).build()
        except Exception as e:
            logger.error(f"Failed to load prompt template: {str(e)}")
            return "Please analyze the provided image."

    async def execute(
        self, 
        image_path: str, 
        llm_model: str
    ) -> str:
        """
        Executes the tool to extract information from an image.
        
        Args:
            image_path: Path to the image file
            llm_model: LLM model identifier
        
        Returns:
            str: Analysis results or error message
        """
        logger.info(f"Executing image_information_tool with image_path: {image_path}")
        
        try:
            llm_instance = LLMFactory.create_llm(llm_model)
            initial_prompt = self.get_prompt()
            initial_user_message = UserMessage(content=initial_prompt, file_paths=[image_path])

            self.agent = StandaloneAgent(
                role="image_analyzer",
                llm=llm_instance,
                tools=[],
                initial_user_message=initial_user_message,
                agent_id="image_analyzer"
            )
            self.agent.subscribe(EventType.ASSISTANT_RESPONSE, self._on_assistant_response, self.agent.agent_id)
            self.agent.start()

            try:
                final_response = await asyncio.wait_for(
                    self.response_queue.get(),
                    timeout=30.0
                )
                return final_response
            except asyncio.TimeoutError:
                logger.error("Timeout waiting for image analysis response")
                return "Error: Analysis timeout occurred"
            finally:
                await self.cleanup()

        except Exception as e:
            error_message = f"Error during image analysis: {str(e)}"
            logger.error(error_message, exc_info=True)
            return error_message

    async def cleanup(self):
        """Clean up resources."""
        try:
            if self.agent:
                self.agent.unsubscribe(EventType.ASSISTANT_RESPONSE, self._on_assistant_response, self.agent.agent_id)
                self.agent.stop()
                await self.agent.cleanup()
                self.agent = None
                
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}", exc_info=True)
            raise
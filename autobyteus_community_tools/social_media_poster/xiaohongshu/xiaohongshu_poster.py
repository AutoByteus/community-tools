import asyncio
import pyperclip
import sys
import platform
import subprocess
import pyautogui
from autobyteus.tools.base_tool import BaseTool
from llm_ui_integration.ui_integrator import UIIntegrator
from bson import ObjectId
from datetime import datetime
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from autobyteus_community_tools.social_media_poster.xiaohongshu.repositories.book_review_repository import ReviewedBooksRepository, XiaohongshuBookReviewModel

class XiaohongshuPoster(BaseTool, UIIntegrator):
    def __init__(self, xiaohongshu_account_name):
        BaseTool.__init__(self)
        UIIntegrator.__init__(self)
        
        self.post_creation_url = 'https://creator.xiaohongshu.com/publish/publish?source=official'
        self.image_text_tab_selector = 'div.tab:not(.active) span.title'
        self.title_input_selector = '.input.titleInput input'
        self.content_input_selector = '#post-textarea'
        self.publish_button_selector = '.publishBtn'
        self.uploading_indicator = '.img-container .mask.uploading'
        self.file_input_selector = 'input.upload-input[type="file"][accept=".jpg,.jpeg,.png,.webp"]'
        self.xiaohongshu_account_name = xiaohongshu_account_name

    def tool_usage(self) -> str:
        usage = (
            "XiaohongshuPoster: Publishes a book review on Xiaohongshu (小红书). "
            "This tool allows you to create engaging book review posts with both original title (in any language) and Chinese translated title. "
            "Note: The translated_title must be within 20 words and will be used as the post title. The image_path is optional.\n"
            "Usage: <<<XiaohongshuPoster(original_title=\"Original Title\", translated_title=\"中文标题 (20 words max)\", content=\"Book review content in Chinese\", image_path=\"/full/path/to/image.jpg\")>>>\n\n"
            "Examples:\n"
            "1. English book with image:\n"
            "<<<XiaohongshuPoster(\n"
            "    original_title=\"To Live\",\n"
            "    translated_title=\"活着\",\n"
            "    content=\"余华的《活着》是一部震撼人心的小说，讲述了一个普通中国家庭在动荡年代的生存故事。...\",\n"
            "    image_path=\"/home/user/Downloads/to_live_cover.jpg\"\n"
            ")>>>\n\n"
            "2. French book without image:\n"
            "<<<XiaohongshuPoster(\n"
            "    original_title=\"Le Petit Prince\",\n"
            "    translated_title=\"小王子\",\n"
            "    content=\"《小王子》是一部充满哲理的童话故事，讲述了一个来自外星球的小王子的奇妙冒险...\"\n"
            ")>>>\n\n"
            "3. INCORRECT EXAMPLE - DO NOT USE:\n"
            "<<<XiaohongshuPoster(\n"
            "    original_title=\"The Catcher in the Rye\",\n"
            "    translated_title=\"麦田里的守望者：一部探讨青春期叛逆与成长的经典小说，深刻剖析了现代社会中年轻人的困惑与迷茫\",\n"
            "    content=\"...\"\n"
            ")>>>\n"
            "THIS IS ABSOLUTELY WRONG! The translated_title is way over the 20-word limit. "
            "Such long titles are strictly prohibited and will cause the post to fail. "
            "Always keep your translated titles concise and within the 20-word limit!"
        )
        return usage

    def tool_usage_xml(self) -> str:
        usage = '''XiaohongshuPoster: Publishes a book review on Xiaohongshu (小红书). This tool creates engaging book review posts with both original title (in any language) and Chinese translated title. Note: The translated_title must be within 20 words and will be used as the post title. The image_path is optional. Usage:
        <command name="XiaohongshuPoster">
            <arg name="original_title">Original Title (in any language)</arg>
            <arg name="translated_title">中文标题 (20 words max)</arg>
            <arg name="content">Book review content in Chinese</arg>
            <arg name="image_path" optional="true">Full path to cover image file</arg>
        </command>
        where "original_title" is the book's title in its original language, "translated_title" is the Chinese translation of the title (max 20 words) and will be used as the post title, "content" is the main text of the review in Chinese, and "image_path" is the optional full path to the cover image file.

        Examples:
        1. English book with image:
        <command name="XiaohongshuPoster">
            <arg name="original_title">To Live</arg>
            <arg name="translated_title">活着</arg>
            <arg name="content">余华的《活着》是一部震撼人心的小说，讲述了一个普通中国家庭在动荡年代的生存故事。...</arg>
            <arg name="image_path">/home/user/Downloads/to_live_cover.jpg</arg>
        </command>

        2. French book without image:
        <command name="XiaohongshuPoster">
            <arg name="original_title">Le Petit Prince</arg>
            <arg name="translated_title">小王子</arg>
            <arg name="content">《小王子》是一部充满哲理的童话故事，讲述了一个来自外星球的小王子的奇妙冒险...</arg>
        </command>

        3. INCORRECT EXAMPLE - DO NOT USE:
        <command name="XiaohongshuPoster">
            <arg name="original_title">The Catcher in the Rye</arg>
            <arg name="translated_title">麦田里的守望者：一部探讨青春期叛逆与成长的经典小说，深刻剖析了现代社会中年轻人的困惑与迷茫</arg>
            <arg name="content">...</arg>
        </command>
        THIS IS ABSOLUTELY WRONG! The translated_title is way over the 20-word limit. 
        Such long titles are strictly prohibited and will cause the post to fail. 
        Always keep your translated titles concise and within the 20-word limit!
        '''
        return usage

    async def _execute(self, **kwargs) -> str:
        original_title = kwargs.get('original_title')
        translated_title = kwargs.get('translated_title')
        content = kwargs.get('content')
        image_path = kwargs.get('image_path')

        if not original_title or not translated_title or not content:
            raise ValueError("'original_title', 'translated_title', and 'content' are required for the book review.")

        if len(translated_title.split()) > 20:
            raise ValueError("The translated_title must be within 20 words.")

        book_review = XiaohongshuBookReviewModel(
            review_id=ObjectId(),
            original_title=original_title,
            title=translated_title,
            content=content,
            timestamp=datetime.utcnow()
        )

        await self.initialize()

        try:
            await self.page.goto(self.post_creation_url)
            await self.page.wait_for_load_state('networkidle')

            image_text_tab = self.page.locator(self.image_text_tab_selector)
            await image_text_tab.click()

            image_uploaded = False
            if image_path:
                await self.click_upload_button()
                await self.select_file(image_path)
                image_uploaded = True

            await self.wait_for_image_upload(image_uploaded)
            await asyncio.sleep(1)

            await self._copy_paste_text(self.title_input_selector, book_review.title)
            await self._copy_paste_text(self.content_input_selector, book_review.content)

            publish_button = self.page.locator(self.publish_button_selector)
            await publish_button.click()

            await self.wait_for_post_submission()

            book_review_repository = ReviewedBooksRepository()
            book_review_repository.create(book_review)

            return f"Book review '{book_review.title}' published successfully on Xiaohongshu!"
        except PlaywrightTimeoutError as e:
            return f"Timeout error while creating the book review post on Xiaohongshu: {str(e)}"
        except Exception as e:
            return f"An error occurred while creating the book review post on Xiaohongshu: {str(e)}"
        finally:
            await asyncio.sleep(3)
            await self.close()

    async def click_upload_button(self):
        try:
            upload_button = self.page.locator(self.file_input_selector)
            await upload_button.click()
            await asyncio.sleep(1)  # Wait for the file dialog to open
        except PlaywrightTimeoutError as e:
            raise Exception(f"Timeout error clicking upload button: {str(e)}")
        except Exception as e:
            raise Exception(f"Error clicking upload button: {str(e)}")

    async def select_file(self, image_path):
        os_name = platform.system().lower()
        if os_name == 'darwin':
            return await self.select_file_mac(image_path)
        elif os_name in ['linux', 'windows']:
            return await self.select_file_pyautogui(image_path, os_name)
        else:
            raise Exception(f"Unsupported operating system: {os_name}")

    async def select_file_mac(self, image_path):
        script = f'''
        tell application "System Events"
            tell process "Google Chrome"
                set frontmost to true
                delay 1
                keystroke "g" using {{command down, shift down}}
                delay 1
                keystroke "{image_path}"
                delay 1
                keystroke return
            end tell
        end tell
        '''
        try:
            subprocess.run(['osascript', '-e', script], check=True, capture_output=True, text=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error executing AppleScript: {e}")
            print(f"Script output: {e.output}")
            return False

    async def select_file_pyautogui(self, image_path, os_name):
        try:
            if os_name == 'linux':
                pyautogui.hotkey('ctrl', 'l')
            elif os_name == 'windows':
                pyautogui.hotkey('alt', 'd')
            
            await asyncio.sleep(0.5)
            
            pyautogui.write(image_path)
            pyautogui.press('enter')
            return True
        except Exception as e:
            print(f"Error using PyAutoGUI: {e}")
            return False

    async def wait_for_image_upload(self, image_uploaded: bool):
        if image_uploaded:
            try:
                uploading_indicator = self.page.locator(self.uploading_indicator)
                await uploading_indicator.wait_for(state='attached', timeout=30000)
                await uploading_indicator.wait_for(state='detached', timeout=60000)
                await asyncio.sleep(1)
                print("Image upload completed successfully.")
            except PlaywrightTimeoutError as e:
                raise Exception(f"Timeout error while waiting for image upload: {str(e)}")
            except Exception as e:
                raise Exception(f"Error while waiting for image upload: {str(e)}")
        else:
            max_wait_time = 300  # 5 minutes
            poll_interval = 5  # 5 seconds
            elapsed_time = 0

            while elapsed_time < max_wait_time:
                if await self.is_post_ready():
                    print("Post is ready for submission.")
                    return
                await asyncio.sleep(poll_interval)
                elapsed_time += poll_interval

            raise Exception("Timed out waiting for post to be ready for submission.")

    async def is_post_ready(self):
        try:
            publish_button = self.page.locator(self.publish_button_selector)
            return await publish_button.is_enabled()
        except Exception:
            return False

    async def wait_for_post_submission(self):
        try:
            success_container = self.page.locator('.success-container')
            await success_container.wait_for(state='visible', timeout=30000)
            
            success_title = success_container.locator('.content .title')
            success_text = await success_title.inner_text()
            
            if success_text.strip() == "发布成功":
                print("Post published successfully on Xiaohongshu!")
            else:
                raise Exception("Unexpected content in success message")
        except PlaywrightTimeoutError as e:
            raise Exception(f"Timeout error while waiting for post submission: {str(e)}")
        except Exception as e:
            raise Exception(f"Error while waiting for post submission: {str(e)}")

    async def _copy_paste_text(self, selector: str, text: str) -> None:
        pyperclip.copy(text)
        input_element = self.page.locator(selector)
        await input_element.focus()
        
        paste_shortcut = "Meta+V" if sys.platform == "darwin" else "Control+V"
        await self.page.keyboard.press(paste_shortcut)
        await asyncio.sleep(0.5)
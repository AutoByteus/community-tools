import asyncio

from autobyteus_community_tools.social_media_poster.xiaohongshu.xiaohongshu_poster import XiaohongshuPoster

async def main():
    xiaohongshu_poster = XiaohongshuPoster(xiaohongshu_account_name="TestAccount")

    # Content to be posted
    original_title = "The Great Gatsby"
    translated_title = "了不起的盖茨比"
    content = """
    《了不起的盖茨比》是一部经典的美国小说，作者是F. 斯科特·菲茨杰拉德。这本书通过描绘1920年代的美国社会，深刻揭示了"美国梦"的本质。
    故事围绕着神秘的百万富翁杰伊·盖茨比展开，他的奢华生活和神秘过去引人入胜。盖茨比对黛西·布坎南的执着追求，反映了他对理想生活的渴望。
    然而，小说最终揭示了这种理想的虚幻和空洞，通过盖茨比的悲剧命运，菲茨杰拉德批判了社会的腐败和道德的沦丧。
    这本书不仅是对那个时代的真实写照，更是对人性和社会的深刻反思。无论是语言的优美还是情节的紧凑，都让人难以忘怀。
    """
    image_filename = "testimaging.webp"

    try:
        result = await xiaohongshu_poster.execute(
            original_title=original_title,
            translated_title=translated_title,
            content=content,
            image_filename=image_filename
        )
        print(result)
        if "published successfully on Xiaohongshu" in result:
            print("Post was successful!")
        else:
            print("Post may have failed. Please check the result.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
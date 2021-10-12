import logging
import pyrogram
from config import Config


# Setting up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.INFO)

chotu = pyrogram.Client(
    "chotu",
    bot_token=Config.TOKEN,
    api_id=Config.ID,
    api_hash=Config.HASH,
    plugins=dict(root="cogs")
)

chotu.run()
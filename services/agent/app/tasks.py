import os
from enum import Enum

from dotenv import load_dotenv
from pyyoutube import Api
from sqlalchemy.orm import Session

from . import crud
from .schemas import TrimmedItem, VideoCreate

load_dotenv()


api = Api(api_key=os.environ.get("YOUTUBE_API_KEY"))


class ProcessedStatus(Enum):
    PROCESSED = True
    NOT_PROCESSED = False
    NOT_FOUND = True


def process_playlist(playlist: str, db: Session):
    processed = ProcessedStatus.NOT_PROCESSED
    playlist_db_id = crud.get_playlist_id_by_list(db, playlist)
    if playlist_db_id != 0:
        result = crud.get_item(db, playlist_db_id)
        processed = result.processed if result else ProcessedStatus.NOT_FOUND

    if not processed:
        try:
            resp = api.get_playlist_items(playlist_id=playlist, count=None)
        except Exception as e:
            print(e)
        else:
            for item in resp.items:
                title = str(item.snippet.title).strip()
                description = str(item.snippet.description).strip()
                video_id = item.snippet.resourceId.videoId
                status = item.status.privacyStatus
                video_by_id = api.get_video_by_id(video_id=video_id)
                views_count = video_by_id.items[0].statistics.viewCount
                likes_count = video_by_id.items[0].statistics.likeCount
                dislikes_count = video_by_id.items[0].statistics.dislikeCount
                comments_count = video_by_id.items[0].statistics.commentCount

                video = VideoCreate(
                    youtube_id=video_id,
                    list_id=playlist_db_id,
                    title=title,
                    description=description,
                    privacy_status=status,
                    view_count=0 if views_count is None else int(views_count),
                    like_count=0 if likes_count is None else int(likes_count),
                    dislike_count=0 if dislikes_count is None else int(dislikes_count),
                    comment_count=0 if comments_count is None else int(comments_count),
                )
                crud.create_video(db, video)
            crud.process_item(db, TrimmedItem(list=playlist))

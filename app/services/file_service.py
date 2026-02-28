"""File upload: store metadata and return url."""
import os
import uuid as uuid_lib
from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from app.db.models.file import File


def _file_resource(f: File) -> Dict[str, Any]:
    return {"uuid": f.uuid, "filename": f.filename, "url": f.url, "created_at": f.created_at}


class FileService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: int, filename: str, content: bytes = b"", path: Optional[str] = None) -> Optional[Dict[str, Any]]:
        try:
            upload_dir = os.environ.get("UPLOAD_DIR", "uploads")
            os.makedirs(upload_dir, exist_ok=True)
            ext = os.path.splitext(filename)[1] or ".bin"
            safe_name = f"{uuid_lib.uuid4().hex}{ext}"
            file_path = os.path.join(upload_dir, safe_name)
            if content:
                with open(file_path, "wb") as fp:
                    fp.write(content)
            url = path or f"/uploads/{safe_name}"
            f = File(uuid=str(uuid_lib.uuid4()), user_id=user_id, path=file_path, filename=filename, url=url, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
            self.db.add(f)
            self.db.commit()
            self.db.refresh(f)
            return _file_resource(f)
        except Exception:
            return None

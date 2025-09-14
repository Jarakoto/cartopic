import mimetypes
import os
import uuid
from typing import Tuple
import requests
from django.conf import settings

class OwnCloudError(Exception):
    pass

def _check_config():
    required = [settings.OWNCLOUD_BASE_URL, settings.OWNCLOUD_USERNAME, settings.OWNCLOUD_PASSWORD]
    if not all(required):
        raise OwnCloudError("OwnCloud settings incomplete. Set OWNCLOUD_BASE_URL, OWNCLOUD_USERNAME, OWNCLOUD_PASSWORD.")


def upload_file(file_bytes: bytes, original_name: str) -> Tuple[str, str]:
    """Upload a file to ownCloud/Nextcloud and return a tuple of (share_page_url, direct_download_url).

    share_page_url: Standard public share page (e.g. https://cloud.example.com/s/<token>)
    direct_download_url: A URL intended for direct file download (share_page_url + '/download').
    If share creation or parsing fails, both values may fall back to the WebDAV URL (non-public).
    """
    _check_config()
    base = settings.OWNCLOUD_BASE_URL
    webdav_url = f"{base}/remote.php/dav/files/{settings.OWNCLOUD_USERNAME}"
    # Ensure path
    remote_dir = settings.OWNCLOUD_UPLOAD_ROOT.strip('/')
    # Generate unique filename preserving extension
    ext = os.path.splitext(original_name)[1]
    remote_name = f"{uuid.uuid4().hex}{ext}"
    remote_path = f"{remote_dir}/{remote_name}" if remote_dir else remote_name

    # Create intermediate directories is optional; Nextcloud auto-creates only final? We can try MKCOL for each segment.
    session = requests.Session()
    session.auth = (settings.OWNCLOUD_USERNAME, settings.OWNCLOUD_PASSWORD)

    # Ensure directory path exists
    if remote_dir:
        segments = remote_dir.split('/')
        current = ''
        for seg in segments:
            current = f"{current}/{seg}" if current else seg
            mkcol_url = f"{webdav_url}/{current}"
            resp = session.request('MKCOL', mkcol_url)
            if resp.status_code in (201, 405):  # 201 Created, 405 Already exists
                pass
            elif resp.status_code == 409:
                # parent missing - continue attempts
                continue
            else:
                # Some servers return 207 multi-status; ignore success patterns
                if resp.status_code not in (200, 207):
                    raise OwnCloudError(f"Failed to ensure directory {current}: {resp.status_code} {resp.text}")

    mime_type, _ = mimetypes.guess_type(original_name)
    headers = {}
    if mime_type:
        headers['Content-Type'] = mime_type

    put_url = f"{webdav_url}/{remote_path}"
    put_resp = session.put(put_url, data=file_bytes, headers=headers)
    if put_resp.status_code not in (200,201,204):
        raise OwnCloudError(f"Upload failed: {put_resp.status_code} {put_resp.text}")

    # Create share via OCS API
    share_api = f"{base}/ocs/v2.php/apps/files_sharing/api/v1/shares"
    data = {
        'path': f"/{remote_path}",
        'shareType': 3 if settings.OWNCLOUD_SHARE_PUBLIC else 0,  # 3 public link
        'permissions': settings.OWNCLOUD_SHARE_PERMISSIONS,
    }
    headers = { 'OCS-APIRequest': 'true' }
    share_resp = session.post(share_api, data=data, headers=headers)
    if share_resp.status_code not in (200,201):
        # fallback – no share created
        return (put_url, put_url)

    share_page_url: str | None = None
    token: str | None = None
    # Try proper XML parsing
    try:
        import xml.etree.ElementTree as ET
        root = ET.fromstring(share_resp.text)
        # Nextcloud wraps in <ocs><data><element>...</element></data></ocs>
        for elem in root.iter():
            tag = elem.tag.lower()
            if tag.endswith('url') and elem.text and not share_page_url:
                share_page_url = elem.text.strip()
            if tag.endswith('token') and elem.text and not token:
                token = elem.text.strip()
    except Exception:
        # Fallback to naive extraction
        if 'url' in share_resp.text:
            start = share_resp.text.find('<url>')
            end = share_resp.text.find('</url>')
            if start != -1 and end != -1:
                share_page_url = share_resp.text[start+5:end].strip()

    if not share_page_url:
        # Could not parse – return WebDAV path
        return (put_url, put_url)

    direct_download = share_page_url.rstrip('/') + '/download'
    return (share_page_url, direct_download)

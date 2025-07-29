# File Upload
**ALWAYS create database table for file storage**

1. **Endpoint**: `POST https://database.altan.ai/storage/v1/upload`
2. **Header**: `apikey: <supabaseKey>`
3. **Payload**:
```json
{
  "file_content": "[base64_encoded]",
  "mime_type": "image/jpeg",
  "file_name": "filename.ext"
}
```
4. **Store**: Save `media_url` from response to database
5. **Retrieve**: GET request to stored `media_url` for file/preview

## Media Instructions
Guide users: Click "+" icon → "Add Media" → submit (NEVER recommend attachments)
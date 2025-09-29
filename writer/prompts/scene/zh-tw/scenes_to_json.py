SCENES_TO_JSON = '''# CONTEXT
我需要將以下的場景-by-場景大綱轉換為JSON格式的列表。
```
{_Scenes}
```
---

# OBJECTIVE
為提供的大綱生成JSON列表，其中每個元素包含對應場景的內容。
範例：
[
    "scene 1 content...",
    "scene 2 content...",
    "etc."
]
請勿包含其他JSON字段，僅需是一個字串列表。
---

# STYLE
以純JSON格式回應。
---

# AUDIENCE
請確保回應純為JSON格式。
---

# RESPONSE
請勿遺失原始大綱中的任何資訊，僅需格式化為列表。
---
'''
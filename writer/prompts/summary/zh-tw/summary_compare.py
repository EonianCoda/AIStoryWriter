SUMMARY_COMPARE = '''請比較提供的章節摘要和關聯大綱，並指示提供的內容是否大致遵循大綱。

<CHAPTER_SUMMARY>
{WorkSummary}
</CHAPTER_SUMMARY>

<OUTLINE>
{OutlineSummary}
</OUTLINE>

請以無其他內容的JSON格式編寫回應，確保其結構正確（計算機將直接解析此JSON）。

請按以下JSON欄位回應：

{"Suggestions": "重要事項：在撰寫時需注意以下內容：\n- 請確保章節摘要與大綱在情節和節奏上大致匹配\n- 避免過度偏離大綱的結構和重點\n- 保持語言流暢自然，避免冗長或模糊表述"}
"DidFollowOutline": true/false

注意：此回應將直接解析為JSON，因此必須嚴格符合格式要求。'''
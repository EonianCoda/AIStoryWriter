EXTRA_PROMPT_INFO_GENERATION = '''請從使用者提示中拓展關鍵資訊：

<USER_PROMPT>
{user_story_prompt}
</USER_PROMPT>

僅列出使用者提示未涵蓋的關鍵點，如章節長度要求, 整體創作願景, 格式規範
（*註：勿用 XML 標籤，僅範例*）
按以下格式回應:  
<EXAMPLE>
# 關鍵補充說明
- 要點 1
- 要點 2
</EXAMPLE>

回應需極簡，且不含使用者提示內容。'''
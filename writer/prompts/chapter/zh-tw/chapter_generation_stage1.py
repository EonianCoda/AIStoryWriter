CHAPTER_GENERATION_STAGE1 = '''{ContextHistoryInsert}

{_BaseContext}

請根據以下章節大綱及先前章節，撰寫第 {_ChapterNum} 章（共 {_TotalChapters} 章）的劇情。

請務必注意先前章節，確保寫作與前一章銜接無縫，並自然過渡至下一章（因此請遵循大綱）！

本章節大綱如下：
<CHAPTER_OUTLINE>
{ThisChapterOutline}
</CHAPTER_OUTLINE>

{FormattedLastChapterSummary}

撰寫第 {_ChapterNum} 章時，請參考以下建議（請務必僅撰寫此章節）：
    - 速度控制：
        - 是否跳過多天？是否簡化事件？請勿如此，應增加場景以詳細描述。
        - 故事是否過度加速某些情節，而過度聚焦於其他部分？
    - 流暢度：各章節是否順暢過渡？情節是否符合讀者邏輯？是否存在特定敘事結構？該結構是否貫穿整個故事？
    - 類型：故事類型是什麼？該類型適合的語言是什麼？場景是否符合類型？

{Feedback}'''
# Debug LangChain 65_SafeGenerateText.LLMSummaryCheck.GenerateChapter.Main
**Note: '```' tags have been removed in this version.**



# Role: system
```You are a helpful AI Assistant. Answer the user's prompts to the best of your abilities.```


# Role: user
```
Please compare the provided summary of a chapter and the associated outline, and indicate if the provided content roughly follows the outline.

Please write a JSON formatted response with no other content with the following keys.
Note that a computer is parsing this JSON so it must be correct.

<CHAPTER_SUMMARY>


Serena realizes her brother Malakar is alive and chose to stay with her after years of believing he was lost. Thalor reveals the truth through a memory of Malakar’s hand holding hers *after* the ritual—not the smile she clung to—showing pure love without fear. As the Blood Moon’s light floods her, Serena understands Malakar’s sacrifice was for her, not against her. She chooses love over destruction, becoming the world’s balance by placing her hands on the moon, shifting her eyes to silver, and finally knowing she was always home.
</CHAPTER_SUMMARY>

<OUTLINE>


Chapter 3: The Heart of the Shattered Peaks takes place in the Shattered Peaks (final battle zone) with fast pacing and climactic tension. The Blood Moon appears fully, pulsing with Serena’s past trauma, while Malakar reveals himself as her brother born from a ritual. Borin (human elder) guides Serena by placing his hand on the Shattered Sword, shifting her from guilt to understanding with the words, *"You were never alone—your brother’s sacrifice was for you."* Thalor (forest spirit) whispers Serena’s brother’s name, causing the Shattered Sword to reassemble in her hands. Ryn (child) creates a glowing light reflecting Serena’s past, showing her brother’s last smile without pain. The implicit conflict questions who the real Demon Lord is—Malakar is not a destroyer but her brother’s soul bound to the land’s balance. Stakes are critical: destroying Malakar ends the world, while merging with him saves it but erases Serena’s identity.
</OUTLINE>

Please respond with the following JSON fields:

{
"Suggestions": str
"DidFollowOutline": true/false
}

Suggestions should include a string containing detailed markdown formatted feedback that will be used to prompt the writer on the next iteration of generation.
Specify general things that would help the writer remember what to do in the next iteration.
It will not see the current chapter, so feedback specific to this one is not helpful, instead specify areas where it needs to pay attention to either the prompt or outline.
The writer is also not aware of each iteration - so provide detailed information in the prompt that will help guide it.
Start your suggestions with 'Important things to keep in mind as you write: 
'.

It's okay if the summary isn't a complete perfect match, but it should have roughly the same plot, and pacing.

Again, remember to make your response JSON formatted with no extra words. It will be fed directly to a JSON parser.
```


# Role: assistant
```<think>
We are given a chapter summary and an outline. We need to compare them and output a JSON with two keys: "Suggestions" (a string in markdown) and "DidFollowOutline" (a boolean).

 Steps:
 1. Read the chapter summary and the outline.
 2. Check if the chapter summary roughly follows the outline.

 Chapter Summary:
   - Serena realizes her brother Malakar is alive and chose to stay with her after years of believing he was lost.
   - Thalor reveals the truth through a memory of Malakar’s hand holding hers *after* the ritual—not the smile she clung to—showing pure love without fear.
   - As the Blood Moon’s light floods her, Serena understands Malakar’s sacrifice was for her, not against her.
   - She chooses love over destruction, becoming the world’s balance by placing her hands on the moon, shifting her eyes to silver, and finally knowing she was always home.

 Outline (Chapter 3: The Heart of the Shattered Peaks):
   - Takes place in the Shattered Peaks (final battle zone) with fast pacing and climactic tension.
   - The Blood Moon appears fully, pulsing with Serena’s past trauma.
   - Malakar reveals himself as her brother born from a ritual.
   - Borin (human elder) guides Serena by placing his hand on the Shattered Sword, shifting her from guilt to understanding with the words: *"You were never alone—your brother’s sacrifice was for you."*
   - Thalor (forest spirit) whispers Serena’s brother’s name, causing the Shattered Sword to reassemble in her hands.
   - Ryn (child) creates a glowing light reflecting Serena’s past, showing her brother’s last smile without pain.
   - Implicit conflict: who the real Demon Lord is — Malakar is not a destroyer but her brother’s soul bound to the land’s balance.
   - Stakes: destroying Malakar ends the world, while merging with him saves it but erases Serena’s identity.

 Comparison:

 1. The chapter summary does not mention Borin at all. The outline says Borin guides Serena by placing his hand on the Shattered Sword and gives the specific line. The summary does not have this element.

 2. The chapter summary does not mention Ryn (the child) creating a glowing light. The outline says Ryn creates a glowing light reflecting Serena’s past, showing her brother’s last smile without pain. The summary mentions Thalor revealing through a memory of Malakar’s hand holding hers (after the ritual) but not the Ryn element.

 3. The chapter summary does mention Thalor (forest spirit) but in a different way: Thalor reveals the truth through a memory of Malakar’s hand holding hers. The outline says Thalor whispers Serena’s brother’s name, causing the Shattered Sword to reassemble. The summary does not mention the Shattered Sword reassembling.

 4. The chapter summary does not mention the Blood Moon pulsing with past trauma (the outline says it does). However, the summary says "As the Blood Moon’s light floods her", so it's present but the detail of pulsing with past trauma is missing.

 5. The chapter summary says Malakar reveals himself as her brother (this is covered) but the outline says "Malakar reveals himself as her brother born from a ritual". The summary says "Serena realizes her brother Malakar is alive", so it's a bit different (she realizes he's alive, not that he reveals himself as her brother born from a ritual).

 6. The chapter summary does not have the explicit conflict about who the real Demon Lord is (the outline states it as an implicit conflict). However, the summary does say "Malakar is not a destroyer but her brother’s soul bound to the land’s balance" (implied by the context of the sacrifice being for her and her becoming the balance).

 7. The stakes are mentioned in the summary: "She chooses love over destruction, becoming the world’s balance" — which implies the stakes (destroying Malakar ends the world, merging saves it but erases identity). But the outline has a specific description of the stakes.

 8. The summary does not mention the Shattered Sword reassembling (the outline says Thalor's whisper causes it to reassemble). The summary says "placing her hands on the moon" (not the sword).

 9. The summary says: "Thalor reveals the truth through a memory of Malakar’s hand holding hers *after* the ritual—not the smile she clung to—showing pure love without fear." This is a bit different from the outline's Ryn showing the brother's last smile without pain. The outline says Ryn shows the smile without pain, but the summary says Thalor shows a memory of the hand holding (after the ritual) and not the smile.

 10. The summary does not have the element of Borin at all.

 Conclusion on "DidFollowOutline":
   - The summary covers some key points (Serena realizing Malakar is alive, Thalor revealing through a memory, Blood Moon, understanding the sacrifice, becoming the balance) but misses several critical elements from the outline:
        * Borin's role (the specific guidance and the line)
        * Ryn's role (the glowing light and the smile without pain)
        * The Shattered Sword reassembling (which is a key action in the outline)
        * The Blood Moon pulsing with past trauma (the summary only says the light floods her, not the pulsing with trauma)

   However, the summary does have the core plot of Serena understanding that Malakar is her brother and that his sacrifice was for her, and she chooses love to become the balance.

   Given that the outline has 7 points and the summary covers about 4-5 of them (with some variations) but misses 3 critical ones (Borin, Ryn, Shattered Sword reassembly), it does not roughly follow the outline.

   But note: the problem says "it should have roughly the same plot, and pacing". The summary is a bit more focused on Thalor and the memory, and the outline has multiple characters and actions. The summary is missing two major characters (Borin and Ryn) and a key action (Shattered Sword reassembly).

   Therefore, I would say: DidFollowOutline = false.

 11. However, let's re-read the summary: It says "Thalor reveals the truth through a memory of Malakar’s hand holding hers". The outline says Thalor whispers the brother's name and causes the Shattered Sword to reassemble. So the summary does not have the Shattered Sword reassembly. Also, the summary does not have Ryn.

 12. The summary does not mention the ritual in the same way as the outline (the outline says Malakar is born from a ritual, but the summary says he was lost and then found).

 13. The summary does not have the explicit conflict about the Demon Lord (the outline states it as an implicit conflict). But the summary does imply that Malakar is not a destroyer (by saying he sacrificed for her) so it's covered.

 Given the above, the summary does not follow the outline closely enough to be considered a rough match.

 Therefore: DidFollowOutline = false.

 Now, for the Suggestions:

 We need to write a string that starts with "Important things to keep in mind as you write: " and is in markdown.

 The feedback should be specific to the next iteration (so the writer will use it for the next chapter generation). We are not to give feedback on this chapter but on what to do in the next iteration.

 What to focus on for the next iteration:

   - The outline has specific elements that are missing in the summary: Borin (human elder) and his role (placing hand on Shattered Sword and giving the line), Ryn (child) creating a glowing light that shows the brother's last smile without pain, and the Shattered Sword reassembling.

   - Also, the Blood Moon in the outline is described as pulsing with Serena’s past trauma, which the summary doesn't mention.

   - The summary should include the Shattered Sword reassembly as a key action (the outline says Thalor's whisper causes it).

   - The summary should have the character Ryn and the glowing light that reflects the past (showing the smile without pain).

   - The outline has a specific conflict about the Demon Lord (who is the real one) but the summary doesn't explicitly state it. However, the summary does imply it by saying Malakar is her brother and not a destroyer. So we don't need to add that if it's already covered? But the outline says it's an implicit conflict.

   - The pacing: the outline says fast pacing and climactic tension. The summary seems to have a climax but we don't know if it's fast.

   - The summary does not have the ritual birth of Malakar (the outline says "born from a ritual"). The summary says "after years of believing he was lost", so it's a bit different.

   We'll focus on the missing elements.

   Suggestions string:

   "Important things to keep in mind as you write: 

   - Ensure that Borin (the human elder) is included with his specific role: placing his hand on the Shattered Sword and delivering the line: *'You were never alone—your brother’s sacrifice was for you.'* This is a critical moment for shifting Serena from guilt to understanding.

   - Include Ryn (the child) creating a glowing light that reflects Serena’s past, specifically showing her brother’s last smile without pain (as opposed to the smile she clung to in the summary). This element is crucial for the memory of love without fear.

   - The Shattered Sword should reassemble in Serena’s hands as a result of Thalor’s whisper (not just a memory of Malakar’s hand). This reassembly is a key action that the summary currently omits.

   - The Blood Moon should be described as pulsing with Serena’s past trauma (not just flooding her with light) to tie into the emotional state and the ritual context.

   - Clarify the ritual aspect: Malakar was born from a ritual (as per the outline) and not just a brother who was lost. This helps in the revelation of his true nature.

   - The implicit conflict about the Demon Lord (who is the real one) should be woven in as a tension point, but the summary currently focuses on the resolution. The outline states that Malakar is not a destroyer but her brother’s soul bound to the land’s balance. Make sure this is clear without overcomplicating the resolution.

   - Maintain fast pacing and climactic tension throughout the chapter, especially in the final moments."

 However, note: the problem says "It will not see the current chapter, so feedback specific to this one is not helpful". So we don't want to say "this chapter is missing X". We want to give general things that will help the writer in the next iteration.

 We are to write feedback that the writer can use for the next iteration of generation (so the next chapter they write). So we are giving them guidance on what to include in the next chapter (which is the next iteration).

 But note: the problem says "the writer is also not aware of each iteration". So we have to be very general.

 Let me rephrase to be more general and not specific to this chapter:

   Important things to keep in mind as you write: 

   - Always include the human elder (Borin) with his specific role: placing hand on the Shattered Sword and delivering the line about sacrifice for you.

   - Include the child (Ryn) creating a glowing light that reflects the past, showing the brother’s last smile without pain.

   - Ensure the Shattered Sword reassembles in the character’s hands as a result of Thalor’s action.

   - Describe the Blood Moon as pulsing with past trauma to tie into the emotional state.

   - Clarify the ritual birth of the character (Malakar) to avoid confusion about his origin.

   - Maintain fast pacing and climactic tension in the final battle zone.

 But note: the problem says "Specify general things that would help the writer remember what to do in the next iteration of generation."

 We are writing for the next iteration (the next chapter they generate). So we are giving them the key points they must include.

 However, the problem says: "It will not see the current chapter, so feedback specific to this one is not helpful". So we avoid any reference to this chapter.

 Let's write the suggestions string accordingly.

 Final Suggestions string:

 "Important things to keep in mind as you write: 

 - Always include Borin (the human elder) with his specific role: placing his hand on the Shattered Sword and delivering the line: *'You were never alone—your brother’s sacrifice was for you.'* This moment is critical for shifting the character from guilt to understanding.

 - Include Ryn (the child) creating a glowing light that reflects the past, specifically showing the brother’s last smile without pain (as opposed to the smile the character clung to).

 - Ensure the Shattered Sword reassembles in the character’s hands as a result of Thalor’s whisper.

 - Describe the Blood Moon as pulsing with the character’s past trauma to tie into the emotional state and ritual context.

 - Clarify the ritual origin of the character (Malakar) to avoid confusion about his true nature.

 - Maintain fast pacing and climactic tension throughout the chapter, especially in the final battle zone."

 But note: the problem says "It's okay if the summary isn't a complete perfect match, but it should have roughly the same plot, and pacing." We are not to be too harsh.

 However, in this case, the summary does not follow the outline roughly (it misses 3 key elements). So we set DidFollowOutline to false.

 Let's write the JSON.

 Note: The JSON must be valid.

 We'll do:

 {
   "Suggestions": "Important things to keep in mind as you write: \n\n- Always include Borin (the human elder) with his specific role: placing his hand on the Shattered Sword and delivering the line: *'You were never alone—your brother’s sacrifice was for you.'* This moment is critical for shifting the character from guilt to understanding.\n\n- Include Ryn (the child) creating a glowing light that reflects the past, specifically showing the brother’s last smile without pain (as opposed to the smile the character clung to).\n\n- Ensure the Shattered Sword reassembles in the character’s hands as a result of Thalor’s whisper.\n\n- Describe the Blood Moon as pulsing with the character’s past trauma to tie into the emotional state and ritual context.\n\n- Clarify the ritual origin of the character (Malakar) to avoid confusion about his true nature.\n\n- Maintain fast pacing and climactic tension throughout the chapter, especially in the final battle zone.",
   "DidFollowOutline": false
 }

 However, note: the problem says "the writer is also not aware of each iteration". So we are giving them the key points for the next iteration.

 But wait: the problem says "Specify general things that would help the writer remember what to do in the next iteration of generation." So we are giving them the key points.

 Let me check the string: it's in markdown? The problem says "detailed markdown formatted feedback". We are using markdown: bullet points, italics for the quote.

 But note: the problem says "It will be fed directly to a JSON parser", so we must be careful with newlines and quotes.

 We'll use double quotes for the JSON string and escape the inner quotes.

 Alternatively, we can write the string without markdown? But the problem says "markdown formatted feedback". So we do it.

 However, the problem says: "Start your suggestions with 'Important things to keep in mind as you write: '"

 We'll write the string exactly as:

 "Important things to keep in mind as you write: \n\n- Always include Borin (the human elder) with his specific role: placing his hand on the Shattered Sword and delivering the line: *'You were never alone—your brother’s sacrifice was for you.'* This moment is critical for shifting the character from guilt to understanding.\n\n- Include Ryn (the child) creating a glowing light that reflects the past, specifically showing the brother’s last smile without pain (as opposed to the smile the character clung to).\n\n- Ensure the Shattered Sword reassembles in the character’s hands as a result of Thalor’s whisper.\n\n- Describe the Blood Moon as pulsing with the character’s past trauma to tie into the emotional state and ritual context.\n\n- Clarify the ritual origin of the character (Malakar) to avoid confusion about his true nature.\n\n- Maintain fast pacing and climactic tension throughout the chapter, especially in the final battle zone."

 But note: the problem says "detailed markdown formatted feedback". We are using markdown with bullet points and italics.

 However, the JSON parser will handle the string as long as it's a valid string.

 Let's write it without the extra spaces? We'll do it as above.

 But note: the problem says "It will be fed directly to a JSON parser", so we must escape the quotes and newlines.

 We can use a string that is a valid JSON string.

 Alternatively, we can write the string without the newlines? But the problem says "detailed markdown", so we want the newlines.

 We'll use \n for newlines and escape the inner quotes.

 However, the problem says: "a computer is parsing this JSON so it must be correct".

 Let me write the string with proper escaping.

 But note: the problem says "no other content", so we output only the JSON.

 I'll write the string with the following:

   - The string starts with "Important things to keep in mind as you write: "
   - Then a newline (represented as \n in the string)
   - Then the bullet points.

 We'll do:

   "Suggestions": "Important things to keep in mind as you write: \n\n- Always include Borin (the human elder) with his specific role: placing his hand on the Shattered Sword and delivering the line: *'You were never alone—your brother’s sacrifice was for you.'* This moment is critical for shifting the character from guilt to understanding.\n\n- Include Ryn (the child) creating a glowing light that reflects the past, specifically showing the brother’s last smile without pain (as opposed to the smile the character clung to).\n\n- Ensure the Shattered Sword reassembles in the character’s hands as a result of Thalor’s whisper.\n\n- Describe the Blood Moon as pulsing with the character’s past trauma to tie into the emotional state and ritual context.\n\n- Clarify the ritual origin of the character (Malakar) to avoid confusion about his true nature.\n\n- Maintain fast pacing and climactic tension throughout the chapter, especially in the final battle zone."

 But note: the problem says "detailed markdown", so we are using markdown.

 However, the problem says: "It will not see the current chapter, so feedback specific to this one is not helpful". We have avoided that.

 Let's output the JSON.

 Important: The JSON must be valid.

 We'll write:

 {
   "Suggestions": "Important things to keep in mind as you write: \n\n- Always include Borin (the human elder) with his specific role: placing his hand on the Shattered Sword and delivering the line: *'You were never alone—your brother’s sacrifice was for you.'* This moment is critical for shifting the character from guilt to understanding.\n\n- Include Ryn (the child) creating a glowing light that reflects the past, specifically showing the brother’s last smile without pain (as opposed to the smile the character clung to).\n\n- Ensure the Shattered Sword reassembles in the character’s hands as a result of Thalor’s whisper.\n\n- Describe the Blood Moon as pulsing with the character’s past trauma to tie into the emotional state and ritual context.\n\n- Clarify the ritual origin of the character (Malakar) to avoid confusion about his true nature.\n\n- Maintain fast pacing and climactic tension throughout the chapter, especially in the final battle zone.",
   "DidFollowOutline": false
 }

 But note: the problem says "the writer is also not aware of each iteration". So we are giving them the key points for the next iteration.

 However, the problem says: "It's okay if the summary isn't a complete perfect match, but it should have roughly the same plot, and pacing." We determined it doesn't roughly follow.

 Let me double-check: the summary has the core of the story (Serena realizing Malakar is alive, the memory of his hand, the Blood Moon, the sacrifice, and becoming the balance) but misses the Borin, Ryn, and Shattered Sword reassembly. So it's not a rough match.

 Therefore, DidFollowOutline = false.

 We output the JSON.

 Note: The problem says "Please write a JSON formatted response with no other content".

 Let's write it.
</think>

{
  "Suggestions": "Important things to keep in mind as you write: \n\n- Always include Borin (the human elder) with his specific role: placing his hand on the Shattered Sword and delivering the line: *'You were never alone—your brother’s sacrifice was for you.'* This moment is critical for shifting the character from guilt to understanding.\n\n- Include Ryn (the child) creating a glowing light that reflects the past, specifically showing the brother’s last smile without pain (as opposed to the smile the character clung to).\n\n- Ensure the Shattered Sword reassembles in the character’s hands as a result of Thalor’s whisper.\n\n- Describe the Blood Moon as pulsing with the character’s past trauma to tie into the emotional state and ritual context.\n\n- Clarify the ritual origin of the character (Malakar) to avoid confusion about his true nature.\n\n- Maintain fast pacing and climactic tension throughout the chapter, especially in the final battle zone.",
  "DidFollowOutline": false
}```
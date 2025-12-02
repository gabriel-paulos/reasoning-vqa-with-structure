qa_to_declarative_statement= '''

User: You are presented with a question with corresponding multi-choice answer options. You are required to convert each option along with the question into a grammatical declarative statement sentence. Most importantly, make sure that proving the statement amounts to choosing that answer option over the other ones.
Note: do not modify the semantics of the sentence. Do not add new information or your own descriptions into the statements. <Examples>:
# Input:
Question: Why does the brown cat watch the other cat eat food?
(A). Wants to go into box.
(B). Wants to have a rest
(C). Waiting for his turn
(D). Playing with it
# Output:
(A). The brown cat watch the other cat eat food because it wants to go into the box. (B). The brown cat watch the other cat eat food because it wants to have a rest
(C). The brown cat watch the other cat eat food because it waits for his turn for food. (D). The brown cat watch the other cat eat food because it’s playing with it.
Assistant:
# Input: <user_inputs> # Output:

'''

statement_decomposition_prompt='''

User: Given a declarative statement, analyze the statement to extract distinct claims that could support this statement. Specifically, based on the claims, you need to decompose the statement into two shorter sub-statements, which can be utilized to verify the original statement jointly.
Note:
1. Each sub-statement should be verifiable and not overlap in content with the other one.
2. Make sure that the original statement is True if and only if both two sub-statements are True.
3. The sub-statement should be declarative sentences and avoid any hypothetical expression, such as “Let’s assume”, “consider
whether”.
4. If you think the given statement does not contain any verifiable facts, output “Decomposition failed: No worthy decomposition
found.”
5. Do not add additional information into the sub-statements that didn’t indicate by the original statement.
<Examples>:
# Input: The man with spectacles looked to the camera after he looked down on the floor.
# Output:
(1) The man with spectacles looked to the camera.
(2) The man with spectacles first looked down on the floor.
# Input: The boy starts shake his legs to mimic the toy movement.
# Output:
(1) The boy mimics the toy movement with his legs.
(2) The toy moves in shaking.
# Input: The lady with jacket clapped her hands when the lady with microphone is performing. # Output:
(1) The lady with jacket clapped her hands.
(2) The lady with microphone is performing.
Assistant:
# Input: <user_inputs> # Output:


'''

fact_statement_extraction_prompt= '''

User: Given multiple possible statements, your task is to extract a common fact claim. A fact claim is a statement that is acknowledged by all provided statements. Do not include any additional knowledge or information beyond what is explicitly present in the statements.
<Examples>:
# Input:
(A). The brown cat watch the other cat eat food because it wants to go into the box. (B). The brown cat watch the other cat eat food because it wants to have a rest
(C). The brown cat watch the other cat eat food because it waits for his turn for food. (D). The brown cat watch the other cat eat food because it’s playing with it.
# Output:
The brown cat watch the other cat eat food.
Assistant:
# Input: <user_inputs> # Output:

'''

fact_retrieving_statement_prompt='''

User: You are acting as a retriever. Given a query along with its structured semantic representation, your task is to identify the single most relevant frame from the provided semantic representations of all video frames. Carefully analyze the critical objects, actions, and attributes indicated by the query, compare them with all the candidate frames, and select the frame where the query is most likely to be represented.
Note: do not refuse to provide an answer and directly return the retrieved frame ID without any additional explanations.
<Examples>:
# Input:
Query:
The boy in yellow is crawling out of the green mat.
<boy, in, yellow>, <boy, crawl, mat>, <boy, out of, mat>, <mat, in, green> Candidate frames:
(1) <boy, in, yellow>, <boy, pick, toy>
(2) <boy, in, yellow>, <boy, stand, _>, <boy, in front of, chair> (3) <boy, play, toy>, <boy in yellow>
(4) <boy, on, mat>, <boy, sit, _>, <boy in yellow>,
(5) <boy, in, yellow,>, <boy, playing, _>, <boy, in, room>
(6) <boy, sit, mat>, <boy, in, room>
# Output frame ID:
(4)
Assistant:
# Input: <user_inputs> # Output frame ID:

'''

evidence_nav_prompt='''
User: You are acting as a navigator over the temporal dimension of a video. You will be presented with a question, a keyframe timestamp, and a fact statement describing an event or action occurring at that moment. Starting from this timestamp, your role is to determine the next direction to explore in the video, aiming to locate the segment most likely to answer the question. To guide your navigation, consider the semantic context of the entire video and prioritize the reasoning cues in the question (e.g., "what," "how," "why") and temporal indicators (e.g., "after," "while“, “at the end of video”) to make an informed decision about the next steps. Note: you need to return your navigation from the following options:
(a) Look back
(b) Look behind
(c) Look around
<Examples>:
# Input:
Question: What does the boy do before crawling out of the green mat in the middle? Information of frames:
(1) <boy, in, yellow>, <boy, pick, toy>
(2) <boy, in, yellow>, <boy, stand, _>, <boy, in front of, chair>
(3) <boy, play, toy>, <boy in yellow>
(4) <boy, on, mat>, <boy, sit, _>, <boy in yellow>,
(5) <boy, in, yellow,>, <boy, playing, _>, <boy, in, room>
(6) <boy, sit, mat>, <boy, in, room>
Key frame timestamp and corresponding statement:
(4)
The boy is crawling out of the green mat.
# Output navigation:
(a) Look back
Assistant:
# Input: <user_inputs> # Output navigation:

'''

statement_verification_prompt='''
User: Are the following statements TRUE or FALSE in this video? Carefully watch the video content, paying close attention to the objects, actions, and attributes of each object in the video. For each statement, determine whether it is TRUE or FALSE in the video. Provide a response of ‘TRUE’ if the statement is correct, or ‘FALSE’ if the statement is incorrect.
Note: Apart from the video content, you cannot use additional information or rely on commonsense knowledge. Directly output 'TRUE' or 'FALSE' without adding explanations or any markers.
Assistant:
# Input: <user_inputs_video > <user_inputs_text> # Output:

'''
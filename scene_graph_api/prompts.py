captioner_prompt = " You will be given a video. You need to describe the events in the video. Start your description with the first event happening in the video, describe all the events in chronological, causal, or hierarchical order,and end your description with the last event in the video. In your description, indicate temporal relations of events using keywords such as 'after' 'then' 'meanwhile' etc.; indicate causal relations of events using key words such as 'causing' etc.; indicate hierarchical relations of events using keywords such as 'by' 'with' etc. When referring to entities, always use descriptive keywords representing their characteristics, such as 'white Honda Civic', 'man in black suit', 'chair on the left', etc. Make sure the references to the entities are consistent, for example, if you mentioned a 'black car with broken window', refer to it with the same name ('black car with broken window') everywhere else you mention it. For entities mentioned in the question, reference them using the same name everywhere else, for example, if the question mentions 'man in black pants', use 'man in black pants' to reference that entity. Your description will be used to answer the following question: {question}? Choices: A. {a0} B. {a1} C. {a2} D. {a3} E. {a4}. When describing the video, do not answer the question, only describe the video in detail. Example description: Two boxers, one in gold-white shorts, and the other one in orange-white shorts, facing each other in a boxing ring; meanwhile, the referee is observing the fight inside the ring; at the same time, a large number of audiences are watching. During the fight, the boxer in gold-white shorts throws a left jab, knocking down the opponent in orange-white shorts. After that, the referee counts to ten while the boxer in gold-white shorts raises his hand in victory; at the same time, the crowd cheers and applauds after the knockout. The referee announced the victory the boxer in gold-white victorious after he counted to ten; after that the boxer in gold-white shorts goes to a big screen and celebrates. Meanwhile, the referee and the boxer’s cornermen check the well-being of the boxer in orange-white shorts."


graph_generator_prompt = '''

Given a paragraph, please extract all events and its argument roles in the following format:
    {<event_1>: {<argument_role_type_1>: [argument_role_1_1, argument_role_1_2, ...], <argument_role_type_2>: [
        argument_role_2_1, argument_role_2_2, ... ] , ....},
     <event_2>: {<argument_role_type_1>: [argument_role_1_1, argument_role_1_2, ...], <argument_role_type_2>: [
         argument_role_2_1,argument_role_2_2, ...], ...},
    ...}
    Coreference of argument roles with different names should follow the name of the first occurrence of the
        argument. For example, \"blue car driving left\" and \"blue car turning left\" both should be named \"
        driving\".
    Coreference of events with different names should follow the name of the first occurrence of the argument. For
         example, \"blue car\" and \"blue vehicle\" both should be named \"blue car\".
    Collective arguments that are should maintain its finest grained form in the text. For example, if \"three
        cars\" containing \"red car\", \"blue car\", and \"green car\", then reference the three cars as [\"red
        car\", \"blue car\", \"green car\"] in the graph.
    Differentiate events with the same name with indices. For example: \"man in blue shirt is eating pasta\" and
        \"woman is eating broccoli and rice\" should be \"{\"eating_0\": \"{\"agent\":[\"man in white\"], \"item
        \":[\"pasta\"]}, \"eating_1\": {\"agent\":[\"woman\"], \"item\":[\"rice\",\"broccoli\"]}}, this should
        also be reflected in the event graph.
    In addition, extract all possible event-event relationships. The relationships should be from among causal,
        temporal and hierarchical relationships and the relationship should be directed.
    The format should be:
    {<event_1>: {causal: [<event_4>, <event_5>], temporal: [<event_2>], hierarchical: [<event_7>, <event_8>]},
    <event_2>: {causal:[<event_1>]},
    <event_3>:{},
    ....}
    Causal Definition: An event A is causally related to event B if A was the cause of event B. For example: Black
         car hits the man in white. The man in white falls. Event relation: {\"Hit\": {\"causal\":[\"Fall\"]}}.
    Temporal Definition: An event A is temporally related to event B if A started before B did.

    Hierarchical Definition: An event A is hierarchically related to event B if B occurred spatiotemporally within
      A. Example: The man in white is fighting the person in monster costume. The man in white throws a punch.
     Event relation: {\"Fight\": {\"hierarchical\":[\"Throw\"]}}. Example: The waiter is serving the food by
     passing a tray. Event relation: {\"Serve\": {\"hierarchical\": [\"Pass\"]}}. Example: The soldier is
     holding his gun while patrolling. Event relation: {\"Patrol\": {\"hierarchical\": [\"Hold\"]}}.
    In addition, you will also be given a question related to the text. You should focus on the events related to
        the question when generating the graph.
    Example Text:
    People are marching on a street during a protest. Police fired tear gas to disperse the crowd.
    Example Question: Why did the police fired the tear gas?
    Example Response:
    Events:
    {
    \"Protest\": {\"agent\": [\"people\"], \"place\": \"street\", \"description\": \"People are protesting on the
        street.\"},
    \"Marching\": {\"agent\": [\"people\"], \"place\": \"street\", \"description\": \"People are marching on the
        street.\"},
    \"Fired\": {\"agent\": [\"police\"], \"item\": \"tear gas\". \"description\": \"Police fired tear gas.\"},
    \"Disperse\": {\"item\": [\"crowd\"], \"description\": \"Crowd dispersed.\"}
    }
    Events-Events Relationships:
    {
    \"Protest\": {\"hierarchical\": [\"marching\", \"fired\", \"disperse\"]},
    \"Marching\": {\"temporal\":[\"Fired\"]},
    \"Fired\": {\"causal\":[\"disperse\"], \"temporal\":[\"disperse\"]},
    \"Disperse\": {}
    }
    Example Question: Who came after the black car in the middle turned right?
    Example Text:
    Three cars are waiting at a traffic light. When it turned green, the red one went left, the black one on the
        right went right, and the middle black one went straight. After the black car turned right, a red tow
        truck drove through the road.
    Example Response:
    Events:
    {
    \"Waiting\": {\"agent\": [\"red car\", \"black car on the right\", \"middle black car\"], \"place\": [\"
        traffic light\"], \"description\": \"The red car, the black car on the right, and the black car in the
        middle are waiting for traffic light.\"},
    \"Turned\": {\"agent\": [\"traffic light\"], \"color\": [\"green\"], \"description\": \"The traffic light
        turned green.\"},
    \"Went_0\": {\"agent\": [\"red car\"], \"direction\": [\"left\"], \"description\": \"The red car turned left
        .\"},
    \"Went_1\": {\"agent\": [\"black car on the right\"], \"direction\": [\"right\"], \"description\": \"The black
        car on the right turned right.\"},
    \"Went_2\": {\"agent\": [\"middle black car\"], \"direction\": [\"straight\"], \"description\": \"The middle
        black car turned straight.\"},
    \"Drive\": {\"agent\": [\"red tow truck\"], \"place\":[\"road\"], \"description\": \"The red tow truck drove
    through the road.\"}
    }

    Events-Events Relationships:
{
\"Waiting\": {\"temporal\": [\"Turned\"]},
\"Turned\": {\"causal\":[\"Went_0\", \"Went_1\", \"Went_2\", \"Drive\"], \"temporal\": [\"Went_0\", \"Went_1
     \", \"Went_2\"]},
    \"Went_0\": {\"temporal\":[\"Drive\"]},
    \"Went_1\": {\"temporal\":[\"Drive\"]},
    \"Went_2\": {\"temporal\":[\"Drive\"]},
    \"Drive\": {}
    }
    Question: What made the crowd applaud?
    Example Text:
    Two boxers, one in gold-white shorts, and the other one in orange-white shorts, facing each other in a boxing
        ring. The boxer in gold-white shorts throws a left jab, knocking down the opponent in orange-white shorts.
        The referee counts to ten as the boxer in gold-white shorts raises his hand in victory. The crowd cheers
        and applauds. The boxer in gold-white shorts goes to a big screen and celebrates while the referee and the
        boxer’s cornermen check the well-being of the boxer in orange-white shorts.
    Example Response:
    Events:
    {
    \"Facing\": {\"agent\": [\"boxer in gold-white shorts\", \"boxer in orange-white shorts\"], \"direction\":[\"
        each other\"], \"location\": [\"ring\"], \"description\": \"Boxer in gold-white shorts and boxer in orange
        -white shorts are facing each other in the ring.\"},
    \"Throw\": {\"agent\": [\"boxer in gold-white shorts\"], \"action\": [\"left jab\"], \"description\":\"The
        boxer in gold-white shorts throws a left jab\"},
    \"Knock down\": {\"agent\": [\"boxer in gold-white shorts\"], \"target\": [\"boxer in orange-white shorts\"],
        \"description\": \"The boxer in gold-white shorts knocks down the boxer in orange-white shorts\"},
    \"Count to ten\": {\"agent\":[\"refree\"], \"description\": \"The refree counts to ten\"},
    \"Raise\": {\"agent\": [\"boxer in gold-white shorts\"], \"item\":[\"hands\"], \"description\": \"Boxer in
        gold-white shorts raises his hands in victory.\"},
    \"Applaud\": {\"agent\": [\"the crowd\"], \"description\": \"The crowd applauds.\"},
    \"Go\": {\"agent\": [\"boxer in gold-white shorts\"], \"destination\":[\"big screen\"], \"description\": \"
        Boxer in gold-white shorts goes to the big screen\"},
    \"Celebrate\": {\"agent\": [\"boxer in gold-white shorts\"], \"description\": \"Boxer in gold-white shorts
        celebrates.\"},
    \"Check\": {\"agent\": [\"referee\", \"boxer’s cornermen\"], \"target\":[\"boxer in orange-white shorts\"], \"
        description\": \"the referee and the boxer’s cornermen check the well-being of the boxer in orange-white
        shorts.\"}
    }
    Events-Events Relationships:
    {
    \"Facing\": {\"temporal\": [\"Throw\"]},
    \"Throw\": {\"causal\": [\"Knock down\"]},
    \"Knock down\": {\"causal\": [\"Count to ten\", \"Raise\", \"Check\", \"Applaud\"], \"temporal\": [\"Count to
        ten\", \"Raise\", \"Applaud\"]},
    \"Count to ten\": {\"temporal\":[\"Go\", \"Check\"]},
    \"Raise\": {\"temporal\": [\"Go\", \"Check\"]},
    \"Applaud\": {\"temporal\": [\"Go\", \"Check\"]},
    \"Go\": {\"temporal\": [\"Celebrate\"]},
    \"Celebrate\": [],
    \"Check\": []
    }
    Given Text:

'''

code_generator_prompt = '''
    Given the list of available python apis, please generate python code to answer the given question.
    class Event:
        def __init__(self, name:str, args:dict):
            \"\"\"Initializes the event class with an event name and argument roles
            Parameters
            -------
            name: str
                name of the event
            args: dict
                event argument in this format: {arg_role: [arg_values]}
            \"\"\"
        def __str__(self,):
            return self.description
        def find_node(self, name, arguments):
            \"\"\" Returns an event node from the event graph given the event name and the associated arguments
            -------
            >>> # Find the event "riding" with agent "man in hat"
            >>> def execute_command(graph, caption, question, possible_answers, video_file_name):
            >>>     event_graph = EventGraph(graph, question, possible_answers)
            >>>     event_name = \"riding\"
            >>>     agent = \"man in hat\"
            >>>     event_node = event_graph.find_node(event_name, args={\"agent\": agent})
            \"\"\"
        def simple_query(self, query):
            \"\"\"Returns the answer to a basic question yes-or-no asked about arguments of the event, returns
                either True or False. The questions are about basic information about the event, and are not meant
                to be used for complex reasoning for the event, reasoning between among events, or external
                knowledge.
            Examples
            -------
        >>> # Find if the event "running" has a dog in it
        >>> def execute_command(graph, caption, question, possible_answers, video_file_name):
        >>>         event_graph = EventGraph(graph, question, possible_answers)
        >>>         event_name = \"running\"
        >>>         event_node = event_graph.find_node(event_name)
        >>>         has_dog = event_node.simple_query("Is there a dog in this event?.") # Ask an      simple yes-or-no question to determine if the event contains a dog
        >>>         if has_dog:
        >>>             return ’yes’
        >>>         else:
        >>>             return 'no'
        \"\"\"

    event_graph = EventGraph(graph, question, possible_answers)
    event_name = \"running\"
    event_node = event_graph.find_node(event_name)
    has_dog = event_node.simple_query("Is there a dog in this event?.") # Ask an simple yes-or-no
    question to determine if the event contains a dog
    if has_dog:
        return ’yes’
    else:
    return ’no’
    class EventGraph:
        def __init__(self, event_graph, question, possible_answers):
            \"\"\"Initializes an event graph. Also creates an Event item for each event.
            Each event is stored internally as a string but interfaces with outside class with Event items.
            Parameters
            -------
            event_graph: Tuple[dict,dict]
                event_graph in the following format: ({ <event_1>: {<argument_role_type_1>: argument_role_1, <
                    argument_role_type_2>: argument_role_2, ....},
                                        <event_2>: {<argument_role_type_1>: argument_role_1, <
                                            argument_role_type_2>: argument_role_2, ....},
                                        ...}, # Containing events and their arguments,
                {<event_1>: {causal: [<event_4>, <event_5>], temporal: [<event_2>], hierarchical: [<event_7>, <
    event_8>]},
                                <event_2>: {causal:[<event_1>]},
                                <event_3>:{},
                                ....} # Containing relationships between events)
            \"\"\"
            self.event_graph, self.events = self.parse_events(event_graph)
            self.event_graph = event_graph
            self.events_dict = {}
            for event, args in events_json.items():
                self.events_dict[event] = Event(event, args)

    def iterate_nodes(self):
        \"\"\" Iterates through all nodes in the graph, to be used in a for loop
        >>> # How many people are there in this video?
        >>> def execute_command(graph, caption, question, possible_answers, video_file_name):
        >>>     event_graph = EventGraph(graph, question, possible_answers)
        >>>     all_people = set()
        >>>     for event in event_graph.iterate_nodes():
        >>>         for arg_name, arg_values in event.args.items():
        >>>             for arg_value in arg_values: # arg_values: List[str] contains all the arguments under arg_name
        >>>                 is_person = event.simple_query(f\"Is {arg_value} a person?\") # Ask an simple yes-or-no question to determine if the argument is a person or not
        >>>                 if is_person:
        >>>                     all_people.add(arg_value)
        >>>     info = {\'all the people in the video \': all people}
        >>>     answer = select_answer(question, possible-answers, info, event_graph)
        >>>     return answer, info, event_graph \"\"\"
        return find_node(event_graph, node)
    def find_node(self, event_name, args=None):
        \"\"\"Returns an event node from the event graph given the event name and the associated arguments
        >>> # Find the event "knight riding horse"
        >>> def execute_command(graph, caption, question, possible_answers, video_file_name):
        >>>     event_graph = EventGraph(graph, question, possible_answers)
        >>>     event_name = \"riding\"
        >>>     agent = \"knight\"
        >>>     item = \"horse\"
        >>>     event_node = event_graph.find_node(event_name, args={\"agent\": agent, \"item\": item})
        >>>     info = {\"event\": event_node}
        >>>     answer = select_answer(question, possible_answers, info, event_graph)
        >>>     return answer, info, event_graph\"\"\"
        return find_node(event_graph, node)
    def get_children(self, node):
        \"\"\"Returns all the children nodes of the specified event node
        >>> # Find the child events of "how are the protesters getting more attention"
        >>> def execute_command(graph, caption, question, possible_answers, video_file_name):
        >>>     event_graph = EventGraph(graph, question, possible_answers)
        >>>     event_name = \"getting attention\"
        >>>     agent = \"protesters\"
        >>>     event_node = event_graph.find_node(event_name, args={\"agent\": agent})
        >>>     children = event_graph.get_children(event_node)
        >>>     info = {\"event\": event_node, \"events contained by the protesters getting attention\":
        >>>     answer = select_answer(question, possible_answers, info, event_graph)
        >>>     return answer, info, event_graph
    \"\"\"
    return get_children(event_graph, node)

    def get_parent(self, node):
        \"\"\"Returns the parent node of the specified event node
        >>> # Find the parent events of "why is the man cutting vegetables"
        >>> def execute_command(graph, caption, question, possible_answers, video_file_name):
        >>>     event_graph = EventGraph(graph, question, possible_answers)
        >>>     event_name = \"Cut\"
        >>>     agent = \"man\"
        >>>     item = \"vegetables\"
        >>>     event_node = event_graph.find_node(event_name, args={\"agent\": agent, \"item\": item})
        >>>     parent = event_graph.get_parent(event_node)
        >>>     caused_by = event_graph.get_caused_by(event_node)
        >>>     info = {\"event\": event_node, \"events containing man cutting vegetables\": parent, \"events
            caused man cutting vegetables\": caused_by}
                answer = select_answer(question, possible_answers, info, event_graph)
                return answer, info, event_graph
        return get_parent(event_graph, node)
    
        
    def get_temporal_after(self, node):
        \"\"\"Returns all the events that happened after the specified event node
        >>> # Find the events happened after "man in blue driving black car"
        >>> def execute_command(graph, caption, question, possible_answers, video_file_name):
        >>>     event_graph = EventGraph(graph, question, possible_answers)
        >>>     event_name = \"driving\"
        >>>     agent = \"man in blue\"
        >>>     item = \"black car\"
        >>>     event_node = event_graph.find_node(event_name, args={\"agent\": agent, \"item\": item})
        >>>     after = event_graph.get_temporal_after(event_node)
        >>>     info = {\"event\": event_node, \"events after man in blue driving black car\": after}
        >>>     answer = select_answer(question, possible_answers, info, event_graph)
        >>>     return answer, info, event_graph
        \"\"\"
        return temporal_after(node)

    def get_temporal_before(self, node):
        \"\"\"Returns all the events that happened before the specified event node
        >>> # Find the events happened before "the white horse with number 3 passed the finish line"
        >>> def execute_command(graph, caption, question, possible_answers, video_file_name):
        >>>     event_graph = EventGraph(graph, question, possible_answers)
        >>>     event_name = \"pass\"
        >>>     agent = \"white horse with number 3\"
        >>>     location = \"finish line\"
        >>>     event_node = event_graph.find_node(event_name, args={\"agent\": agent, \"location\": location})
        >>>     before = event_graph.get_temporal_before(event_node)
        >>>     info = {\"event\": event_node, \"the white horse with number 3 passed the finish line\": before}
        >>>     answer = select_answer(question, possible_answers, info, event_graph)
        >>>     return answer, info, event_graph
        \"\"\"
        return temporal_before(node)

    
    def get_resulted_in(self, node):
        \"\"\"Returns the event that resulted in specified event node
        >>> # Find the events causing "the soldier camouflage fell to the ground"
        >>> def execute_command(graph, caption, question, possible_answers, video_file_name):
        >>>     event_graph = EventGraph(graph, question, possible_answers)
        >>>     event_name = \"fall\"
        >>>     agent = \"soldier in camouflage\"
        >>>     event_node = event_graph.find_node(event_name, args={\"agent\": agent})
        >>>     resulted_in = event_graph.get_resulted_in(event_node)
        >>>     before_event = event_graph.get_temporal_before(event_node)
        >>>     info = {\"event\": event_node, \"The soldier camouflage fell to the ground because of these
            events\": resulted_in, \"These events happened before the soldier in camouflage fell to the ground\": before_event}
        >>>     answer = select_answer(question, possible_answers, info, event_graph)
        >>>     return answer, info, event_graph

        \"\"\"
        return caused_by(node)

    def get_caused_by(self, node):
        \"\"\"Returns all the events that happened due to the specified event node"
        >>> # Find the events happened due to "the samurai in Japanese armor wielding his katana"
        >>> def execute_command(graph, caption, question, possible_answers, video_file_name):
        >>>     event_graph = EventGraph(graph, question, possible_answers)
        >>>     event_name = \"wield\"
        >>>     agent = \"samurai in Japanese armor\"
        >>>     item = \"katana\"
        >>>     event_node = event_graph.find_node(event_name, args={\"agent\": agent, \"item\": item})
        >>>     happened_after = event_graph.get_temporal_after(event_node)
        >>>     caused_by = event_graph.get_caused_by(event_node)
        >>>     info = {\"event\": event_node, \"The samurai in Japanese armor wielding his sword caused these
            events to happen\": caused_by, \"These events happened after the samurai in Japanese armor
            wielding his sword\": happened_after}
        >>>     answer = select_answer(question, possible_answers, info, event_graph)
        >>>     return answer, info, event_graph
        \"\"\"
        return resulted_in(node)
        
    def select_answer(question, possible_answers, info, event_graph):
    \"\"\"Selects an Answer from the possible answers given the question and the info in a dictionary format
         .\"\"\"
    return select_answer(question, possible_answers, info, event_graph)

    Question: How many cats are there in the video? A. one B. two C. three D. four E. five
    def execute_command(graph, caption, question, possible_answers, video_file_name):
        event_graph = EventGraph(graph, question, possible_answers)
        events_mentioning_location = []
        all_cats = set()
        for event in event_graph.iterate_nodes():
            for arg_name, arg_values in event.args.items():
                for arg_value in arg_values: # arg_value: List[str] contains the arguments under arg_name
                    is_cat = event.simple_query(f\"Is {arg_value} a cat?\")
                    if is_cat:
                        all_cats.add(arg_value)
        info = {\"all the cats in the video\": all_cats}
        answer = select_answer(question, possible_answers, info, event_graph)
        return answer

Example Question: Where is the video taking place? A. Road B. House C. Dog D. Dining room E. street
def execute_command(graph, caption, question, possible_answers, video_file_name):
    event_graph = EventGraph(graph, question, possible_answers)
    events_mentioning_location = []
    for event in event_graph.iterate_nodes():
        query_result = event.simple_query(\"Does this event mention any location, or does it hint the location
              where the event is happening?\")
        if query_result:
            events_mentioning_location.append(event)
    info = {\"the events mentioning location\": events_mentioning_location}
    retry_answering = 3
    answer = select_answer(question, possible_answers, info, event_graph)
    return answer

Example Question: how is the man in blue feeling after standing up from the chair? A. Happy B. Sad C. Angry D. Neutral E. Surprised
def execute_command(graph, caption, question, possible_answers, video_file_name):
    event_graph = EventGraph(graph, question, possible_answers)
    event_name = \"stand up\"
    agent = \"man in blue\"
    item = \"chair\"
    event_node = event_graph.find_node(event_name, args={\"agent\": agent, \"item\": item})
    after = event_graph.get_temporal_after(event_node)
    children = event_graph.get_children(event_node)
    caused_by = event_graph.get_caused_by(event_node)
    retry_getting_events = 3
    denser_graph_prompt = \"\"\"Read the question and the paragraph, and find relations and/or events in the paragraph that are related to the event the man in blue standing up. Use these events to generate a new graph, such that the new graph has at least one of the following for question answering: the event after \"stand up\", what happens after the man in blue standing up, if you find these events, create these new events and draw the event relation \"stand up\": {\"temporal\":[\"<event>\", ...]} for these events; the event contained by \"stand up\", what is the man doing while he is standing up, if you find these events, create these new events and draw the event relation \"stand up\": {\"hierarchical\":[<event>, ...]} for these events; the event caused by \"stand up\", what happened due to the man standing up, if you find these events, create these new events and draw the event relation \"stand up\": {\"causal\":[<event>, ...]} for these events.\"\"\"
    denser_caption_prompt = \"\"\"Watch the video, describe what happens after the man in blue standing up; is he doing while standing up; what event happened due to the man standing up; and everything else that is helpful in answering the question.\"\"\"
    
    if len(after)+len(children)+len(caused_by) == 0:
        graph = generate_denser_graph(event_node, graph, caption, question, possible_answers,
             denser_graph_prompt, 0)
        event_graph = EventGraph(graph, question, possible_answers)
        event_node = event_graph.find_node(event_name, args={\"agent\": agent, \"item\": item})
        after = event_graph.get_temporal_after(event_node)
        children = event_graph.get_children(event_node)
        caused_by = event_graph.get_caused_by(event_node)

    for i in range(retry_getting_events):
        if len(after)+len(children)+len(caused_by) == 0:
            caption = generate_denser_caption(event_node, graph, caption, question, possible_answers,
                 denser_caption_prompt, video_file_name, i)
            graph = generate_denser_graph(event_node, graph, caption, question, possible_answers,
                 denser_graph_prompt, i+1)
            event_graph = EventGraph(graph, question, possible_answers)
            event_node = event_graph.find_node(event_name, args={\"agent\": agent, \"item\": item})
            after = event_graph.get_temporal_after(event_node)
            children = event_graph.get_children(event_node)
            caused_by = event_graph.get_caused_by(event_node)
        else: 
            break
    
    info = {\"event\": event_node,
            \"events after the man in blue standing up\": after,
            \"events containing the man in blue standing up\": children,
            \"events caused by the man in blue standing up\": caused_by
            }
    retry_answering = 3

    for i in range(retry_answering):
        answer = select_answer(question, possible_answers, info, event_graph)
        if \"not sure\" in answer and i < retry_answering - 1:
            info = get_new_info(answer, info, graph, caption)
        else:
            break
    return answer


    Example Question: whom was the police firing the tear gas to? A. Robbers B. Terrorists C. Protesters D.Attackers E. Prisoners

    Python Code:
    def execute_command(graph, caption, question, possible_answers, video_file_name):
        event_graph = EventGraph(graph, question, possible_answers)
        event_name = \"fire\"
        agent = \"police\"
        item = \"tear gas\"
        event_node = event_graph.find_node(event_name, args={\"agent\": agent, \"item\": item})
        resulted_in = event_graph.get_resulted_in(event_node)
        parents = event_graph.get_parent(event_node)
        caused_by = event_graph.get_caused_by(event_node)
        retry_getting_events = 3
        denser_graph_prompt = \"\"\"Read the question and the paragraph, and find relations and/or events in the paragraph that are related to the event the police firing tear gas. Use these events to generate a new graph, such that the new graph has at least one of the following for answering the question: the event causing \"fire\", what events directly caused the police to fire tear gas, if you find these events, create these new events and draw the event relation <event>: {\"causal\":[\"fire\", ...]} for these events; the event contains \"fire\", what do they achieve by firing the tear gas, if you find these events, create these new events and draw the event relation <event>: {\"hierarchical\":[\"fire\", ...]} for these events; the event caused by \"fire\", what happened due to the firing of tear gas, if you find these events, create these new events and draw the event relation \"fire\": {\"causal\":[<event>, ...]} for these events.\"\"\"
        denser_caption_prompt = \"\"\"Watch the video, describe what causes the police to fire the tear gas; what do they need to achieve to fire the tear gas; what event happened due to the police firing tear gas; and everything else that is helpful in answering the question.\"\"\"
    
        if len(caused_by)+len(parents)+len(resulted_in) == 0:
            graph = generate_denser_graph(event_node, graph, caption, question, possible_answers,
                denser_graph_prompt, 0)
            event_graph = EventGraph(graph, question, possible_answers)
            event_node = event_graph.find_node(event_name, args={\"agent\": agent, \"item\": item})
            resulted_in = event_graph.get_resulted_in(event_node)
            parents = event_graph.get_parent(event_node)
            caused_by = event_graph.get_caused_by(event_node)
        for i in range(retry_getting_events):
            if len(caused_by)+len(parents)+len(resulted_in) == 0:
                caption = generate_denser_caption(event_node, graph, caption, question, possible_answers,
                    denser_caption_prompt, video_file_name, i)
                graph = generate_denser_graph(event_node, graph, caption, question, possible_answers,
                    denser_graph_prompt, i+1)
                event_graph = EventGraph(graph, question, possible_answers)
                event_node = event_graph.find_node(event_name, args={\"agent\": agent, \"item\": item})
                resulted_in = event_graph.get_resulted_in(event_node)
                parents = event_graph.get_parent(event_node)
                caused_by = event_graph.get_caused_by(event_node)
            else: 
                break
        info = {\"event\": event_node,
                \"events resulted in police firing tear gas\": resulted_in,
                \"events containing the police firing tear gas\": parents,
                \"events caused by police firing tear gas\": caused_by
                }
        retry_answering = 3
        for i in range(retry_answering):
            answer = select_answer(question, possible_answers, info, event_graph)
            if \"not sure\" in answer and i < retry_answering - 1:
                info = get_new_info(answer, info, graph, caption)
            else:
                break
        return answer, info, event_graph

    Example Question: how did the man in blue shirt cook the steak? A. Hold with hands B. Put on a grill C. Fry in pan D. Boil in water E. Putting it in the oven
    Python Code:
    def execute_command(graph, caption, question, possible_answers, video_file_name):
        event_graph = EventGraph(graph, caption, video_file_name)
        event_name = \"cook\"
        agent = \"man in blue shirt\"
        item = \"steak\"
        # Get the event node related to the question
        event_node = event_graph.find_node(event_name, args={\"agent\": agent, \"item\": item})
        children = event_graph.get_children(event_node)
        before = event_graph.get_temporal_before(event_node)
        retry_getting_events = 3
        denser_graph_prompt = \"\"\"Read the question and paragraph, and find relations and/or events that are
            related to the man is cooking steak in the paragraph. Use these events to generate a new graph, such
            that the new graph has one of the following for question answering: the events contained by \"cook\",
            focus on what tools techniques and methods is he using, if you find these events, create new event
            nodes for them and add the event relation \"cook\":{\"hierarchical\":[<event>, ...]} for these events;
            the events before the man cooking the steak, focus on the possible preparation he did for the cooking
            , if you find these events, create new events for them and add the event relation <event>:{\"temporal
            \":[\"cook\", ...]}. \"\"\"
        denser_caption_prompt = \"\"\"Watch the video, describe: what happens before the man in blue shirt cooking
            the steak; what is the environment is it like; what is he doing while cooking the steak; what method,
            technique or tool he is using to cook the steak; and everything else that is helpful in answering the
            question.\"\"\"
        if len(children)+len(before) == 0:
            graph = generate_denser_graph(event_node, graph, caption, question, possible_answers,
                denser_graph_prompt, 0)
            event_graph = EventGraph(graph, question, possible_answers)
            event_node = event_graph.find_node(event_name, args={\"agent\": agent, \"item\": item})
            children = event_graph.get_children(event_node)
            before = event_graph.get_temporal_before(event_node)
        for i in range(retry_getting_events):
            if len(children)+len(before) == 0:
                caption = generate_denser_caption(event_node, graph, caption, question, possible_answers,
                    denser_caption_prompt, video_file_name, i)
                graph = generate_denser_graph(event_node, graph, caption, question, possible_answers,
                    denser_graph_prompt, i+1)
                event_graph = EventGraph(graph, question, possible_answers)
                event_node = event_graph.find_node(event_name, args={\"agent\": agent, \"item\": item})
                children = event_graph.get_children(event_node)
                before = event_graph.get_temporal_before(event_node)
            else: 
                break
            
    info = {\"event\": event_node, \"events contained by the man cooking steak\": children, \"events before
         the man cooking steak\": before}
    retry_answering = 3
    for i in range(retry_answering):
        answer = select_answer(question, possible_answers, info, event_graph)
        if \"not sure\" in answer and i < retry_answering - 1:
            info = get_new_info(answer, info, graph, caption)
        else:
            break
    return answer, info, event_graph

    

    Example Question: how does the kid get the ball at the beginning? A. With his hand B. Kicks it C. Run to fetch it D. Looks at the baby E. Happy
    def execute_command(graph, caption, question, possible_answers, video_file_name):
        event_graph = EventGraph(graph, question, possible_answers)
        event_name = \"get\"
        agent = \"kid\"
        item = \"ball\"
        # Get the event node related to the question
        event_node = event_graph.find_node(event_name, args={\"agent\": agent, \"item\": item})
        children = event_graph.get_children(event_node)
        before = event_graph.get_temporal_before(event_node)
        retry_getting_events = 3
        denser_graph_prompt = \"\"\"Read the question and paragraph, and find relations and/or events that are
            related to the kid getting the ball in the paragraph. Use these events to generate a new graph, such
            that the new graph has one of the following for question answering: the events contained by \"get\",
            focus on what actions he is performing in order to get the ball, if you find these events, create new
            event nodes for them and add the event relation \"get\":{\"hierarchical\":[<event>, ...]} for these
            events; the events before the kid getting the ball, focus where is the ball located, what action the
            kid is doing before getting the ball, if you find these events, create new events for them and add the
            event relation <event>:{\"temporal\":[\"get\", ...]}. \"\"\"
        denser_caption_prompt = \"\"\"Watch the video, describe: what happens before the kid getting the the ball;
            where is the ball located; what is the kid doing while getting the ball; what action is the kid doing
            to get the ball; and everything else that is helpful in answering the question.\"\"\"
        if len(children) + len(before) == 0:
            graph = generate_denser_graph(event_node, graph, caption, question, possible_answers,
                denser_graph_prompt, 0)
            event_graph = EventGraph(graph, question, possible_answers)
            event_node = event_graph.find_node(event_name, args={\"agent\": agent})
            children = event_graph.get_children(event_node)
            before = event_graph.get_temporal_before(event_node)
        for i in range(retry_getting_events):
            if len(children) + len(before) == 0:
                caption = generate_denser_caption(event_node, graph, caption, question, possible_answers,
                    denser_caption_prompt, video_file_name, i)
                graph = generate_denser_graph(event_node, graph, caption, question, possible_answers,
                    denser_graph_prompt, i+1)
                event_graph = EventGraph(graph, question, possible_answers)
                event_node = event_graph.find_node(event_name, args={\"agent\": agent})
                children = event_graph.get_children(event_node)
                before = event_graph.get_temporal_before(event_node)
            else: break

        info = {\"event\": event_node,
                \"child events of the kid getting the ball\": children,
                \"before the kid getting the ball\": before}
        retry_answering = 3
        for i in range(retry_answering):
            answer = select_answer(question, possible_answers, info, event_graph)
            if \"not sure\" in answer and i < retry_answering - 1:
                info = get_new_info(answer, info, graph, caption)
            else:
                break
        return answer, info, event_graph
    Example Question: what did the hen do after the chicks wandered off? A. Moves the food in her hand B. Eat the corn C. Lay down on the straw D. Flip onto back E. look around

    Python Code:
    def execute_command(graph, caption, question, possible_answers, video_file_name):
        event_graph = EventGraph(graph, question, possible_answers)
        event_name = \"wander\"
        agent = \"chicks\"
        # Get the event node related to the question
        event_node = event_graph.find_node(event_name, args={\"agent\": agent})
        after = event_graph.get_temporal_after(event_node)
        caused_by = event_graph.get_caused_by(event_node)
        retry_getting_events = 3
        denser_graph_prompt = \"\"\"Read the question and paragraph, and find relations and/or events that are related to the chicks wandered off that describe what did the hen do in the paragraph. Use these events to generate a new graph such that the new graph has one of the following for question answering: the events after \"wander\", focus on what was the behavior of the hen, or what did it interact with, if you find these events, create new event nodes for them and add the event relation \"wander\":{\"temporal\":[<event>, ...]} for these events; the events caused by \"wander\", focus on what caused the hen did due to the chicks wandered off, what was its reaction to the chicks, if you find these events, create new events for them and add the event relation \"wander\":{\"causal\":[<event>, ...]}. \"\"\" denser_caption_prompt = \"\"\"Watch the video, describe: what happened to the hen after the chicks wandered off; what was the hen’s behavior after the chicks wandered off; the chicks wandered off caused the hen to do what; and everything else that is helpful in answering the question.\"\"\"

        if len(after)+len(caused_by) == 0:
            graph = generate_denser_graph(event_node, graph, caption, question, possible_answers,
                denser_graph_prompt, 0)
            event_graph = EventGraph(graph, question, possible_answers)
            event_node = event_graph.find_node(event_name, args={\"agent\": agent})
            after = event_graph.get_temporal_after(event_node)
            caused_by = event_graph.get_caused_by(event_node)
        for i in range(retry_getting_events):
            if len(after)+len(caused_by) == 0:
                caption = generate_denser_caption(event_node, graph, caption, question, possible_answers,
                    denser_caption_prompt, video_file_name, i)
                graph = generate_denser_graph(event_node, graph, caption, question, possible_answers,
                    denser_graph_prompt, i+1)
                event_graph = EventGraph(graph, question, possible_answers)
                event_node = event_graph.find_node(event_name, args={\"agent\": agent})
                after = event_graph.get_temporal_after(event_node)
                caused_by = event_graph.get_caused_by(event_node)
            else: break
        
        info = {\"event\": event_node, \"events after the chicks wandered off\": after, \"events caused by the chicks wandered off\": caused_by}
        retry_answering = 3
        for i in range(retry_answering):
            answer = select_answer(question, possible_answers, info, event_graph)
            if \"not sure\" in answer and i < retry_answering - 1:
                info = get_new_info(answer, info, graph, caption)
            else:
                break
        return answer, info, event_graph
    For the provided question and graph below, please generate python code to solve it. When you are looking for events by name, make sure to specify the exact name, include the indicies if they are present in the graph(i.e.Run_0, Eat_1). Only generate the execute_command method, do not generate anything else.
''' 

dense_graph_prompt= '''

 input_text = f"{graph_prompt}\n Paragraph: {caption} \n Graph: {original_graph} \n You need to gennerate a
          new graph based on the original graph that has additional events and/or relations that addresses the
         following concern: {request}. The new graph will be used to answer the following question Question: {
         question}? {choices} \n Response: \n Events: \n" where graph prompt is the prompt for graph generator

'''

denser_caption_prompter = '''

You will be given a video and a request. The request is made to ask for specific details the provided
     description is missing. You need to generate a new description that addresses the requested details. \n In
      your description, indicate temporal, causal, or hierarchical relations of events clearly using keywords
     such as \"at the same time\", \"mean while\", \"after\", \"causing\", \"due to\", etc.\n When referring to
      entities, always use descriptive keywords representing their characteristics, such as \"white Honda Civic
     \", \"woman in purple dress\", \"man in black suit\", \"chair on the left and chair on the right\", etc.
     Make sure the references to the entities are consistent, for example, if you mentioned a \"black car with
     broken window\", refer to it with the same name (\"black car with broken window\") everywhere else you
     mention it. When making the description, do not answer the question.\n Now, generate a new text addressing
      the concerns stated in the request: {request}:

'''

event_simple_query_prompt = '''

[
{"role": "system", "content": "You will be given a description to an event and a simple question.
     Answer the question with \"yes\" or \"no\" based on the information provided. Do not generate
     anything else besides \"yes\" or \"no\"."},
{"role": "user", "content": f"Event: {self.description}.\n Question: {query}. Answer the question with
      \"yes\" or \"no\" only.\n Your answer:\n"}
]

'''

reasoner_prompt = '''

[{"role": "system",
             "content": "You will be given a set of information describing events in a video and a multiple
choice question. You need to answer the question with the information from the paragraph.
      Chose one and only one of the answer from the five choices by returning the corresponding
      letter from A-E. You must choose one as your final answer, or make an educated guess. If the
      information provided is insufficient to answer the question, you must: First, guess an answer
       by choosing one of the choices from A, B, C, D, or E. Then, indicate you are not sure by
      saying \"I am not sure\". Finally, explain what additional information you need, and explain
      what details or events you will focus on to obtain the information if you are watching the
      video. Only say you are not sure when the events do not mention what is being asked."},
{"role":"user",
 "content":[
    {"type":"text",
      "text": user_input}
]}]


'''

get_additional_info_prompt = '''


You will be given a video, a question, and a textual request generated by a language model asking for
     additional information to answer the question. You should watch the video, read the question and the
     request, then generate a textual description of the video focusing on what is being asked in the request.
     You should not try to determine if it answered correctly, nor answer the question directly. You should
     generate information addressing what the request is asking for, additionally you can also generate
     information helpful for answering the question. \n Question: {question} \n Choices: {choices} \n Request:
     {concern}. \n Your response: ’

'''

reasoning_with_MM_graph_prompt = '''

You will be given a set of multimodal information as a multimodal graph, a question, and a set of choices. You
      need to answer the question with the multimodal graph by selecting from one of the choices, represented
     by one letter. Your answer must contain a single letter only without any additional text. \n Question: {
     question} Choices: {choices}
'''
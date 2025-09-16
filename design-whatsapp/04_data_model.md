# Data model:

1. Entities:

- User: Represents whatsapp users
- Messages: Represents messages sent by users
- Conversations: Represents each conversation that a user is part of
- Conversation Participants: Represents the participants of conversations - example: muliple users can be part of
a single conversation incase it's a group


2. Relationships:

- User sends messages
- Messages are a part of conversations
- Users are participants in conversations


3. ER Diagram:

    ![alt text](er_model.png)
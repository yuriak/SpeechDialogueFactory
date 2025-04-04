from pydantic import BaseModel, Field
from typing import List, Literal, Optional, Dict, Any
import json
import pickle
from data.common import DataClassModel
from data.evaluation import ConsistencyEvaluation


class DialogueScenario(DataClassModel):
    """Dialogue scenario model representing the high-level parameters for dialogue generation."""

    dialogue_type: str = Field(
        ...,
        description="Type or purpose of the dialogue, such as 'interview', 'debate', 'negotiation', etc.",
    )
    temporal_context: str = Field(
        ...,
        description="Temporal background, such as '21st century', 'modern day', 'information age', etc.",
    )
    spatial_context: str = Field(
        ...,
        description="Spatial or geographical background, such as 'urban', 'corporate', 'academic', etc.",
    )
    cultural_background: str = Field(
        ...,
        description="Cultural background, such as 'Western', 'Eastern', 'Global', etc.",
    )
    dialogue_language: str = Field(
        default="English",
        description="The language to be used in the dialogue, either 'English' or 'Chinese'",
    )
    custom_prompt: Optional[str] = Field(
        default="",
        description="User-defined prompt to provide additional guidance or constraints",
    )

    model_config = {"json_schema_extra": {"exclude": ["language", "custom_prompt"]}}


class Setting(DataClassModel):
    location: str = Field(
        ..., description="Physical location where the conversation takes place"
    )
    time_of_day: str = Field(
        ..., description="Time of day when the conversation occurs"
    )
    context: str = Field(
        ..., description="Brief description of the situational context"
    )
    atmosphere: str = Field(..., description="Mood or feeling of the environment")


class Role(DataClassModel):
    name: str = Field(..., description="Full name of the speaker")
    gender: str = Field(..., description="Gender of the speaker")
    age: int = Field(..., description="Age of the speaker")
    occupation: str = Field(..., description="Current occupation or role")
    nationality: str = Field(..., description="The nationality of the speaker")
    personality_traits: List[str] = Field(
        ...,
        description="List of key personality traits that define the speaker",
    )
    relationship_context: str = Field(
        ..., description="Speaker's relationship or role in the current context"
    )
    self_introduction: str = Field(
        ...,
        description="Detailed description of the speaker's characteristics and background",
    )


class ConversationContext(DataClassModel):
    type: str = Field(..., description="Type or category of the conversation")
    main_topic: str = Field(
        ..., description="Primary topic or purpose of the conversation"
    )
    relationship_dynamic: str = Field(
        ..., description="Nature of relationship between the speakers"
    )
    emotional_tone: str = Field(
        ..., description="Overall emotional tone of the conversation"
    )
    expected_duration: str = Field(
        ..., description="Expected length of the conversation"
    )
    expected_turns: int = Field(
        ..., description="Expected number of conversation turns"
    )
    key_points: List[str] = Field(
        ...,
        description="List of key points or events expected in the conversation",
    )


class Metadata(DataClassModel):
    setting: Setting = Field(..., description="Details about the conversation setting")
    role_1: Role = Field(..., description="Details about the first speaker")
    role_2: Role = Field(..., description="Details about the second speaker")
    conversation_context: ConversationContext = Field(
        ..., description="Details about the conversation context and structure"
    )


class ConversationTurn(DataClassModel):
    speaker_id: str = Field(
        ..., description="Identifier for the speaker (role_1 or role_2)"
    )
    speaker_name: str = Field(..., description="Name of the speaker")
    text: str = Field(..., description="The actual dialogue text")
    emotion: str = Field(
        ..., description="Emotional state of the speaker during this turn"
    )
    speech_rate: str = Field(..., description="Rate of speech for this turn")
    pause_after: str = Field(..., description="Length of pause after this turn")
    tts_prompt: str = Field(
        ...,
        description="Concise natural language prompt describing how the text should be spoken by a TTS model",
    )


class Conversation(DataClassModel):
    utterances: List[ConversationTurn] = Field(
        ..., description="List of conversation utterances (turns)"
    )


class Dialogue(DataClassModel):
    """Complete dialogue package with metadata and conversation."""

    scenario: Optional[DialogueScenario] = Field(
        default=None, description="High-level parameters for dialogue generation"
    )
    metadata: Optional[Metadata] = Field(
        default=None, description="Complete metadata for the dialogue"
    )
    script: Optional[str] = Field(
        default=None, description="Script outline for the dialogue"
    )
    conversation: Optional[List[ConversationTurn]] = Field(
        default=None, description="The actual conversation turns"
    )
    consistency_evaluation: Optional[ConsistencyEvaluation] = Field(
        default=None, description="Evaluation results of the dialogue consistency"
    )

    def save_to_json(self, file_path: str, pretty: bool = True) -> None:
        """Save the Dialogue to a JSON file.

        Args:
            file_path: Path to save the JSON file.
            pretty: If True, format the JSON with indentation for readability.
        """
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(self.to_json(pretty=pretty))

    @classmethod
    def load_from_json(cls, file_path: str) -> "Dialogue":
        """Load a Dialogue from a JSON file.

        Args:
            file_path: Path to the JSON file.

        Returns:
            A new Dialogue instance.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            return cls.from_json(f.read())

    def save_to_pickle(self, file_path: str) -> None:
        """Save the Dialogue to a pickle file.

        Args:
            file_path: Path to save the pickle file.
        """
        with open(file_path, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load_from_pickle(cls, file_path: str) -> "Dialogue":
        """Load a Dialogue from a pickle file.

        Args:
            file_path: Path to the pickle file.

        Returns:
            A new Dialogue instance.
        """
        with open(file_path, "rb") as f:
            return pickle.load(f)

    @classmethod
    def save_batch_to_pickle(cls, dialogues: List["Dialogue"], file_path: str) -> None:
        """Save a batch of Dialogues to a pickle file.

        Args:
            dialogues: List of Dialogue instances to save.
            file_path: Path to save the pickle file.
        """
        with open(file_path, "wb") as f:
            pickle.dump(dialogues, f)

    @classmethod
    def load_batch_from_pickle(cls, file_path: str) -> List["Dialogue"]:
        """Load a batch of Dialogues from a pickle file.

        Args:
            file_path: Path to the pickle file.

        Returns:
            List of Dialogue instances.
        """
        with open(file_path, "rb") as f:
            return pickle.load(f)

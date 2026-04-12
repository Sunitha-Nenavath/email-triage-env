# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""Email Env Environment Client."""

from typing import Dict

from openenv.core import EnvClient
from openenv.core.client_types import StepResult
from openenv.core.env_server.types import State

from .models import EmailAction, EmailObservation, EmailDetails


class EmailEnv(
    EnvClient[EmailAction, EmailObservation, State]
):
    """
    Client for the Email Env Environment.

    This client maintains a persistent WebSocket connection to the environment server,
    enabling efficient multi-step interactions with lower latency.
    Each client instance has its own dedicated environment session on the server.

    Example:
        >>> # Connect to a running server
        >>> with EmailEnv(base_url="http://localhost:8000") as client:
        ...     result = client.reset()
        ...     print(result.observation.echoed_message)
        ...
        ...     result = client.step(EmailAction(message="Hello!"))
        ...     print(result.observation.echoed_message)

    Example with Docker:
        >>> # Automatically start container and connect
        >>> client = EmailEnv.from_docker_image("email_env-env:latest")
        >>> try:
        ...     result = client.reset()
        ...     result = client.step(EmailAction(message="Test"))
        ... finally:
        ...     client.close()
    """

    def _step_payload(self, action: EmailAction) -> Dict:
        """
        Convert EmailAction to JSON payload for step message.

        Args:
            action: EmailAction instance

        Returns:
            Dictionary representation suitable for JSON encoding
        """
        return action.model_dump()

    def _parse_result(self, payload: Dict) -> StepResult[EmailObservation]:
        """
        Parse server response into StepResult[EmailObservation].

        Args:
            payload: JSON response data from server

        Returns:
            StepResult with EmailObservation
        """
        obs_data = payload.get("observation", {})
        
        # Correctly reconstruct nested models
        email_data = obs_data.get("email", {})
        observation = EmailObservation(
            task_id=obs_data.get("task_id", ""),
            email=EmailDetails(
                subject=email_data.get("subject", ""),
                email_text=email_data.get("email_text", ""),
                sender=email_data.get("sender", "")
            )
        )

        return StepResult(
            observation=observation,
            reward=payload.get("reward"),
            done=payload.get("done", False),
        )

    def _parse_state(self, payload: Dict) -> State:
        """
        Parse server response into State object.

        Args:
            payload: JSON response from state request

        Returns:
            State object with episode_id and step_count
        """
        return State(
            episode_id=payload.get("episode_id"),
            step_count=payload.get("step_count", 0),
        )

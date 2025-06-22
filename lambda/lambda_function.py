# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, API calls, and more.
# This sample is built using the handler classes approach in skill builder.

import logging
import os
import requests
import json
import ask_sdk_core.utils as ask_utils

from dotenv import load_dotenv
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Load your Google API Key from an environment variable for security
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# The model to use. As of now, 'gemini-1.5-flash-latest' is the correct name.
# "gemini 2.5 flash" is not a valid model endpoint.
GEMINI_MODEL = "gemini-2.0-flash-latest"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GOOGLE_API_KEY}"

# --- Helper Function for API Call ---

def get_gemini_response(history):
    """
    Sends the conversation history to the Gemini API and gets a response.
    Returns the response text or an error message.
    """
    if not GOOGLE_API_KEY:
        logger.error("GOOGLE_API_KEY is not set.")
        return "API key is not configured. Please check the skill's setup."

    headers = {'Content-Type': 'application/json'}
    payload = {"contents": history}

    try:
        response = requests.post(GEMINI_API_URL, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        response_data = response.json()
        # Safely extract the text from the response
        text = (response_data.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text", "I could not find an answer to that."))
        return text
    except requests.exceptions.RequestException as e:
        logger.error(f"Error calling Gemini API: {e}")
        return "There was an error connecting to the AI service."
    except (KeyError, IndexError) as e:
        logger.error(f"Error parsing Gemini API response: {e}")
        logger.error(f"Full response: {response.json()}")
        return "I received an unusual response. Please try again."


# --- Intent Handlers ---

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes

        # This is the initial "system prompt" to set the context for the AI.
        system_prompt = "You are my AI assistant. I will give you commands, and we will interact as I guide and train you."
        
        # Start the conversation history for this session
        history = [
            {"role": "user", "parts": [{"text": system_prompt}]}
        ]
        
        initial_response_text = get_gemini_response(history)
        
        # Add the model's first response to the history
        history.append({"role": "model", "parts": [{"text": initial_response_text}]})
        
        # Save the history to the session
        session_attr['history'] = history
        
        speak_output = initial_response_text + " How can I help you?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class ChatIntentHandler(AbstractRequestHandler):
    """Handler for Chat Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ChatIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        
        # Get the user's query from the slot
        query = handler_input.request_envelope.request.intent.slots["query"].value
        
        # Retrieve the conversation history from the session, or start fresh if it's missing
        history = session_attr.get('history', [])
        
        # Add the user's new query to the history
        history.append({"role": "user", "parts": [{"text": query}]})
        
        # Get the response from Gemini
        response_text = get_gemini_response(history)
        
        # Add the model's response to the history
        history.append({"role": "model", "parts": [{"text": response_text}]})
        
        # Save the updated history back to the session
        session_attr['history'] = history
        
        speak_output = response_text
        reprompt_text = "Do you have another question?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """
    Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.

sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(ChatIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
# Make sure the exception handler is last
sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()

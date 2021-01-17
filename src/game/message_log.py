from typing import Iterable, List, Reversible, Tuple


import ui.color


class Message:
	def __init__(self, text: str, color: str):
		self.plain_text = text
		self.color = color
		self.count = 1

	@property
	def full_text(self) -> str:
		"""The full text of this message, including the count if necessary."""
		if self.count > 1:
			return f"{self.plain_text} (x{self.count})"
		return self.plain_text



class MessageLog:
	def __init__(self) -> None:
		self.messages: List[Message] = []


	def add_message(self, text: str, color: str = ui.color.default_fg, *, stack: bool = True,
	) -> None:
		"""Add a message to this log.
		If `stack` is True then the message can stack with a previous message of the same text.
		"""
		if stack and self.messages and text == self.messages[-1].plain_text:
			self.messages[-1].count += 1
		else:
			self.messages.append(Message(text, color))

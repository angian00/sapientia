from __future__ import annotations

from typing import List, Dict


class SiteData:
	"""
	A generic object to site matadata.
	"""
	
	def __init__(
		self,
		name: str,
		size: str,
	):
		self.name = name
		self.size = size
		self.staff: List[Dict[str, str]] = []

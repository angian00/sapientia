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
		faction: str,
	):
		self.name = name
		self.size = size
		self.faction = faction
		self.staff: List[Dict[str, str]] = []

from typing import List, Dict
from .constants import PROGRAM_ID_MAP

class PlatformDetector:
    @staticmethod
    def detect_platforms(instructions: List[Dict], inner: List[Dict]) -> List[str]:
        platforms = set()
        for instr in instructions:
            pid = instr.get("programId")
            if pid in PROGRAM_ID_MAP:
                platforms.add(PROGRAM_ID_MAP[pid])
        for ix in inner:
            for instr in ix.get("instructions", []):
                pid = instr.get("programId")
                if pid in PROGRAM_ID_MAP:
                    platforms.add(PROGRAM_ID_MAP[pid])
        return list(platforms)

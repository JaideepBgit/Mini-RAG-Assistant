import os
import json
import hashlib
from typing import List
from pathlib import Path

class DocumentAutoLoader:
    def __init__(self, docs_folder: str = "docs", metadata_file: str = "vector_store/processed_files.json"):
        self.docs_folder = docs_folder
        self.metadata_file = metadata_file
        self.processed_files = self._load_metadata()
        os.makedirs(docs_folder, exist_ok=True)
    
    def _load_metadata(self) -> dict:
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_metadata(self):
        os.makedirs(os.path.dirname(self.metadata_file), exist_ok=True)
        with open(self.metadata_file, 'w') as f:
            json.dump(self.processed_files, f, indent=2)
    
    def _get_file_hash(self, filepath: str) -> str:
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    
    def get_unprocessed_files(self) -> List[str]:
        unprocessed = []
        for ext in ['*.txt', '*.pdf']:
            for filepath in Path(self.docs_folder).glob(ext):
                filepath_str = str(filepath)
                file_hash = self._get_file_hash(filepath_str)
                if filepath_str not in self.processed_files or \
                   self.processed_files[filepath_str] != file_hash:
                    unprocessed.append(filepath_str)
        return unprocessed
    
    def mark_as_processed(self, filepaths: List[str]):
        for filepath in filepaths:
            if os.path.exists(filepath):
                self.processed_files[filepath] = self._get_file_hash(filepath)
        self._save_metadata()
    
    def get_all_docs_files(self) -> List[str]:
        all_files = []
        for ext in ['*.txt', '*.pdf']:
            all_files.extend([str(f) for f in Path(self.docs_folder).glob(ext)])
        return all_files


from typing import List

class Film:
    def __init__(self, name: str, author: str, year: int, genre: List[str], key_words: List[str]):
        self.name = name
        self.author = author
        self.year = year
        self.genre = genre
        self.key_words = key_words

    def __str__(self) -> str:
        return f"{self.name} by {self.author} ({self.year}) - {self.genre}"

    def __repr__(self) -> str:
        return f"Film(name='{self.name}', author='{self.author}', year={self.year}, genre='{self.genre}')"

    def metric(self, other: 'Film') -> float:
        """
        Calculate similarity metric between two films.
        Returns a score from 0 to 100.
        """
        if not isinstance(other, Film):
            raise TypeError("Can only compare with another Film object")
        
        points = 0.0
        
        # Author similarity (20 points)
        if self.author == other.author:
            points += 20
        
        # Genre similarity (20 points)
        if self.genre and other.genre:
            matching_genres = set(self.genre) & set(other.genre)
            shorter_length = min(len(self.genre), len(other.genre))
            points += len(matching_genres) * 20 / shorter_length
        
        # Year similarity (10 points for films within 10 years)
        if abs(self.year - other.year) < 10:
            points += 10
        
        # Keyword similarity (50 points based on overlap)
        if self.key_words and other.key_words:
            # Use set intersection for O(n+m) performance instead of O(n*m)
            matching_keywords = set(self.key_words) & set(other.key_words)
            shorter_length = min(len(self.key_words), len(other.key_words))
            
            if shorter_length > 0:
                keyword_score = len(matching_keywords) / shorter_length * 50
                points += keyword_score
        
        return points

    def get_common_keywords(self, other: 'Film') -> List[str]:
        """Get keywords that are common between two films."""
        if not isinstance(other, Film):
            raise TypeError("Can only compare with another Film object")
        
        return list(set(self.key_words) & set(other.key_words))

    def similarity_percentage(self, other: 'Film') -> float:
        """Get similarity as a percentage (0-100)."""
        return self.metric(other)

    def is_similar(self, other: 'Film', threshold: float = 50.0) -> bool:
        """Check if two films are similar based on a threshold."""
        return self.metric(other) >= threshold

from schemas.movie import Movie

MOVIE_LIST = [
    Movie(
        slug="shawshank",
        title="The Shawshank Redemption",
        description="A banker convicted of uxoricide forms a friendship over a quarter century with a hardened convict,\n"
        " while maintaining his innocence and trying to remain hopeful through simple compassion.",
        year=1994,
    ),
    Movie(
        slug="godfather",
        title="The Godfather",
        description="The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
        year=1972,
    ),
    Movie(
        slug="batman",
        title="The Dark Knight",
        description="When a menace known as the Joker wreaks havoc and chaos on the people of Gotham,\n"
        " Batman, James Gordon and Harvey Dent must work together to put an end to the madness.",
        year=2008,
    ),
]

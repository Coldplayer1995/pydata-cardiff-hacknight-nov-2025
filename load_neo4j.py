"""Load Simpsons data into Neo4j for graph visualization

Usage:
    python load_neo4j.py

Make sure Neo4j is running and update the connection details below.
Default Neo4j Desktop: bolt://localhost:7687, user: neo4j
"""
import polars as pl
from neo4j import GraphDatabase
from daveparr import joinar


class Neo4jLoader:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self.driver.close()
    
    def clear_database(self):
        """Clear all nodes and relationships"""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            print("Database cleared.")
    
    def create_characters(self, characters_df):
        """Create Character nodes"""
        with self.driver.session() as session:
            query = """
            UNWIND $characters AS char
            CREATE (c:Character {
                id: char.id,
                name: char.name,
                normalized_name: char.normalized_name,
                gender: char.gender
            })
            """
            result = session.run(query, characters=characters_df.to_dicts())
            summary = result.consume()
            print(f"Created {summary.counters.nodes_created} Character nodes")
    
    def create_episodes(self, episodes_df):
        """Create Episode nodes"""
        with self.driver.session() as session:
            query = """
            UNWIND $episodes AS ep
            CREATE (e:Episode {
                id: ep.id,
                title: ep.title,
                season: ep.season,
                number_in_season: ep.number_in_season,
                imdb_rating: ep.imdb_rating,
                imdb_votes: ep.imdb_votes,
                original_air_date: ep.original_air_date,
                original_air_year: ep.original_air_year,
                us_viewers_in_millions: ep.us_viewers_in_millions
            })
            """
            result = session.run(query, episodes=episodes_df.to_dicts())
            summary = result.consume()
            print(f"Created {summary.counters.nodes_created} Episode nodes")
    
    def create_locations(self, locations_df):
        """Create Location nodes"""
        with self.driver.session() as session:
            query = """
            UNWIND $locations AS loc
            CREATE (l:Location {
                id: loc.id,
                name: loc.name,
                normalized_name: loc.normalized_name
            })
            """
            result = session.run(query, locations=locations_df.to_dicts())
            summary = result.consume()
            print(f"Created {summary.counters.nodes_created} Location nodes")
    
    def create_character_episode_relationships(self, script_lines_df):
        """Create SPOKE_IN relationships with aggregated counts"""
        with self.driver.session() as session:
            # Aggregate script lines by character and episode
            aggregated = (
                script_lines_df
                .filter(pl.col("speaking_line") == True)
                .group_by(["character_id", "episode_id"])
                .agg([
                    pl.count().alias("line_count"),
                    pl.sum("word_count").alias("total_words")
                ])
                .filter(pl.col("character_id").is_not_null())
                .to_dicts()
            )
            
            query = """
            UNWIND $data AS rel
            MATCH (c:Character {id: rel.character_id})
            MATCH (e:Episode {id: rel.episode_id})
            CREATE (c)-[:SPOKE_IN {
                line_count: rel.line_count,
                total_words: rel.total_words
            }]->(e)
            """
            result = session.run(query, data=aggregated)
            summary = result.consume()
            print(f"Created {summary.counters.relationships_created} SPOKE_IN relationships")
    
    def create_character_location_relationships(self, script_lines_df):
        """Create SPOKE_AT relationships"""
        with self.driver.session() as session:
            aggregated = (
                script_lines_df
                .filter(pl.col("speaking_line") == True)
                .group_by(["character_id", "location_id"])
                .agg(pl.count().alias("line_count"))
                .filter(
                    pl.col("character_id").is_not_null() &
                    pl.col("location_id").is_not_null()
                )
                .to_dicts()
            )
            
            query = """
            UNWIND $data AS rel
            MATCH (c:Character {id: rel.character_id})
            MATCH (l:Location {id: rel.location_id})
            CREATE (c)-[:SPOKE_AT {
                line_count: rel.line_count
            }]->(l)
            """
            result = session.run(query, data=aggregated)
            summary = result.consume()
            print(f"Created {summary.counters.relationships_created} SPOKE_AT relationships")
    
    def create_episode_location_relationships(self, script_lines_df):
        """Create HAS_LOCATION relationships"""
        with self.driver.session() as session:
            aggregated = (
                script_lines_df
                .group_by(["episode_id", "location_id"])
                .agg(pl.count().alias("scene_count"))
                .filter(pl.col("location_id").is_not_null())
                .to_dicts()
            )
            
            query = """
            UNWIND $data AS rel
            MATCH (e:Episode {id: rel.episode_id})
            MATCH (l:Location {id: rel.location_id})
            CREATE (e)-[:HAS_LOCATION {
                scene_count: rel.scene_count
            }]->(l)
            """
            result = session.run(query, data=aggregated)
            summary = result.consume()
            print(f"Created {summary.counters.relationships_created} HAS_LOCATION relationships")
    
    def create_character_interactions(self, script_lines_df):
        """Create INTERACTS_WITH relationships (characters in same episodes)"""
        with self.driver.session() as session:
            # Get unique character-episode pairs
            char_episodes = (
                script_lines_df
                .filter(pl.col("speaking_line") == True)
                .select(["character_id", "episode_id"])
                .unique()
                .filter(pl.col("character_id").is_not_null())
            )
            
            # Self-join to find co-appearances
            interactions = (
                char_episodes
                .join(
                    char_episodes,
                    on="episode_id",
                    how="inner"
                )
                .filter(pl.col("character_id") != pl.col("character_id_right"))
                .group_by(["character_id", "character_id_right"])
                .agg(pl.count().alias("episode_count"))
                .to_dicts()
            )
            
            query = """
            UNWIND $data AS rel
            MATCH (c1:Character {id: rel.character_id})
            MATCH (c2:Character {id: rel.character_id_right})
            WHERE c1.id < c2.id  // Avoid duplicate relationships
            MERGE (c1)-[r:INTERACTS_WITH]->(c2)
            SET r.episode_count = rel.episode_count
            """
            result = session.run(query, data=interactions)
            summary = result.consume()
            print(f"Created/updated {summary.counters.relationships_created} INTERACTS_WITH relationships")


def main():
    # Configuration - update these for your Neo4j instance
    NEO4J_URI = "bolt://localhost:7687"
    NEO4J_USER = "neo4j"
    NEO4J_PASSWORD = "password"  # Change this to your Neo4j password
    
    # Main characters to include
    main_character_names = [
        "Homer Simpson",
        "Marge Simpson", 
        "Bart Simpson",
        "Lisa Simpson",
        "Maggie Simpson",
        "Ned Flanders",
        "Moe Szyslak",
        "Principal Skinner",
        "Mr. Burns",
        "Apu Nahasapeemapetilon",
        "Milhouse Van Houten",
        "Krusty the Clown",
        "Barney Gumble",
        "Chief Wiggum",
        "Comic Book Guy",
        "Lenny Leonard",
        "Carl Carlson",
        "Sideshow Bob",
        "Ralph Wiggum",
        "Nelson Muntz"
    ]
    
    # Load data
    print("Loading data from CSV files...")
    all_characters = pl.read_csv("data/raw/simpsons_characters.csv")
    episodes = pl.read_csv("data/raw/simpsons_episodes.csv")
    locations = pl.read_csv("data/raw/simpsons_locations.csv")
    script_lines = pl.read_csv("data/raw/simpsons_script_lines.csv")
    
    # Filter to main characters
    characters = all_characters.filter(
        pl.col("name").is_in(main_character_names)
    )
    
    # Get main character IDs
    main_character_ids = characters.select("id").to_series().to_list()
    
    # Filter script lines to only those with main characters
    script_lines_filtered = script_lines.filter(
        pl.col("character_id").is_in(main_character_ids) | 
        pl.col("character_id").is_null()  # Keep non-speaking lines for context
    )
    
    print(f"Loaded {len(characters)} main characters, {len(episodes)} episodes, "
          f"{len(locations)} locations, {len(script_lines_filtered)} script lines")
    
    # Connect to Neo4j
    print(f"\nConnecting to Neo4j at {NEO4J_URI}...")
    loader = Neo4jLoader(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    
    try:
        # Verify connection
        with loader.driver.session() as session:
            result = session.run("RETURN 1 as test")
            result.consume()
        print("Connected successfully!\n")
        
        print("Clearing existing data...")
        loader.clear_database()
        
        print("\nCreating nodes...")
        loader.create_characters(characters)
        loader.create_episodes(episodes)
        loader.create_locations(locations)
        
        print("\nCreating relationships...")
        loader.create_character_episode_relationships(script_lines_filtered)
        loader.create_character_location_relationships(script_lines_filtered)
        loader.create_episode_location_relationships(script_lines_filtered)
        loader.create_character_interactions(script_lines_filtered)
        
        print("\n" + "="*50)
        print("Done! Main characters and relationships loaded into Neo4j.")
        print("="*50)
        print("\nYou can now visualize the data in Neo4j Browser at http://localhost:7474")
        print("\nExample queries:")
        print("  MATCH (c:Character)-[r:SPOKE_IN]->(e:Episode)")
        print("  RETURN c.name, sum(r.line_count) as total_lines")
        print("  ORDER BY total_lines DESC")
        print("\n  MATCH (c1:Character)-[r:INTERACTS_WITH]-(c2:Character)")
        print("  RETURN c1, c2, r")
        print("  LIMIT 50")
        print("\n  MATCH (c:Character)-[:SPOKE_IN]->(e:Episode)")
        print("  RETURN c, e")
        print("  LIMIT 100")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        print("\nMake sure:")
        print("  1. Neo4j is running (docker-compose up -d)")
        print("  2. Connection URI, user, and password are correct")
        print("  3. You've updated NEO4J_PASSWORD in the script if needed")
    finally:
        loader.close()


if __name__ == "__main__":
    main()


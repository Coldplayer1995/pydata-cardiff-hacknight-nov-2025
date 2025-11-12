# Running Neo4j with Docker

This project includes a Docker Compose setup to easily run Neo4j for graph visualization.

## Quick Start

1. **Start Neo4j:**
   ```bash
   docker-compose up -d
   ```

2. **Check if Neo4j is running:**
   ```bash
   docker-compose ps
   ```

3. **Access Neo4j Browser:**
   - Open http://localhost:7474 in your browser
   - Login with:
     - Username: `neo4j`
     - Password: `password`

4. **Load the Simpsons data:**
   ```bash
   python load_neo4j.py
   ```

5. **Stop Neo4j:**
   ```bash
   docker-compose down
   ```

## Configuration

The default configuration in `docker-compose.yml`:
- **Ports:**
  - `7474` - Neo4j Browser (HTTP)
  - `7687` - Bolt protocol (for Python driver)
- **Default password:** `password`
- **Memory settings:** 2GB heap, 1GB pagecache

### Changing the Password

To change the Neo4j password:

1. Update `docker-compose.yml`:
   ```yaml
   environment:
     - NEO4J_AUTH=neo4j/your_new_password
   ```

2. Update `load_neo4j.py`:
   ```python
   NEO4J_PASSWORD = "your_new_password"
   ```

3. Restart the container:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

## Data Persistence

Data is stored in Docker volumes:
- `neo4j_data` - Database files
- `neo4j_logs` - Log files
- `neo4j_import` - Import directory
- `neo4j_plugins` - Plugins directory

To completely remove all data:
```bash
docker-compose down -v
```

## Troubleshooting

**Container won't start:**
- Check if ports 7474 or 7687 are already in use
- Check Docker logs: `docker-compose logs neo4j`

**Connection refused:**
- Wait a few seconds after starting - Neo4j takes time to initialize
- Check health status: `docker-compose ps`

**Reset everything:**
```bash
docker-compose down -v
docker-compose up -d
```

## Example Queries

Once data is loaded, try these in Neo4j Browser:

**Top characters by dialogue:**
```cypher
MATCH (c:Character)-[r:SPOKE_IN]->(e:Episode)
RETURN c.name, sum(r.line_count) as total_lines
ORDER BY total_lines DESC
LIMIT 10
```

**Character interaction network:**
```cypher
MATCH (c1:Character)-[r:INTERACTS_WITH]-(c2:Character)
WHERE r.episode_count > 5
RETURN c1, c2, r
LIMIT 50
```

**Episode locations:**
```cypher
MATCH (e:Episode)-[:HAS_LOCATION]->(l:Location)
WHERE e.title CONTAINS "Christmas"
RETURN e, l
```


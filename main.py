import sys
from src.postgres_server import postgres_server
from src.mongo_server import mongo_server
from src.neo4j_server import neo4j_server 

def main():
    # Initialize servers with updated credentials
    try:
        # PostgreSQL connection
        pg_server = postgres_server(
            host="localhost",
            port=5432,
            database="nosql_proj",
            user="abhijay",
            password="abhijay"
        )
        pg_server.connect()

        # MongoDB connection (no auth by default)
        m_server = mongo_server(
            host="localhost",
            port=27017,
            database="nosql_proj"
        )
        m_server.connect()

        # Neo4j connection
        neo_server = neo4j_server(
            uri="bolt://localhost:7687",
            user="neo4j",
            password="abhijay"  # Updated password
        )
        neo_server.connect()

    except Exception as e:
        print(f"Server initialization failed: {e}")
        sys.exit(1)

    try:
        while True:
            # Improved input prompt
            user_input = input("\nCommand format: [action] [server] [arguments]\n"
                             "Actions: query, update, merge, recover\n"
                             "Servers: postgres, mongo, neo4j\n"
                             "Example: 'query postgres subject123'\n"
                             "> ").strip().lower()
            
            if not user_input:
                continue

            command = user_input.split()
            if len(command) == 1 and command[0] in ("exit", "quit"):
                break

            try:
                action, server_name, *args = command
            except ValueError:
                print("Invalid command format. Required: [action] [server] [args]")
                continue

            # Server selection
            servers = {
                "postgres": pg_server,
                "mongo": m_server,
                "neo4j": neo_server
            }

            if server_name not in servers:
                print(f"Invalid server: {server_name}. Choose from: {list(servers.keys())}")
                continue

            server = servers[server_name]

            # Command handling
            if action == "query":
                if len(args) != 1:
                    print("Query requires exactly 1 argument: subject")
                    continue
                
                results = server.query(args[0])
                if not results:
                    print(f"No entries found for subject: {args[0]}")
                    continue
                
                print(f"\n{len(results)} results for '{args[0]}':")
                for idx, (subj, pred, obj, _) in enumerate(results, 1):
                    print(f"{idx}. {subj} → {pred} → {obj}")

            elif action == "update":
                if len(args) != 3:
                    print("Update requires 3 arguments: subject predicate new_value")
                    continue
                
                server.update(*args)
                print(f"Updated {server_name}: {args[0]} {args[1]} → {args[2]}")

            elif action == "merge":
                if len(args) != 1:
                    print("Merge requires 1 argument: target_server")
                    continue
                
                if args[0] not in servers:
                    print(f"Invalid target server: {args[0]}")
                    continue
                
                if args[0] == server_name:
                    print("Cannot merge server with itself")
                    continue
                
                target_server = servers[args[0]]
                server.merge(target_server)
                print(f"Merged data from {server_name} to {args[0]}")

            elif action == "recover":
                server.recover()
                print(f"{server_name} recovery initiated")

            else:
                print(f"Unknown action: {action}. Valid actions: query, update, merge, recover")

    finally:
        # Clean shutdown
        pg_server.disconnect()
        m_server.disconnect()
        neo_server.disconnect()
        print("\nSystem shutdown complete")

if __name__ == "__main__":
    main()

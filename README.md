# Decentralized Multi-Model RDF Storage System

This project demonstrates a scalable, distributed prototype for managing RDF (Resource Description Framework) data across heterogeneous database systems. The framework integrates PostgreSQL, MongoDB, and Neo4j to enable cross-platform synchronization using transaction logs and conflict resolution mechanisms.

## Core Capabilities

- **Data Retrieval**: Fetch RDF-style triples (subject-predicate-object) from configured database nodes
- **Dynamic Updates**: Alter object values associated with specific subject-predicate pairs atomically
- **State Synchronization**: Reconcile distributed states through timestamp-ordered log replay and version control

## Technical Design

The architecture combines relational, document, and graph databases into a cohesive data management ecosystem:

- **Storage Models**:
  - PostgreSQL/MongoDB: Tabular/collection-based triple storage
  - Neo4j: Graph-structured representation with labeled nodes and typed edges
- **Consistency Mechanism**:
  - Transaction journals track local modifications
  - Cross-node synchronization uses hybrid vector clock-logical timestamp resolution
- **Resilience Features**:
  - Log segmentation for parallel recovery
  - State reconstruction via replayable operation sequences

## Development Approach

Built in Python, the system employs database-specific adapters for optimized interactions:

- **Schema Design**:
  - Customized storage layouts for each database type
  - Indexing strategies for SPARQL-like pattern matching
- **Synchronization Protocol**:
  - Bidirectional log exchange between nodes
  - Idempotent operation application with version tagging
- **Interoperability**:
  - Unified API abstraction layer
  - Query translation between SQL, Cypher, and MongoDB DSL

## Validation Process

The verification suite (`yago_test.py`) uses semantic web datasets to evaluate:

- Cross-database insert consistency
- Temporal conflict resolution accuracy
- Distributed state convergence timelines

## Interaction Model

A terminal-based interface enables:

- Unified query execution across storage backends
- Transaction simulation with automatic logging
- On-demand synchronization between database pairs

## Performance Analysis

Benchmarking reveals:

- Sub-second latency for local triple operations
- Linear scaling of merge operations (tested up to 10^6 triples)
- Neo4j outperforms on graph traversal patterns
- PostgreSQL excels in bulk predicate filtering

## Enhancement Roadmap

- Sharded log distribution with consensus protocols
- Merkle-tree based integrity verification
- Hybrid logical-physical timestamp allocation

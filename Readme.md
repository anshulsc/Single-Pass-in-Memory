# SPIMI Indexer Project

## Overview

This project implements the **Single-Pass In-Memory Indexing (SPIMI)** algorithm, which is a method commonly used for efficient index construction in information retrieval systems. The SPIMI algorithm is particularly effective for large-scale text collections due to its efficient handling of memory and disk operations.

The project structure is organized into different modules, each handling specific responsibilities to ensure a clean separation of functionality:

- `src/query`: Handles querying the SPIMI index.
- `src/reuters`: Deals with processing Reuters documents to be indexed.
- `src/spimi`: Implements the core SPIMI indexing algorithm.

Let's dive into each component in detail to understand its function and how it contributes to the overall working of the project.

## Project Structure

```
SPIMI_Indexer_Project/
├── src/
│   ├── query.py
│   ├── reuters.py
│   └── spimi.py
└── main.py
```

### 1. SPIMI Algorithm (`src/spimi.py`)

The **Single-Pass In-Memory Indexing (SPIMI)** algorithm is the core component of this project. SPIMI is designed to create an inverted index by processing each block of documents independently and storing intermediate results on disk. The SPIMI process has several key steps:

1. **Tokenization**: Split documents into individual words or tokens.
2. **In-Memory Index Construction**: Construct a dictionary in memory by adding tokens, along with their document IDs.
3. **Writing to Disk**: Once the memory is filled, the dictionary is sorted and written to disk as an index file.
4. **Merging**: If multiple index files are created due to memory limitations, they are merged at the end.

#### Key Features
- **Efficiency**: The SPIMI algorithm uses a single pass over each block of documents, minimizing the number of passes required compared to multi-pass algorithms.
- **Dynamic Dictionary**: The dictionary size grows dynamically as new tokens are encountered, making efficient use of available memory.
- **Inverted Index**: The output is an inverted index that maps each token to a list of documents where it appears.

#### Code Structure
The core SPIMI indexing function is found in `spimi.py`, and it performs the following operations:

- **Index Creation**: Parses each document, tokenizes it, and adds the token to an in-memory dictionary.
- **Block Write**: When the memory limit is reached, it sorts the in-memory dictionary and writes the index to disk.
- **Merge Blocks**: Once all documents are processed, the index files are merged into a single unified index.

### 2. Reuters Document Processing (`src/reuters.py`)

This module deals with parsing and processing **Reuters news documents**. Reuters provides a rich set of documents that are well-suited for testing indexing algorithms.

#### Key Features
- **Document Parsing**: The module reads the Reuters dataset and parses individual articles.
- **Preprocessing**: Basic text preprocessing is done to normalize the data, such as lowercasing, removing punctuation, and eliminating stop words.

#### Code Structure
- **Document Extraction**: Reads documents from a dataset and splits them based on defined delimiters.
- **Text Normalization**: Performs various preprocessing steps to clean the text before indexing.

### 3. Query Handling (`src/query.py`)

The **query module** is responsible for handling queries against the generated SPIMI index. Users can input search queries to retrieve documents that contain specific tokens or phrases.

#### Key Features
- **Boolean Queries**: Supports simple boolean queries to combine search terms using logical operators like `AND` and `OR`.
- **Inverted Index Lookup**: Uses the inverted index generated by SPIMI to quickly find matching documents.

#### Code Structure
- **Query Parsing**: Parses the user's input to determine the search terms and the type of query (e.g., boolean search).
- **Index Lookup**: Searches the inverted index to retrieve matching document IDs.
- **Result Display**: Displays the retrieved documents to the user.

### 4. Main Script (`main.py`)

The `main.py` script ties all the components together:

1. **Index Creation**: Uses the SPIMI algorithm to index the Reuters documents.
2. **Query Handling**: Once the index is built, users can input queries to search the indexed documents.

## How to Run the Project

To run the project, follow these steps:

1. **Install Dependencies**: Make sure you have Python and the necessary libraries installed.
2. **Index the Documents**:
   ```sh
   python main.py --index
   ```
   This will index the Reuters documents using the SPIMI algorithm and store the inverted index on disk.
3. **Run Queries**:
   ```sh
   python main.py --query "your search query here"
   ```
   This will allow you to input queries and retrieve relevant documents from the indexed data.

## SPIMI Algorithm Explained

The SPIMI algorithm is designed to handle large datasets by splitting them into manageable blocks and building an index for each block in memory. Here's a deeper look into how the algorithm works:

1. **Document Tokenization**: Each document is split into individual tokens. This step is crucial for creating an inverted index, as each token will be indexed.
2. **Adding to Dictionary**: Tokens are added to an in-memory dictionary. If the token already exists, the document ID is appended to its posting list; otherwise, a new entry is created.
3. **Memory Management**: When the memory limit is reached, the in-memory dictionary is sorted, and the block is written to disk. This is done to prevent excessive memory usage.
4. **Merging Index Blocks**: Once all documents are processed, the individual blocks are merged to create a final, unified inverted index.

## Advantages of SPIMI

- **Memory Efficiency**: SPIMI builds the index for one block of documents at a time, avoiding the need to load the entire dataset into memory.
- **Dynamic Dictionary Growth**: The dictionary grows dynamically as new tokens are added, ensuring that memory is used efficiently.
- **Simplified Merging**: Since the index is written to disk in sorted order, merging multiple blocks is a straightforward process.

## Conclusion

The SPIMI Indexer Project demonstrates an efficient way to build an inverted index for a large document collection. By leveraging the SPIMI algorithm, the project is capable of indexing documents with limited memory usage while maintaining high performance. The modular structure ensures that each part of the project can be easily understood and extended, from document parsing to query handling.

Feel free to explore each module and modify the code to experiment with different indexing and query techniques. This project provides a solid foundation for building scalable information retrieval systems.

## Future Improvements
- **Advanced Query Features**: Adding support for more complex query types, such as phrase queries or proximity searches.
- **Performance Optimization**: Optimizing the memory management in the SPIMI implementation to handle even larger datasets more efficiently.
- **User Interface**: Creating a simple web-based interface to allow users to interact with the search engine more easily.

## References
- **Information Retrieval** by Christopher D. Manning, Prabhakar Raghavan, and Hinrich Schütze: This book provides a comprehensive introduction to information retrieval and indexing techniques, including SPIMI.


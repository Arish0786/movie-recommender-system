import gzip
import pickle


def compress_file(input_file, output_file):
    print(f"Compressing {input_file}...")

    # Step 1: Open and read the pickle file
    with open(input_file, 'rb') as f:
        data = pickle.load(f)

    # Step 2: Compress the data using gzip
    with gzip.open(output_file, 'wb') as f:
        pickle.dump(data, f)

    print(f"✅ Done! Compressed file saved as {output_file}")


# Compress the files
compress_file('movies.pkl', 'movies_compressed.pkl.gz')
compress_file('similarity.pkl', 'similarity_compressed.pkl.gz')

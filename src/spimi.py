import os 

from utils.utils import ROOT_DIR

class SPIMI:

    def __init__(self, reuters, term_limit=1000000, example=False):

        self.reuters = reuters

        self.out_dir =  os.path.join(ROOT_DIR, 'output')
        self.block_prefix = 'block_'
        self.block_num = 0
        self.block_suffix = '.txt'

        self.output_index = os.path.join(self.out_dir, f"index{self.block_suffix}")
        self.term_limit = term_limit

        self.mkdir_output_dir(self.out_dir)
        
        if not example:
            self.list_of_lists_of_tokens = self.reuters.get_tokens()

    
    @staticmethod
    def mkdir_output_dir(directory):
        # Clear existing files in the directory
        os.makedirs(directory, exist_ok=True)

        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)

    @staticmethod
    def add_to_dictionary( dictionary, term):
        dictionary[term] = []
        return dictionary[term]
    
    @staticmethod
    def get_postings_list( dictionary, term):
        return dictionary[term]
    
    @staticmethod
    def add_to_postings_list( postings_list, doci_id):

        postings_list.append(doci_id)

    @staticmethod
    def sort_terms( dictionary):
       return [term for term in sorted(dictionary)]
    
    def write_block(self, block_file, terms, dictionary):
        with open(block_file, 'w') as block:
            for term in terms:
                postings_list = dictionary[term]
                postings_list = [str(doc_id) for doc_id in sorted(postings_list)]
                block.write(f"{term} {' '.join(postings_list)}\n")
        return block_file
    

    def merge_blocks(self, block_files):

        block_files = [open(block_file) for block_file in block_files]
        lines = [block_file.readline()[:-1] for block_file in block_files]
        most_recent_term = ""

        index = 0 
        for block_file in block_files:
            if lines[index] == "":
                block_files.pop(index)
                lines.pop(index)
            else:
                index += 1

        
        with open(self.output_index, "w") as output_index:
            while len(block_files) > 0:

                min_index = lines.index(min(lines))
                line = lines[min_index]
                current_term = line.split()[0]
                current_postings = " ".join(map(str, sorted(list(map(int, line.split()[1:])))))

                if current_term != most_recent_term:
                    output_index.write("\n%s %s" % (current_term, current_postings))
                    most_recent_term = current_term
                else:
                    output_index.write(" %s" % current_postings)

                lines[min_index] = block_files[min_index].readline()[:-1]

                if lines[min_index] == "":
                    block_files[min_index].close()
                    block_files.pop(min_index)
                    lines.pop(min_index)

            output_index.close()
        print("Index has been constructed.")

        return self.get_index()
    

    def construct_index(self):

        if os.path.exists(self.output_index):
            return self.get_index()
         
        block_files = []

        for tokens in self.list_of_lists_of_tokens:
            
            dictionary = {}
            for term, doci_id in tokens:
                if term not in dictionary:
                    postings_list = self.add_to_dictionary(dictionary, term)

                else: 
                    postings_list = self.get_postings_list(dictionary, term)
                    
                
                self.add_to_postings_list(postings_list, doci_id)

            self.block_num += 1
            terms = self.sort_terms(dictionary)

            block_file = "/".join([self.out_dir, "".join([self.block_prefix, str(self.block_num), self.block_suffix])])
            block_files.append(self.write_block(block_file, terms, dictionary))

        return self.merge_blocks(block_files)
    

    def get_index(self):
        inverted_index = {}

        index_file = open(self.output_index)
        index_file.readline()

        for line in index_file:
            line = line.split()
            inverted_index[line[0]] = sorted(map(int, (line[1:])))

        return inverted_index
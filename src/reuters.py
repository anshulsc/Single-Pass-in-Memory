import os 
import wget
import tarfile
from bs4 import BeautifulSoup


from utils.utils import ROOT_DIR, word_tokenize, stopwords, ps


class Reuters:

    def __init__(self, num_files=22, docs_per_block=500,
                remove_stopwords=False, stem=False, case_folding=False, remove_numbers=False):
        
        self.reuters_url = "http://www.daviddlewis.com/resources/testcollections/reuters21578/reuters21578.tar.gz"
        self.reuters_dir = os.path.join(ROOT_DIR, 'reuters')

        self.reuters_files = self.__init_reuters_files()[:num_files]
        self.docs_per_block = docs_per_block
        self.num_of_docs = 0
        self.num_of_tokens = 0

        self.remove_stopwords = remove_stopwords
        self.stem = stem
        self.case_folding = case_folding
        self.remove_numbers = remove_numbers

        self.will_compress = self.remove_stopwords or self.stem or self.case_folding or self.remove_numbers

        self.list_of_lists_of_tokens = []

        self.documents_lengths = {}
        self.average_document_length = 0



    
    def get_reuters(self):

        if not os.path.exists(self.reuters_dir):
            print("Downloading Reuters dataset...")
            file = wget.download(self.reuters_url, out=ROOT_DIR)
            print()
            tar = tarfile.open(file)
            tar.extractall(path=self.reuters_dir)
            tar.close()
            os.remove(file)

    
    def __init_reuters_files(self):
        self.get_reuters()
        reuters_files = [os.path.join(self.reuters_dir, file)
                         for file in os.listdir(self.reuters_dir)
                         if file.endswith(".sgm")]

        print(f"Found {len(reuters_files)} Reuters files")
        return sorted(reuters_files)
    

    def get_tokens(self):
        tokens = []
        current_doc = 0
        print("Processing Reuters dataset...")

        for file in self.reuters_files:
            
            soup = BeautifulSoup(open(file, encoding="ISO-8859-1"), "html.parser")
            documents = soup.find_all('reuters')

            for document in documents:
                doc_id = int(document['newid'])

                content = document.find('text').text
                terms = word_tokenize(content)

                if self.will_compress:
                    terms = self.compress(terms)

                token_pairs = [(term, doc_id) for term in terms]
                tokens.extend(token_pairs)
                self.num_of_docs += 1

                self.documents_lengths[doc_id] = len(token_pairs)

                current_doc += 1
                if current_doc == self.docs_per_block:
                    self.num_of_tokens += len(tokens)
                    self.list_of_lists_of_tokens.append(tokens)
                    tokens = []
                    current_doc = 0

                if tokens:
                    self.num_of_tokens += len(tokens)
                    self.list_of_lists_of_tokens.append(tokens)

                self.average_document_length = self.num_of_tokens / self.num_of_docs
                print(f"Found {self.num_of_docs}  documents and {self.num_of_docs} tokens. {len(self.list_of_lists_of_tokens)} block files(s) will be generated")

            return self.list_of_lists_of_tokens



    def compress(self, terms):

            if self.remove_stopwords:
                terms = [term for term in terms if term.lower() not in stopwords]

            if self.stem:
                terms = [ps.stem(term) for term in terms]

            if self.case_folding:
                terms = [term.casefold() for term in terms]

            if self.remove_numbers:
                terms = [term for term in terms if not term.replace(",", "").replace(".", "").isdigit()]
            return terms


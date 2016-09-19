from utils.data_loader import loadDocuments
from model.embedding_layer import EmbeddingLayer

def test():
    documentsList = loadDocuments()
    embeddingLayer = EmbeddingLayer(documentsList[:5])
    print embeddingLayer.out

test()
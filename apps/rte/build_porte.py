# coding=UTF-8

"""
Build PORTE
================

Script para criação e serialização do classifier RTE em Português.
"""
import porte

if __name__ == "__main__":
    root = "/Users/phillipe/Projects/storyline/apps/rte/corpus_pt"
    c = porte.RTEClassifier(root)   
    c.serialize()
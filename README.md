Review of Related Work and Search Engine Design
The practical aspect of this module is to go through the process of research, design and implement a search engine of your own. You will work within a group of 3-4 members throughout the project. For exceptional reasons, the group can be changed after discussed with and approved by the MO.

The aim of the assignments is to help you fully understand how a search engine is built. For this purpose, you are asked to design and implement a search engine and evaluate it with experiments. You can make use of the platforms we introduce in the lab, or you can use any other existing tool. You may also want to build everything from scratch.

There are no restriction in terms of tools, programming languages and application/domains. A search engine interface is not compulsory, while you may want consider interface components useful for your specific focus, like query recommendation, user feedback functions, etc.


In this assignment, you are expected to submit a report of no more than 8 pages, to describe your review of the related papers in the field, and the design of a search engine you would like to build. In the report, the following information can be included (but are not limited to):

Review of related work: report your reading, research, exploration of the literature, and discuss your finding, your remarks, identified gaps that motivate you in your design (30%)
Aim, task and dataset - describe a scenario that you will be investigating, such a particular type of retrieval, using a particular type of documents, etc. Description of how models will be evaluated. (20%)
A general architecture of the search engine, showing its components/modules, and how they relate to each others. (20%)
Retrieval model(s) you will be using. (10%)
The tool(s) you will be using to build the search engine. (10%)
Teamwork - Who in your group will be responsible for what. (5%)
The time plan for the building of the search engine. (5%)
All the above need to be justified. The mark distribution can be considered as a general guidance. Your report should be submitted via QMPlus in Word or PDF format..
For the review of related work, a starting list of references are provided below for you to choose from. You can also expand your reading and choose a related, more recent research paper online.

Term-weighting approaches in automatic text retrieval (G. Salton and C. Buckley, IP&M, 1988)
Indexing by latent semantic analysis (S. Deerwester, S. T. Dumais, G. W. Furnas, T. K. Landauer, and R. Harshman, JASIS, 1990)
Inference networks for document retrieval (H.R. Turtle, and B. Croft, .SIGIR 1990)
Towards an information logic (C. J. van Rijsbergen, SIGIR, 1989)
Okapi at TREC-3 (S. E. Robertson, S. Walker, M. M. Hancock-Beaulieu, and M. Gatford, TREC-3, 1994)
Pivoted document length normalization (A. Singhal, C. Buckley, and M. Mitra, SIGIR, 1996)
Self-indexing inverted files for fast text retrieval (A. Moffat and J. Zobel, ACM TOIS, 1996)
Advantages of query biased summaries in information retrieval (A. Tombros and M. Sanderson, SIGIR, 1998)
A language modelling approach to information retrieval (Ponte and Croft, SIGIR, 1998)
The anatomy of a large-scale hypertextual web search engine (Brin and Page, WWW7, 1998)
A study of smoothing methods for language models applied to ad hoc information retrieval (C. Zhai and J. Lafferty, SIGIR, 2001)
Combining document representations for known-item search (P. Ogilvie, and J. Callan, SIGIR, 2003)
Stuff I've seen: A system for personal information retrieval and re-use (S. Dumais, E. Cutell, J. Cadiz, G. Jancke, R. Sarin, and D. Robbins, SIGIR, 2003)
Parsimonious language models for information retrieval, (Hiemstra etal, SIGIR 2004)
A General Matrix Framework for Modelling Information Retrieval (T. Roelleke, T. Tsikrika, and G. Kazai, IP&M, 2006)
Harmony Assumptions in Information Retrieval and Social Networks (T. Roelleke etal, Computer Journal 2015)
Simple BM25 extension to multiple weighted fields (S. Robertson, H. Zaragoza, and M. Taylor, CIKM, 2004)
A general matrix framework for modelling information retrieval (T. Roelleke,T. Tsikrika, and G. Kazai, IP&M, 2006)
A formal study of information retrieval heuristics (H. Fang, T. Tao, and C. Zhai, SIGIR, 2004)
Context modeling and discovery using vector space bases (M. Melucci, CIKM 2005)
Benchmarking declarative approximate selection predicates (Amit Chandel, Oktie Hassanzadeh, Nick Koudas, Mohammad Sadoghi and Divesh Srivastava, SIGMOD Conference 2007)
An Exploration of Axiomatic Approaches to Information Retrieval (Hui Fang and ChengXiang Zhai, SIGIR 2005)
On event space and rank equivalence between probabilistic retrieval models (Robert W. Luk, IR Journal 2008)
The review section should answer the following questions about the works:

the problem being addressed
how it is being addressed
what are the results
what are your views
Note that it may be necessary to read additional papers to be able to have a better and more complete idea/knowledge of the research in your selected paper.
General Comments:

Here are some general comments regarding the search engine design coursework based on previous years' submissions, which I believe will be of benefit to everybody. Some of the comments are valid with respect to other modules, whereas others are specific to this module. Feel free to discuss with us any of the comments, if they are not clear.

Make sure that you cite properly anything that is not from you. For example, when listing the advantages of a given retrieval model, if the list is NOT YOURS, BUT TAKEN FROM SOMETHING YOU HAVE READ, YOU HAVE TO REFERENCE THIS. Otherwise this can be considered as plagiarism.
Some of the writing was not great. If you are not the best writer in English, at least ensure that your sentences are short. A sentence that spans over several lines is not going to help you expressing a clear and understandable message.
Also avoid any informal terms, e.g. thing, nick name
Do not confuse file and document. You are doing document retrieval and not file retrieval. A document may be an ASCII file, a PDF document, etc.
When tf and idf are calculated, this is done at indexing time, and not with respect to a given query. The values of tf and idf remain constant for any query.
Some listed the characteristics of the tools they will be using, e.g. Lucene. Just list what you are actually going to use, and nothing else. It should be made clear what are these features, why you are listing them. Just listing them is not acceptable.
Any tool that you are using, you should have a clear references, which could be a book, a paper, or simply an URL.
It is not correct to say that the vector space model will lead to the fastest search engine. It is not because the mathematical formula is somewhat easier that it leads to fast performance. All other models, when actually implemented, are a summation of term weights. The indexing time may differ as the more data is needed, the longest it will take to build the index, and the larger the index.

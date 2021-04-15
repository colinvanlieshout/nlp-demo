# Question Answering and Named Entity Recognition demo

Demo of two NLP methods applied to the Dutch language:
- Question Answering: uses https://huggingface.co/henryk/bert-base-multilingual-cased-finetuned-dutch-squad2.
- Named Entity Recognition: uses nl_core_news_md  https://spacy.io/models/nl

For a demo:
- Clone it
- pip install -r requirements in a venv
- Streamlit run main.py
- Select a file in data/pdf, tk-bijlage-wob-iccb works the best
- Question answering
    - First three questions will be automatically generated
    - Ask a question. One which works well is "Over welk ministerie wordt er gesproken?". Feel free to test others.
- NER
  - Go through some of the entity types and type in some that you find interesting. Some that I typically do
    - Absolute of relatieve datum of periode.
    - Organisaties
    - Landen, steden, staten (Nederland type ik dan in omdat die vrij vaak voorkomt

Important: If you are doing a live demo, you should run it fully beforehand, such that the answers are in cache. Answering the questions takes some time so that will be a bit of awkward silence otherwise, unless you have any good puns or anecdotes with which you can dazzle your audience.

It is good to indicate that these are off-the-shelf models trained for another purpose. Answers won't be perfect, but are already pretty good. It could be finetuned to any domain.

Feel free to ask if there are any questions.

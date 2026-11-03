# Bolum 0: Kurulum ve Ortam Hazirligi - Soru Cevap

**Ders:** Dogal Dil Isleme (NLP)  
**Ogretim Uyesi:** Dr. Mesut Polatgil  
**Takim:** Alfa (Mehmet Can Efe)  
**Konu:** Hugging Face Chapter 0 (Setup)  

---

## Soru 1: Kutuphane Kurulumu

**Soru:** Hugging Face Transformers kutuphanesini tum gerekli gelistirme bagimliliklariyla birlikte yuklemek icin kullanilan resmi pip komutu hangisidir?

- A) `pip install nlp`  
- **B) `pip install "transformers[sentencepiece]"` (DOGRU CEVAP)**  
- C) `pip install huggingface-all`  
- D) `pip install torch-transformers-models`  

> **Aciklama:** Hugging Face resmi dokumantasyonunda, farkli tokenizer ve model formatlarini desteklemek amaciyla `transformers[sentencepiece]` komutu onerilmektedir.

---

## Soru 2: Sanal Ortam (Virtual Environment) Olusturma

**Soru:** Python'da projeye ozel, izole bir sanal ortam olusturmak icin hangi standart komut kullanilir?

- A) `python create environment`  
- B) `pip make venv`  
- **C) `python -m venv .env` (DOGRU CEVAP)**  
- D) `python install venv-all`  

> **Aciklama:** Python'un standart kutuphanesinde yer alan `venv` modulu ile `python -m venv <klasor_adi>` komutu calistirilarak bagimsiz sanal ortam olusturulur.

---

## Soru 3: Hugging Face Token Girisi

**Soru:** Hugging Face Hub uzerindeki modelleri indirmek ve terminal uzerinden kimlik dogrulamasi yapmak icin hangi komut calistirilir?

- A) `git huggingface connect`  
- **B) `huggingface-cli login` (DOGRU CEVAP)**  
- C) `python login huggingface`  
- D) `pip auth hf`  

> **Aciklama:** Hugging Face Hub CLI araci olan `huggingface-cli login` komutu kullanici erisim token'ini (User Access Token) sisteme kaydeder.

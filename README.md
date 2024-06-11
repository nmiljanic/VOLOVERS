# VOLOVERS

## Opis projekta
VOLOVERS je sustav za upravljanje volonterima i volonterskim aktivnostima. Projekt omogućuje administratorima da dodaju, ažuriraju i brišu aktivnosti, kao i da upravljaju bazom volontera. Volonteri mogu pregledavati dostupne aktivnosti i prijavljivati se na njih. Ovaj sustav ima za cilj olakšati proces organiziranja i sudjelovanja u volonterskim aktivnostima.

## Funkcionalnosti
- **Admin**:
  - Dodavanje nove aktivnosti
  - Ažuriranje postojećih aktivnosti
  - Brisanje aktivnosti
  - Dodavanje volontera u bazu
- **Volonteri**:
  - Pregled dostupnih aktivnosti
  - Prijava na odabrane aktivnosti

## Kako pokrenuti aplikaciju lokalno

### Korištenjem Docker-a

1. **Klonirajte repozitorij**:
   ```bash
   cd ~/Downloads
   git clone https://github.com/nmiljanic/VOLOVERS
   cd volovers

2. **Izgradite Docker sliku**:
   ```bash
   docker build -t volovers .

3. **Pokrenite Docker kontejner**:
  ```bash
  docker run -p 8080:8080 volovers

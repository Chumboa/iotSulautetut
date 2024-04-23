# EnvironmentSensorSystem

Tämä järjestelmä hyödyntää erilaisia sensoreita ja näyttöjä ympäristön lämpötilan ja kosteuden mittaamiseen ja näyttämiseen. Järjestelmä sisältää myös LED-valot, jotka reagoivat määriteltyihin raja-arvoihin.

## Laitteiston asennus

Laitteisto koostuu seuraavista osista:
- I2C-väylä
- ADC-muuntimet lämpötila- ja potentiometrisensorien lukemiseen
- DHT20-sensori lämpötilan ja kosteuden mittaamiseen
- SSD1306_I2C OLED-näyttö tietojen näyttämiseen
- LED-valot osoittamaan lämpötilan ja kosteuden raja-arvojen ylityksiä

## Ohjelmiston toteutus

Ohjelma sisältää seuraavat toiminnot:
- Laitteiston alustaminen
- Ympäristön tietojen lukeminen DHT20-sensorilta ja ADC-muuntimilta
- Lämpötilan ja kosteuden näyttäminen OLED-näytöllä
- LED-valojen päivittäminen perustuen määriteltyihin lämpötilan ja kosteuden raja-arvoihin

### Toiminnot

- `setup_hardware`: Alustaa I2C-väylän, ADC-muuntimet ja DHT20-sensorin.
- `init_display`: Alustaa OLED-näytön.
- `init_leds`: Alustaa LED-valot.
- `read_environment`: Lukee ympäristön lämpötilan ja kosteuden.
- `calculate_analog_temperature`: Laskee analogisen lämpötilan ADC:n lukemista.
- `update_display`: Päivittää OLED-näytön näyttämään lämpötilan, kosteuden ja niiden raja-arvot.
- `update_leds`: Päivittää LED-valot vastaamaan nykyisiä raja-arvoja.
- `run`: Suorittaa järjestelmän toimintoja jatkuvassa silmukassa, lukee ympäristötietoja, päivittää näytön ja LED-valot.

### Käyttö

Luokka `EnvironmentSensorSystem` voidaan käynnistää luomalla ilmentymä luokasta ja kutsumalla `run`-metodia. Esimerkki tästä löytyy koodin lopusta.


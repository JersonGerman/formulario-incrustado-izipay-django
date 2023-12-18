# Formulario Incrustado Django


## Requirements
- python > 3.10v

## Configuration
1. Cambiar el nombre del archivo de configuración `example.env` a `.env` en la carpeta `./django_formulario_incrustado/`
2. Configurar el archivo `.env` con tus credenciales de Izipay
```sh
IZI_USERNAME=12345678
IZI_PASSWORD=testpassword_xxxxxxxxxxkCMiSGpOQ9rLbQUlKYmunHSfI5SN54avffE
IZI_PUBLIC_KEY=12345678:testpublickey_xxxxxxxxxxy0hYRj29NoDYjBKV6uDAfP42sIonUhG7u
IZI_SHA256_HMAC=xxxxxxxxxx7j9hgKmZU4yhQ91gnqQ36S95YwBh7ByE8
IZI_API_IZIPAY=https://api.micuentaweb.pe
```

3. Instalar librerias
```sh
pip install django requests django-environ
```
4. Levantar servidor de desarrollo
```sh
py manage.py runserver
```
5. Abrir el domunio local en el navegador http://localhost:8000
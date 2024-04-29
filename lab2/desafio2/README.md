# Explicação sobre o desafio 2

> [!TIP]
> Para documentação das etapas específicas do código, ler os comentários feitos em desafio2.py.

Este programa recebe como entrada uma url, e através do programa desenvolvido por [TheScriptGuy](https://github.com/TheScriptGuy/getCertificateChain/) baixa todos os certificados SSL fornecidos pela página web nesta url, juntamente com um conjunto de entidades certificadoras confiadas pela Mozilla, em um arquivo ```cacert.pem```. Em seguida, o programa começa pelo certificado mais abaixo da hierarquia (o mais distante da raíz), que é identificado como certificado ```0```, e verifica se ele foi emitido pelo certificado ```1```. Este procedimento é então repetido para todos os demais certificados - é verificado se o certificado ```n``` foi emitido pelo certificado ```n + 1```. Caso esta condição seja verdadeira para todos os certificados fornecidos pela página web, verifica-se se o último certificado foi emitidos por alguma das entidades certificadoras em ```cacert.pem```, e em caso positivo, o programa retorna que a página é segura. Caso qualquer uma das condições descritas não seja satisfeita, o programa retorna que a página não é segura.

### Testes sugeridos
Com certificados: www.google.com
Sem certificados: handandbrainchess.com
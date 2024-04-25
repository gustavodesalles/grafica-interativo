Padrões para input de transformação:

Campo Transformation
- Translação: "translation"
- Rotação: "rotation"
- Escalonamento: "scaling"
- Rotação arbitrária: "arbitrary_rotation"

Campo Object Name
- Utilizar nome do objeto de acordo com a Object List

Campo Params
- Translação: x,y
- Rotação: ângulo
- Escalonamento: x,y
- Rotação arbitrária: ângulo,x,y

Padrões para "add object"

Campo Coordinates
- Ponto: "point,x,y"
- Reta: "line,x1,y1,x2,y2"
- Wireframe: "wireframe,x1,y1,x2,y2,...,xn,yn"

Rotação da window: inserir apenas o número do ângulo (em graus)

Import e export
- Import: <nome_do_objeto>.obj
- Export: <nome_do_objeto> (sem extensão)

Ao realizar o export, o arquivo será gerado na pasta do projeto.
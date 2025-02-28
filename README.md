# Geração de Relatórios Personalizados com a API do Vicarius vRx  
Esta aplicação foi criada para gerar relatórios personalizados utilizando a API do Vicarius vRx. Siga as etapas abaixo para configurá-la e utilizá-la corretamente.  

## Configuração
### Variáveis de ambiente
Entre no diretório do projeto crie um arquivo chamado ".env". Esse arquivo deve ter o seguinte conteúdo:
```ini
API_KEY="<CHAVE_API_VICARIUS>"
API_URL="https://<EMPRESA>.vicarius.cloud"
DESCRIPTION_FILE_URL="<LINK_PLANILHA_DESCRIÇÕES>"
DESCRIPTION_FILE_PATH="<PATH_PLANILHA_DE_DESCRIÇÕES>"
```

**Importante:** As variáveis de ambiente guardam informações necessárias para o acesso de dados da empresa no portal vRx. Por isso, **não compartilhe esse arquivo**, ele deve ser apenas criado e preenchido localmente.

### Planilha com descrições dos hosts
Caso a planilha esteja no onedrive, é preciso ter um link de acesso público de download.
Para isso, siga os seguintes passos:
1. Abra a planilha no onedrive pelo navegador
2. Clique em compartilhar
3. Gere um link que todos possam editar
4. Copie esse link e cole no arquivo .env ao parâmetro "DESCRIPTION_FILE_URL"
5. Adicione "&download=1" ao fim do link

Caso a planilha esteja armazenada localmente, basta adicionar o caminho relativo ou absoluto do arquivo ao parâmetro "DESCRIPTION_FILE_PATH" no arquivo .env. **Dica:** Adicione a planilha à pasta do projeto. Dessa forma, o caminho para o arquivo é apenas o seu nome.

**Observação:** Caso ambos os parâmetros (link para o onedrive e diretório local) sejam informados, o programa dará prioridade para o arquivo no onedrive.

## Execução
Execute o script de inicialização, especificando o tempo em dias para os dados do relatório.

- No Windows:
```powershell
    Set-ExecutionPolicy Unrestricted -Scope Process     # caso seja preciso fornecer permissão de execução
    \run.ps1 --dias <N_DIAS>"
```
- No Linux:
```bash
    chmod +x run.sh     # caso seja preciso fornecer permissão de execução
    ./run.sh --dias <N_DIAS>
```

Esse script inicializará um ambiente virtual Python e instalará todos os requisitos necessários para a aplicação, sem precisar instalá-los globalmente na sua máquina. Depois que o ambiente estiver ativado e os requisitos forem instalados, a aplicação será executada.

## Geração de relatórios
A execução da aplicação resultará na geração de um arquivo Excel com 8 planilhas: relatórios de hosts e de vulnerabilidades para SP, RJ, RS e outras localidades. O arquivo será armazenado na pasta "report" e incluirá a data de execução no seu nome.

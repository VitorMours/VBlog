# VBlog

<p align="center">
  <a href="https://go-skill-icons.vercel.app/">
    <img
      src="https://go-skill-icons.vercel.app/api/icons?i=python,django,mysql,gemini,docker,nginx,githubactions,gcp,html,javascript,tailwindcss,chartjs&theme=dark&perline=6"
      alt="Tecnologias utilizadas no projeto"
    />
  </a>
</p>

O VBlog é uma plataforma de conteúdo moderna e escalável, desenvolvida com Django e otimizada para execução nativa em nuvem no **Google Cloud Platform (GCP)**.

## 🎯 Diferenciais do Projeto

- **Infraestrutura Serverless**: Utiliza Cloud Run para execução sob demanda com escalonamento automático
- **Banco de Dados Gerenciado**: Cloud SQL (MySQL) com alta disponibilidade, backups automatizados e manutenção zero
- **TDD como Metodologia Principal**: Todo o desenvolvimento é guiado por testes, garantindo código mais limpo, manutenível e com menos bugs
- **CI/CD Automatizado**: Pipeline completo com GitHub Actions para testes, build e deploy
- **IA Generativa**: Integração com Google Gemini API para auxiliar na criação e otimização de conteúdo

## 🏗️ Arquitetura e Infraestrutura (GCP)

A aplicação foi projetada seguindo as melhores práticas cloud-native:

| Componente | Tecnologia | Finalidade |
|------------|------------|------------|
| **Computação** | Google Cloud Run | Hospedagem da aplicação Django em containers serverless com auto-scaling |
| **Banco de Dados** | Google Cloud SQL (MySQL) | Persistência de dados gerenciada, réplicas de leitura e backups automáticos |
| **Servir Arquivos Estáticos** | WhiteNoise | Distribuição eficiente de arquivos estáticos sem necessidade de servidor adicional |
| **Containerização** | Docker | Garantia de consistência entre ambientes local e produção |

### 🔄 Fluxo de Deploy

1. Push para branch principal dispara o pipeline no GitHub Actions
2. Execução da suíte de testes automatizados
3. Build da imagem Docker e push para Artifact Registry
4. Execução de job no Cloud Tasks para rodar `python manage.py migrate`
5. Atualização gradual (rolling update) do serviço no Cloud Run

## 🛠️ Stack de Tecnologias

- **Backend**: Django 4.2+ (Python 3.11)
- **Frontend**: HTML5, JavaScript vanilla, TailwindCSS
- **Banco de Dados**: MySQL 8.0
- **IA**: Google Gemini API
- **Infraestrutura**: Docker, GitHub Actions, GCP (Cloud Run, Cloud SQL, Cloud Storage)
- **Visualização de Dados**: Chart.js para dashboards administrativos

## 🧪 Metodologia TDD (Test-Driven Development)

O projeto adota TDD como prática fundamental. Cada nova funcionalidade é precedida por testes que definem seu comportamento esperado.

### Tipos de Testes Implementados:

- **Unitários**: Validação de models, forms e utilitários isoladamente
- **Integração**: Verificação da comunicação entre views, models e banco de dados
- **Aceitação**: Simulação de fluxos completos do usuário

Todos os testes seguem o padrão **AAA (Arrange-Act-Assert)** para máxima clareza.

## 🚀 Como Executar o Projeto
### Pré-requisitos

- Docker e Docker Compose (versão 3.8+)
- Python 3.11+
- Google Cloud SDK (para deploy)
- Conta no GCP com Cloud Run e Cloud SQL habilitados

### Configuração Local com Docker
Clone o repositório

```bash
git clone https://github.com/seu-usuario/vblog.git
cd vblog
```
Configure as variáveis de ambiente

```bash
cp .env.example .env
# Edite o .env com suas configurações locais
```
Suba os containers

```bash
docker-compose up --build
```
A aplicação estará disponível em http://localhost:8000

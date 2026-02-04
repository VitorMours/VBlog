from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import random
from faker import Faker

# Importar modelos
try:
    from blog.models import Post, Votes, Visualization
    CustomUser = get_user_model()
except ImportError:
    import django
    django.setup()
    from blog.models import Post, Votes, Visualization
    CustomUser = get_user_model()

class Command(BaseCommand):
    help = 'Seed database with sample data for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=10,
            help='Number of users to create'
        )
        parser.add_argument(
            '--posts',
            type=int,
            default=30,
            help='Number of posts to create'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding'
        )

    def handle(self, *args, **options):
        fake = Faker('pt_BR')
        num_users = options['users']
        num_posts = options['posts']
        
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            self.clear_data()
        
        self.stdout.write(self.style.SUCCESS('Starting to seed data...'))
        
        # Criar superusuário
        self.create_superuser()
        
        # Criar usuários regulares
        users = self.create_users(fake, num_users)
        
        # Criar posts
        posts = self.create_posts(fake, users, num_posts)
        
        # Criar votos
        self.create_votes(users, posts)
        
        # Criar visualizações
        self.create_visualizations(users, posts)
        
        # Criar e exibir conta de teste para acesso
        self.create_test_account()
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded database!'))
        self.stdout.write(self.style.SUCCESS(f'Created: {num_users} users, {num_posts} posts'))
    
    def clear_data(self):
        """Limpar dados existentes"""
        Visualization.objects.all().delete()
        Votes.objects.all().delete()
        Post.objects.all().delete()
        CustomUser.objects.filter(is_superuser=False).delete()
        
        self.stdout.write(self.style.SUCCESS('Existing data cleared'))
    
    def create_superuser(self):
        """Criar superusuário"""
        try:
            if not CustomUser.objects.filter(email='admin@example.com').exists():
                CustomUser.objects.create_superuser(
                    email='admin@example.com',
                    password='admin123',
                    first_name='Admin',
                    last_name='User'
                )
                self.stdout.write(self.style.SUCCESS('Superuser created: admin@example.com / admin123'))
            else:
                self.stdout.write(self.style.WARNING('Superuser already exists'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating superuser: {e}'))
    
    def create_users(self, fake, num_users):
        """Criar usuários regulares"""
        users = []
        for i in range(num_users):
            try:
                email = fake.unique.email()
                user = CustomUser.objects.create_user(
                    email=email,
                    password='password123',
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    is_active=True
                )
                users.append(user)
                self.stdout.write(f'  Created user: {email}')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating user {i+1}: {e}'))
        
        return users
    
    def create_posts(self, fake, users, num_posts):
        """Criar posts"""
        posts = []
        
        # Títulos de posts
        post_titles = [
            "Introdução ao Django Framework",
            "Python para Análise de Dados",
            "Desenvolvimento Web Moderno",
            "Machine Learning com Python",
            "Boas Práticas de Programação",
            "API REST com Django REST Framework",
            "Banco de Dados Relacionais",
            "Testes Automatizados em Python",
            "Deploy de Aplicações Django",
            "Segurança em Aplicações Web",
        ]
        
        # Conteúdos simples sem formatação complexa
        contents = [
            "Este é um post sobre Django, um framework web para Python. Django ajuda desenvolvedores a criar aplicações web rapidamente.",
            "Python é excelente para análise de dados. Com bibliotecas como Pandas e NumPy, podemos processar grandes volumes de informação.",
            "O desenvolvimento web moderno inclui várias tecnologias como HTML5, CSS3, JavaScript e frameworks backend como Django.",
            "Machine Learning está transformando o mundo. Python oferece bibliotecas como Scikit-learn para criar modelos preditivos.",
            "Escrever código limpo é essencial para manutenção. Use nomes descritivos e funções pequenas.",
            "APIs REST são fundamentais para comunicação entre sistemas. Django REST Framework facilita a criação de APIs.",
            "Bancos de dados relacionais como PostgreSQL são importantes para armazenar dados estruturados de forma eficiente.",
            "Testes automatizados garantem que seu código funcione corretamente. Django tem ótimo suporte para testes.",
            "Fazer deploy de aplicações Django pode ser feito em vários serviços como Heroku, AWS ou DigitalOcean.",
            "Segurança é crucial em aplicações web. Django oferece proteção contra várias vulnerabilidades comuns.",
        ]
        
        for i in range(num_posts):
            try:
                owner = random.choice(users)
                title = random.choice(post_titles) + f" {i+1}"
                content = random.choice(contents)
                
                post = Post(
                    _title=title,
                    _content=content,
                    _visibility=random.choice([True, False]),
                    _owner=owner,
                    _status=random.choice([0, 1, 2])
                )
                post.save()
                
                # Simular datas de criação variadas (últimos 30 dias)
                days_ago = random.randint(0, 30)
                post._created_at = timezone.now() - timedelta(days=days_ago)
                post.save(update_fields=['_created_at'])
                
                posts.append(post)
                
                if (i + 1) % 10 == 0:
                    self.stdout.write(f'  Created {i+1} posts...')
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating post {i+1}: {e}'))
        
        return posts
    
    def create_votes(self, users, posts):
        """Criar votos aleatórios"""
        self.stdout.write('Creating votes...')
        vote_count = 0
        
        for post in posts:
            # Cada post recebe votos de alguns usuários aleatórios
            num_voters = random.randint(0, min(5, len(users)))
            if num_voters > 0:
                voters = random.sample(users, num_voters)
            else:
                voters = []
            
            for user in voters:
                try:
                    Votes.objects.create(
                        origin_post=post,
                        user_id=user,
                        vote_value=random.choice([True, False])
                    )
                    vote_count += 1
                except Exception:
                    pass  # Ignora se já existe voto
        
        self.stdout.write(self.style.SUCCESS(f'  Created {vote_count} votes'))
    
    def create_visualizations(self, users, posts):
        """Criar visualizações aleatórias"""
        self.stdout.write('Creating visualizations...')
        view_count = 0
        
        for post in posts:
            # Cada post é visualizado por vários usuários
            num_viewers = random.randint(0, min(10, len(users)))
            if num_viewers > 0:
                viewers = random.sample(users, num_viewers)
            else:
                viewers = []
            
            for user in viewers:
                try:
                    # Criar múltiplas visualizações com datas diferentes
                    num_views = random.randint(1, 5)
                    for _ in range(num_views):
                        view = Visualization.objects.create(
                            user=user,
                            post=post
                        )
                        
                        # Simular datas variadas (últimos 30 dias)
                        days_ago = random.randint(0, 30)
                        view.created_at = timezone.now() - timedelta(days=days_ago)
                        view.save(update_fields=['created_at'])
                        
                        view_count += 1
                except Exception:
                    pass  # Ignora erros
        
        self.stdout.write(self.style.SUCCESS(f'  Created {view_count} visualizations'))
    
    def create_test_account(self):
        """Criar e exibir uma conta de teste para acesso"""
        try:
            test_email = 'test@example.com'
            test_password = 'test123'
            
            # Verificar se a conta já existe
            if not CustomUser.objects.filter(email=test_email).exists():
                test_user = CustomUser.objects.create_user(
                    email=test_email,
                    password=test_password,
                    first_name='Test',
                    last_name='User',
                    is_active=True
                )
                
                self.stdout.write(self.style.SUCCESS('\n' + '='*50))
                self.stdout.write(self.style.SUCCESS('CONTA DE TESTE CRIADA:'))
                self.stdout.write(self.style.SUCCESS(f'Login: {test_email}'))
                self.stdout.write(self.style.SUCCESS(f'Senha: {test_password}'))
                self.stdout.write(self.style.SUCCESS('='*50))
            else:
                # Se já existe, apenas exibir as credenciais
                self.stdout.write(self.style.SUCCESS('\n' + '='*50))
                self.stdout.write(self.style.SUCCESS('CONTA DE TESTE EXISTENTE:'))
                self.stdout.write(self.style.SUCCESS(f'Login: {test_email}'))
                self.stdout.write(self.style.SUCCESS(f'Senha: {test_password}'))
                self.stdout.write(self.style.SUCCESS('='*50))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao criar conta de teste: {e}'))